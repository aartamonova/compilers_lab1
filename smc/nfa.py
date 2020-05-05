import copy

from config import BaseConfig, RegexConfig
from smc.smc import StateMachine
from utils import check_regex_symbols, prepare_regex


class NfaRegex:
    def __init__(self, regex_infix):
        if not check_regex_symbols(regex_infix):
            raise ValueError('Unacceptable symbols in regex')

        self.regex_infix = regex_infix
        self.regex_postfix = None
        self.nfa = None

    def _reset_nfa(self):
        self.nfa = None
        self.regex_postfix = None

    @staticmethod
    def _build_basic_sm(char):
        sm = StateMachine()
        sm.add_init_state(0)
        sm.add_finish_state(1)
        sm.add_catch_state(1)
        sm.add_transition(sm.init_state, sm.catch_state, char)
        return sm

    @staticmethod
    def _build_and_sm(sm1, sm2):
        sm = StateMachine()
        sm.add_init_state(sm1.init_state)

        for transition in sm1.transitions:
            sm.add_transition(transition[0], transition[1], transition[2])

        if sm1.catch_state > 0:
            sm2.renumber_states(sm1.catch_state - 1)
        else:
            sm2.renumber_states()

        for transition in sm2.transitions:
            sm.add_transition(transition[0], transition[1], transition[2])

        sm.add_finish_state(sm2.catch_state)
        sm.add_catch_state(sm2.catch_state)

        return sm

    @staticmethod
    def _build_or_sm(sm1, sm2):
        sm = StateMachine()
        sm.add_init_state(0)
        sm1.renumber_states()
        sm2.renumber_states(from_number=sm1.catch_state)

        sm.add_transition(sm.init_state, sm1.init_state, BaseConfig.EPSILON)
        sm.add_transition(sm.init_state, sm2.init_state, BaseConfig.EPSILON)

        for transition in sm1.transitions:
            sm.add_transition(transition[0], transition[1], transition[2])

        for transition in sm2.transitions:
            sm.add_transition(transition[0], transition[1], transition[2])

        sm.add_finish_state(sm2.catch_state + 1)
        sm.add_catch_state(sm2.catch_state + 1)

        sm.add_transition(sm1.catch_state, sm.catch_state, BaseConfig.EPSILON)
        sm.add_transition(sm2.catch_state, sm.catch_state, BaseConfig.EPSILON)

        sm.states = sorted(sm.states)

        return sm

    @staticmethod
    def _build_zero_or_more_sm(sm1):
        sm = StateMachine()
        sm.add_init_state(0)

        sm1.renumber_states()
        sm1.add_transition(sm1.catch_state, sm1.init_state, BaseConfig.EPSILON)

        for transition in sm1.transitions:
            sm.add_transition(transition[0], transition[1], transition[2])

        sm.add_finish_state(sm1.catch_state + 1)
        sm.add_catch_state(sm1.catch_state + 1)

        sm.add_transition(sm.init_state, sm1.init_state, BaseConfig.EPSILON)
        sm.add_transition(sm.init_state, sm.catch_state, BaseConfig.EPSILON)
        sm.add_transition(sm1.catch_state, sm.catch_state, BaseConfig.EPSILON)

        sm.states = sorted(sm.states)
        sm.transitions = sorted(sm.transitions)
        return sm

    def _build_one_or_more_sm(self, sm1):
        sm2 = self._build_zero_or_more_sm(copy.deepcopy(sm1))
        sm = self._build_and_sm(sm1, sm2)
        return sm

    def build(self):
        self._reset_nfa()
        self.regex_postfix = prepare_regex(self.regex_infix)

        sm_queue = []

        for char in self.regex_postfix:
            if char == RegexConfig.ZERO_OR_MORE:
                if len(sm_queue) < 1:
                    raise ValueError('Regex parsing error')
                sm1 = sm_queue.pop()
                sm = self._build_zero_or_more_sm(sm1)
                sm_queue.append(sm)

            elif char == RegexConfig.ONE_OR_MORE:
                if len(sm_queue) < 1:
                    raise ValueError('Regex parsing error')
                sm1 = sm_queue.pop()
                sm = self._build_one_or_more_sm(sm1)
                sm_queue.append(sm)

            elif char == RegexConfig.AND:
                if len(sm_queue) < 2:
                    raise ValueError('Regex parsing error')

                sm2 = sm_queue.pop()
                sm1 = sm_queue.pop()

                sm = self._build_and_sm(sm1, sm2)
                sm_queue.append(sm)

            elif char == RegexConfig.OR:
                if len(sm_queue) < 2:
                    raise ValueError('Regex parsing error')

                sm2 = sm_queue.pop()
                sm1 = sm_queue.pop()
                sm = self._build_or_sm(sm1, sm2)
                sm_queue.append(sm)

            # [A-Za-z0-9]
            elif char in RegexConfig.VALID_SYMBOLS:
                sm = self._build_basic_sm(char)
                sm_queue.append(sm)
            else:
                raise ValueError('Regex parsing error')

        self.nfa = sm_queue.pop()
