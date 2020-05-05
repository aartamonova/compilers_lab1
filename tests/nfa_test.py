import unittest
from smc.nfa import NfaRegex


class TestNfaRegex(unittest.TestCase):
    def test_build_basic(self):
        nfa = NfaRegex('a')
        sm = nfa._build_basic_sm('a')
        self.assertEqual(sm.states, [0, 1])
        self.assertEqual(sm.init_state, 0)
        self.assertEqual(sm.finish_states, [1])
        self.assertEqual(sm.catch_state, 1)
        self.assertEqual(sm.language, ['a'])
        self.assertEqual(sm.transitions, [[0, 1, 'a']])

    def test_build_and(self):
        nfa = NfaRegex('a&b')
        sm1 = nfa._build_basic_sm('a')
        sm2 = nfa._build_basic_sm('b')
        sm = nfa._build_and_sm(sm1, sm2)
        self.assertEqual(sm.states, [0, 1, 2])
        self.assertEqual(sm.init_state, 0)
        self.assertEqual(sm.finish_states, [2])
        self.assertEqual(sm.catch_state, 2)
        self.assertEqual(sm.language, ['a', 'b'])
        self.assertEqual(sm.transitions, [[0, 1, 'a'], [1, 2, 'b']])

    def test_build_or(self):
        nfa = NfaRegex('a|b')
        sm1 = nfa._build_basic_sm('a')
        sm2 = nfa._build_basic_sm('b')
        sm = nfa._build_or_sm(sm1, sm2)
        self.assertEqual(sm.states, [0, 1, 2, 3, 4, 5])
        self.assertEqual(sm.init_state, 0)
        self.assertEqual(sm.finish_states, [5])
        self.assertEqual(sm.catch_state, 5)
        self.assertEqual(sm.language, ['a', 'b'])
        self.assertEqual(sm.transitions, [[0, 1, 'ε'], [0, 3, 'ε'],
                                          [1, 2, 'a'], [3, 4, 'b'],
                                          [2, 5, 'ε'], [4, 5, 'ε']])

    def test_build_zero_or_more(self):
        nfa = NfaRegex('a*')
        sm1 = nfa._build_basic_sm('a')
        sm = nfa._build_zero_or_more_sm(sm1)
        self.assertEqual(sm.states, [0, 1, 2, 3])
        self.assertEqual(sm.init_state, 0)
        self.assertEqual(sm.finish_states, [3])
        self.assertEqual(sm.catch_state, 3)
        self.assertEqual(sm.language, ['a'])
        self.assertEqual(sm.transitions, [[0, 1, 'ε'], [0, 3, 'ε'],
                                          [1, 2, 'a'], [2, 1, 'ε'],
                                          [2, 3, 'ε']])

    def test_build_one_or_more(self):
        nfa = NfaRegex('a?')
        sm1 = nfa._build_basic_sm('a')
        sm = nfa._build_one_or_more_sm(sm1)
        self.assertEqual(sm.states, [0, 1, 2, 4, 3])
        self.assertEqual(sm.init_state, 0)
        self.assertEqual(sm.finish_states, [4])
        self.assertEqual(sm.catch_state, 4)
        self.assertEqual(sm.language, ['a'])
        self.assertEqual(sm.transitions, [[0, 1, 'a'], [1, 2, 'ε'],
                                          [1, 4, 'ε'], [2, 3, 'a'],
                                          [3, 2, 'ε'], [3, 4, 'ε']])


if __name__ == "__main__":
    unittest.main()
