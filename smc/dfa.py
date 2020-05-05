import copy

from smc.smc import StateMachine
from utils import get_dict_value_by_key


class DfaNfa:
    def __init__(self, nfa):
        self.nfa = nfa

        if not nfa or not isinstance(nfa, StateMachine):
            raise TypeError('Nfa must be non empty StateMachine class member')

        self.dfa = None

    def _reset_dfa(self):
        self.dfa = None

    def build(self):
        self._reset_dfa()
        self.dfa = StateMachine()
        self.dfa.language = self.nfa.language
        self.dfa.add_init_state(0)

        dfa_states = dict()
        unmarked_queue = []  # очередь с помеченными состояниями ДКА
        marked_queue = []
        start_state_list = self.nfa.get_e_closure(self.nfa.init_state)
        unmarked_queue.append(start_state_list)

        dfa_states[0] = start_state_list
        dfa_state_num = 1

        while len(unmarked_queue) > 0:
            start_state_list = unmarked_queue.pop()
            marked_queue.append(start_state_list)
            for symbol in self.dfa.language:
                move_list = self.nfa.get_move_list(start_state_list, symbol)
                end_state_list = self.nfa.get_e_closure_list(move_list)

                if end_state_list is not None and end_state_list not in marked_queue:
                    unmarked_queue.append(end_state_list)
                    dfa_states[dfa_state_num] = end_state_list
                    dfa_state_num += 1

                # Переход в ДКА
                start_state = get_dict_value_by_key(dfa_states, start_state_list)
                end_state = get_dict_value_by_key(dfa_states, end_state_list)
                if start_state is not None and end_state is not None:
                    self.dfa.add_transition(start_state, end_state, symbol)

                    for state in end_state_list:
                        if state in self.nfa.finish_states:
                            self.dfa.add_finish_state(end_state)

    def minimize(self):
        if self.dfa is None:
            raise TypeError('Use build() first')

        dfa_classes = []
        classes_queue = []

        # Начальное разбиение
        finish_states = self.dfa.finish_states
        without_finish_states = list(set(self.dfa.states) - set(finish_states))

        dfa_classes.append(finish_states)
        dfa_classes.append(without_finish_states)
        classes_queue.append(finish_states)
        classes_queue.append(without_finish_states)

        # Поиск эквивалентных классов состояний
        while classes_queue:
            curr_queue_item = classes_queue.pop()
            for symbol in self.dfa.language:
                # Список состояний, в которых есть переход в состояния из curr_queue_item
                # по символу symbol
                curr_end_list = self.dfa.get_come_list(curr_queue_item, symbol)
                if curr_end_list is not None:

                    dfa_classes_frozen = copy.deepcopy(dfa_classes)
                    for curr_dfa_class in dfa_classes_frozen:
                        intersection = set(curr_end_list) & set(curr_dfa_class)
                        subtraction = set(curr_dfa_class) - set(curr_end_list)

                        if len(intersection) > 0 and len(subtraction) > 0:
                            index = dfa_classes.index(curr_dfa_class)
                            dfa_classes.pop(index)
                            dfa_classes.append(list(intersection))
                            dfa_classes.append(list(subtraction))

                            if curr_dfa_class in classes_queue:
                                index = classes_queue.index(curr_dfa_class)
                                classes_queue.pop(index)
                                classes_queue.append(list(intersection))
                                classes_queue.append(list(subtraction))
                            else:
                                if len(intersection) <= len(subtraction):
                                    classes_queue.append(list(intersection))
                                else:
                                    classes_queue.append(list(subtraction))

        for dfa_class in dfa_classes:
            if len(dfa_class) > 1:
                self.dfa.combine_states(dfa_class)

    def run(self, chain):
        if self.dfa is None:
            raise TypeError('Use build() first')

        self.nfa.draw()
        self.dfa.draw()
        self.dfa.debug_print_info()

        print('Входная строка: ', chain)
        is_valid = True
        i = 0
        curr_state = self.dfa.init_state
        while is_valid and i < len(chain):
            print('Текущий символ: ', chain[i])
            next_state = self.dfa.get_move(curr_state, chain[i])
            if next_state is not None and len(next_state) == 1:
                print('Переход: ', curr_state, '---> ', end='')
                curr_state = next_state.pop()
                print(curr_state, 'по символу ', chain[i])
            else:
                print('Переход не существует')
                is_valid = False
            i += 1

        if curr_state in self.dfa.finish_states:
            print('Достигнуто принимающее состояние')
        else:
            print('Принимающее состояние не достигнуто')
            is_valid = False

        print('\nРезультат: ', is_valid)

        return is_valid
