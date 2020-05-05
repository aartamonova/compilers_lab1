import unittest
from smc.smc import StateMachine


def generate_simple_smc():
    sm = StateMachine()
    sm.add_init_state(0)
    sm.add_finish_state(1)
    sm.add_catch_state(1)
    sm.add_transition(0, 1, 'a')
    return sm


class TestStateMachine(unittest.TestCase):
    def test_add_init_non_empty(self):
        smc = StateMachine()
        smc.add_init_state(0)
        with self.assertRaises(ValueError):
            smc.add_init_state(1)

    def test_add_init_not_int(self):
        smc = StateMachine()
        with self.assertRaises(TypeError):
            smc.add_init_state('a')

    def test_add_init_correct(self):
        smc = StateMachine()
        smc.add_init_state(0)
        self.assertEqual(smc.init_state, 0)

    def test_add_catch_non_empty(self):
        smc = StateMachine()
        smc.add_catch_state(1)
        with self.assertRaises(ValueError):
            smc.add_catch_state(2)

    def test_add_catch_not_int(self):
        smc = StateMachine()
        with self.assertRaises(TypeError):
            smc.add_catch_state('a')

    def test_add_catch_correct(self):
        smc = StateMachine()
        smc.add_catch_state(1)
        self.assertEqual(smc.catch_state, 1)

    def test_add_tran_start_not_int(self):
        smc = StateMachine()
        with self.assertRaises(TypeError):
            smc.add_transition('a', 1, 'a')

    def test_add_tran_end_not_int(self):
        smc = StateMachine()
        with self.assertRaises(TypeError):
            smc.add_transition(0, 'a', 'a')

    def test_add_tran_symbol_not_char(self):
        smc = StateMachine()
        with self.assertRaises(TypeError):
            smc.add_transition(0, 1, 2)

    def test_add_tran_correct(self):
        smc = StateMachine()
        smc.add_transition(0, 1, 'a')
        self.assertEqual(smc.transitions[0], [0, 1, 'a'])
        self.assertEqual(smc.states, [0, 1])
        self.assertEqual(smc.language, ['a'])

    def test_add_finish_not_int(self):
        smc = StateMachine()
        with self.assertRaises(TypeError):
            smc.add_finish_state('a')

    def test_add_finish_correct(self):
        smc = StateMachine()
        smc.add_finish_state(1)
        self.assertEqual(smc.finish_states, [1])
        self.assertEqual(smc.states, [1])

    def test_check_states_is_empty(self):
        smc = StateMachine()
        with self.assertRaises(BaseException):
            smc._check_smc()

    def test_check_init_is_none(self):
        smc = StateMachine()
        smc.add_transition(0, 1, 'a')
        with self.assertRaises(BaseException):
            smc._check_smc()

    def test_check_finish_is_empty(self):
        smc = StateMachine()
        smc.add_transition(0, 1, 'a')
        smc.add_init_state(0)
        with self.assertRaises(BaseException):
            smc._check_smc()

    def test_check_tran_is_empty(self):
        smc = StateMachine()
        smc.add_init_state(0)
        smc.add_finish_state(1)
        with self.assertRaises(BaseException):
            smc._check_smc()

    def test_renumber_correct(self):
        smc = generate_simple_smc()
        smc.renumber_states()
        self.assertEqual(smc.states, [1, 2])
        self.assertEqual(smc.init_state, 1)
        self.assertEqual(smc.finish_states, [2])
        self.assertEqual(smc.catch_state, 2)
        self.assertEqual(smc.transitions, [[1, 2, 'a']])

    def test_renumber_from_correct(self):
        smc = generate_simple_smc()
        smc.renumber_states(3)
        self.assertEqual(smc.states, [4, 5])
        self.assertEqual(smc.init_state, 4)
        self.assertEqual(smc.finish_states, [5])
        self.assertEqual(smc.catch_state, 5)
        self.assertEqual(smc.transitions, [[4, 5, 'a']])

    def test_e_closure_state_is_none(self):
        smc = generate_simple_smc()
        result = smc.get_e_closure(None)
        self.assertEqual(result, None)

    def test_e_closure_state_not_int(self):
        smc = generate_simple_smc()
        with self.assertRaises(TypeError):
            smc.get_e_closure('a')

    def test_e_closure_correct(self):
        smc = generate_simple_smc()
        result = smc.get_e_closure(0)
        self.assertEqual(result, [0])

    def test_get_tran_start_correct(self):
        smc = generate_simple_smc()
        result = smc.get_transitions_start_symbol(0, 'a')
        self.assertEqual(result, [[0, 1, 'a']])

    def test_get_tran_start_empty(self):
        smc = generate_simple_smc()
        result = smc.get_transitions_start_symbol(1, 'a')
        self.assertEqual(result, [])

    def test_get_tran_end_correct(self):
        smc = generate_simple_smc()
        result = smc.get_transitions_end_symbol(1, 'a')
        self.assertEqual(result, [[0, 1, 'a']])

    def test_get_tran_end_empty(self):
        smc = generate_simple_smc()
        result = smc.get_transitions_end_symbol(0, 'a')
        self.assertEqual(result, [])

    def test_e_closure_list_correct(self):
        smc = generate_simple_smc()
        result = smc.get_e_closure_list([0, 1])
        self.assertEqual(result, [0, 1])

    def test_move_correct(self):
        smc = generate_simple_smc()
        result = smc.get_move(0, 'a')
        self.assertEqual(result, [1])

    def test_move_none(self):
        smc = generate_simple_smc()
        result = smc.get_move(1, 'a')
        self.assertEqual(result, None)

    def test_move_list_none(self):
        smc = generate_simple_smc()
        result = smc.get_move_list([1], 'a')
        self.assertEqual(result, None)

    def test_move_list_correct(self):
        smc = generate_simple_smc()
        result = smc.get_move_list([0, 1], 'a')
        self.assertEqual(result, [1])

    def test_come_none(self):
        smc = generate_simple_smc()
        result = smc.get_come(0, 'a')
        self.assertEqual(result, None)

    def test_come_correct(self):
        smc = generate_simple_smc()
        result = smc.get_come(1, 'a')
        self.assertEqual(result, [0])

    def test_come_list_none(self):
        smc = generate_simple_smc()
        result = smc.get_come_list([0], 'a')
        self.assertEqual(result, None)

    def test_come_list_correct(self):
        smc = generate_simple_smc()
        result = smc.get_come_list([0, 1], 'a')
        self.assertEqual(result, [0])

    def test_combine_correct(self):
        smc = generate_simple_smc()
        smc.add_transition(0, 2, 'b')
        smc.add_finish_state(2)
        smc.combine_states([1, 2])
        self.assertEqual(smc.states, [0, 1])
        self.assertEqual(smc.init_state, 0)
        self.assertEqual(smc.catch_state, 1)
        self.assertEqual(smc.finish_states, [1])
        self.assertEqual(smc.language, ['a', 'b'])
        self.assertEqual(smc.transitions, [[0, 1, 'a'], [0, 1, 'b']])


if __name__ == "__main__":
    unittest.main()
