import itertools
import uuid
from itertools import groupby
from graphviz import Digraph

from config import BaseConfig


class StateMachine:
    def __init__(self):
        self.transitions = []
        self.states = []
        self.init_state = None
        self.finish_states = []
        self.catch_state = None
        self.language = []

    def add_init_state(self, state):
        if self.init_state is not None:
            raise ValueError('Init state is not none')

        if not isinstance(state, int):
            raise TypeError('Init state must be int')

        self.init_state = state
        if state not in self.states:
            self.states.append(state)

    def add_transition(self, start_state, end_state, symbol):
        if not isinstance(start_state, int):
            raise TypeError('Start state must be int')

        if not isinstance(end_state, int):
            raise TypeError('End state must be int')

        if not isinstance(symbol, str):
            raise TypeError('Symbol must be str')

        if start_state not in self.states:
            self.states.append(start_state)

        if end_state not in self.states:
            self.states.append(end_state)

        transition = [start_state, end_state, symbol]
        if transition not in self.transitions:
            self.transitions.append(transition)

        if symbol != BaseConfig.EPSILON and symbol not in self.language:
            self.language.append(symbol)

    def add_finish_state(self, state):
        if not isinstance(state, int):
            raise TypeError('Finish state must be int')

        if state not in self.finish_states:
            self.finish_states.append(state)

            if state not in self.states:
                self.states.append(state)

    def add_catch_state(self, state):
        if self.catch_state is not None:
            raise ValueError('Catch state is not none')

        if not isinstance(state, int):
            raise TypeError('Catch state must be int')

        self.catch_state = state

        if state not in self.states:
            self.states.append(state)

    def _check_smc(self):
        if len(self.states) == 0:
            raise BaseException('States list is empty')

        if self.init_state is None:
            raise BaseException('Init state is None')

        if len(self.finish_states) == 0:
            raise BaseException('Finish states list is empty')

        if len(self.transitions) == 0:
            raise BaseException('Transitions list is empty')

    def renumber_states(self, from_number=None):
        """
        Изменение нумерации состояний. Порядковый номер каждого состояния
        увеличивается на (1 + from_number), по умолчанию from_number = 0.
        Пример: при from_number = 2 и states = (1, 2, 3) новая нумерация
        состояний будет равна (4, 5, 6).
        """
        self._check_smc()

        if from_number is None:
            from_number = 0

        for i, state in enumerate(self.states):
            self.states[i] = state + 1 + from_number

        for i, state in enumerate(self.finish_states):
            self.finish_states[i] = state + 1 + from_number

        for i, transition in enumerate(self.transitions):
            self.transitions[i][0] = transition[0] + 1 + from_number
            self.transitions[i][1] = transition[1] + 1 + from_number

        self.init_state += (1 + from_number)

        if self.catch_state is not None:
            self.catch_state += (1 + from_number)

    def get_transitions_start_symbol(self, start_state, symbol):
        """Получить список переходов из состояния start_state
        по символу symbol"""

        if not isinstance(start_state, int):
            raise TypeError('Start state must be int')

        if not isinstance(symbol, str):
            raise TypeError('Symbol must be str')

        out_transitions = []
        for transition in self.transitions:
            if transition[0] == start_state and transition[2] == symbol:
                out_transitions.append(transition)

        return sorted(out_transitions)

    def get_transitions_end_symbol(self, end_state, symbol):
        """Получить список переходов в состояние end_state
        по символу symbol"""

        if not isinstance(end_state, int):
            raise TypeError('End state must be int')

        if not isinstance(symbol, str):
            raise TypeError('Symbol must be str')

        out_transitions = []
        for transition in self.transitions:
            if transition[1] == end_state and transition[2] == symbol:
                out_transitions.append(transition)

        return sorted(out_transitions)

    def get_e_closure(self, state):
        """Получить список состояний, достижимых из состояния state
        при ε-переходах"""

        self._check_smc()

        if state is None:
            return None

        if not isinstance(state, int):
            raise TypeError('State must be int')

        e_closure = []
        stack = [state]
        while len(stack) > 0:
            curr_state = stack.pop()
            if curr_state not in e_closure:
                e_closure.append(curr_state)
            suitable_transitions = self.get_transitions_start_symbol(curr_state, BaseConfig.EPSILON)
            for transition in suitable_transitions:
                stack.insert(0, transition[1])

        if len(e_closure) == 0:
            return None

        return sorted(e_closure)

    def get_e_closure_list(self, state_list):
        """Получить список состояний, достижимых из состояний state_list
        при ε-переходах"""

        self._check_smc()

        if state_list is None:
            return None

        if not isinstance(state_list, list):
            raise TypeError('State list must be list')

        e_closure_list = []
        for state in state_list:
            curr_list = self.get_e_closure(state)
            for curr_state in curr_list:
                if curr_state not in e_closure_list:
                    e_closure_list.append(curr_state)

        if len(e_closure_list) == 0:
            return None

        return sorted(e_closure_list)

    def get_move(self, start_state, symbol):
        """Получить список состояний, в которые есть переход из
        состояния start_state по символу symbol"""

        self._check_smc()

        if not isinstance(start_state, int):
            raise TypeError('Start state must be int')

        if not isinstance(symbol, str):
            raise TypeError('Symbol must be str')

        move = []
        transitions = self.get_transitions_start_symbol(start_state, symbol)

        if len(transitions) == 0:
            return None

        for transition in transitions:
            if transition[1] not in move:
                move.append(transition[1])

        return sorted(move)

    def get_move_list(self, start_states_list, symbol):
        """Получить список состояний, в которые есть переход из
        состояний списка start_states_list по символу symbol"""

        self._check_smc()

        if start_states_list is None:
            return None

        if not isinstance(start_states_list, list):
            raise TypeError('State list must be list')

        if not isinstance(symbol, str):
            raise TypeError('Symbol must be str')

        move_list = []
        for state in start_states_list:
            curr_list = self.get_move(state, symbol)
            if curr_list is not None:
                for curr_state in curr_list:
                    if curr_state not in move_list:
                        move_list.append(curr_state)

        if len(move_list) == 0:
            return None

        return sorted(move_list)

    def get_come(self, end_state, symbol):
        """Получить список состояний, из которых есть переход в
        состояние end_state по символу symbol"""
        if not isinstance(end_state, int):
            raise TypeError('End state must be int')

        if not isinstance(symbol, str):
            raise TypeError('Symbol must be str')

        out_states = []
        transitions = self.get_transitions_end_symbol(end_state, symbol)

        if len(transitions) == 0:
            return None

        for transition in transitions:
            if transition[0] not in out_states:
                out_states.append(transition[0])

        return sorted(out_states)

    def get_come_list(self, end_states_list, symbol):
        """Получить список состояний, в которых есть переход в
        состояния списка end_states_set по символу symbol"""
        if end_states_list is None:
            return None

        if not isinstance(end_states_list, list):
            raise TypeError('State list must be list')

        if not isinstance(symbol, str):
            raise TypeError('Symbol must be str')

        out_states = []
        for state in end_states_list:
            curr_list = self.get_come(state, symbol)
            if curr_list is not None:
                for curr_state in curr_list:
                    if curr_state not in out_states:
                        out_states.append(curr_state)

        if len(out_states) == 0:
            return None

        return sorted(out_states)

    def combine_states(self, states):
        if not isinstance(states, list):
            raise TypeError('States must be list')

        if len(states) < 2:
            raise TypeError('States list length must be 2 or more')

        states = sorted(states)
        combined_index = states[0]
        print()

        # Объединение состояний
        for transition in self.transitions:
            for i, value in enumerate(transition):
                if value in states:
                    transition[i] = combined_index

        # Изменение нумерации
        old_indices = list(set(self.states) - (set(states)))
        old_indices.append(combined_index)
        old_indices = sorted(old_indices)
        new_indices = [x for x in range(len(old_indices))]

        for transition in self.transitions:
            index = old_indices.index(transition[0])
            transition[0] = new_indices[index]

        for transition in self.transitions:
            index = old_indices.index(transition[1])
            transition[1] = new_indices[index]

        for i, state in enumerate(self.states):
            if state in states:
                self.states[i] = combined_index
            else:
                index = old_indices.index(state)
                self.states[i] = new_indices[index]

        for i, state in enumerate(self.finish_states):
            if state in states:
                self.finish_states[i] = combined_index
            else:
                index = old_indices.index(state)
                self.finish_states[i] = new_indices[index]

        # Удаление дубликатов
        self.transitions = [tran[0] for tran in groupby(sorted(self.transitions))]
        self.states = [state[0] for state in groupby(sorted(self.states))]
        self.finish_states = [state[0] for state in groupby(sorted(self.finish_states))]

    def draw(self):
        try:
            filename = str(uuid.uuid4()) + '.gv'
            f = Digraph('finite_state_machine', filename=filename, directory=BaseConfig.graphviz_dir)

            f.attr(rankdir='LR', size='8,5')
            f.attr('node', shape='doublecircle')

            for state in self.finish_states:
                f.node(str(state))
            f.attr('node', shape='circle')

            for transition in self.transitions:
                f.edge(str(transition[0]), str(transition[1]), str(transition[2]))

            f.render()
        except:
            print('Graph creation error')

    def debug_print_info(self):
        print('transitions: ', self.transitions)
        print('states: ', self.states)
        print('init state: ', self.init_state)
        print('catch state: ', self.catch_state)
        print('finish states: ', self.finish_states)
        print('language: ', self.language)
        print()
