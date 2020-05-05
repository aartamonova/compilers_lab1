import unittest
from smc.dfa import DfaNfa
from smc.nfa import NfaRegex


class TestDfaNfa(unittest.TestCase):
    def test_build_correct_std(self):
        nfa = NfaRegex('(a|b)*abb')
        nfa.build()
        dfa = DfaNfa(nfa.nfa)
        dfa.build()
        self.assertEqual(dfa.dfa.states, [0, 1, 2, 4, 5])
        self.assertEqual(dfa.dfa.init_state, 0)
        self.assertEqual(dfa.dfa.finish_states, [5])
        self.assertEqual(dfa.dfa.language, ['a', 'b'])
        self.assertEqual(dfa.dfa.transitions, [[0, 1, 'a'], [0, 2, 'b'],
                                               [2, 1, 'a'], [2, 2, 'b'],
                                               [1, 1, 'a'], [1, 4, 'b'],
                                               [4, 1, 'a'], [4, 5, 'b'],
                                               [5, 1, 'a'], [5, 2, 'b']])

    def test_build_correct(self):
        nfa = NfaRegex('a?b?(abc)*')
        nfa.build()
        dfa = DfaNfa(nfa.nfa)
        dfa.build()
        self.assertEqual(dfa.dfa.states, [0, 1, 2, 3, 4, 5, 7, 8])
        self.assertEqual(dfa.dfa.init_state, 0)
        self.assertEqual(dfa.dfa.finish_states, [3, 5, 8])
        self.assertEqual(dfa.dfa.language, ['a', 'b', 'c'])
        self.assertEqual(dfa.dfa.transitions, [[0, 1, 'a'], [1, 2, 'a'],
                                               [1, 3, 'b'], [3, 4, 'a'],
                                               [3, 5, 'b'], [5, 4, 'a'],
                                               [5, 5, 'b'], [4, 7, 'b'],
                                               [7, 8, 'c'], [8, 4, 'a'],
                                               [2, 2, 'a'], [2, 3, 'b']])

    def test_minimize_correct_std(self):
        nfa = NfaRegex('(a|b)*abb')
        nfa.build()
        dfa = DfaNfa(nfa.nfa)
        dfa.build()
        dfa.minimize()
        self.assertEqual(dfa.dfa.states, [0, 1, 2, 3])
        self.assertEqual(dfa.dfa.init_state, 0)
        self.assertEqual(dfa.dfa.finish_states, [3])
        self.assertEqual(dfa.dfa.language, ['a', 'b'])
        self.assertEqual(dfa.dfa.transitions, [[0, 0, 'b'], [0, 1, 'a'],
                                               [1, 1, 'a'], [1, 2, 'b'],
                                               [2, 1, 'a'], [2, 3, 'b'],
                                               [3, 0, 'b'], [3, 1, 'a']])

    def test_minimize_correct(self):
        nfa = NfaRegex('a?b?(abc)*')
        nfa.build()
        dfa = DfaNfa(nfa.nfa)
        dfa.build()
        dfa.minimize()
        self.assertEqual(dfa.dfa.states, [0, 1, 2, 3, 4, 5])
        self.assertEqual(dfa.dfa.init_state, 0)
        self.assertEqual(dfa.dfa.finish_states, [2, 5])
        self.assertEqual(dfa.dfa.language, ['a', 'b', 'c'])
        self.assertEqual(dfa.dfa.transitions, [[0, 1, 'a'], [1, 1, 'a'],
                                               [1, 2, 'b'], [2, 2, 'b'],
                                               [2, 3, 'a'], [3, 4, 'b'],
                                               [4, 5, 'c'], [5, 3, 'a']])

    def test_run_valid_std(self):
        nfa = NfaRegex('(a|b)*abb')
        nfa.build()
        dfa = DfaNfa(nfa.nfa)
        dfa.build()
        dfa.minimize()
        result = dfa.run('ababaabb')
        self.assertEqual(result, True)

    def test_run_invalid_std(self):
        nfa = NfaRegex('(a|b)*abb')
        nfa.build()
        dfa = DfaNfa(nfa.nfa)
        dfa.build()
        dfa.minimize()
        result = dfa.run('ababaab')
        self.assertEqual(result, False)


if __name__ == "__main__":
    unittest.main()
