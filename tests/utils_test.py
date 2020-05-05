import unittest
from utils import prepare_regex


class TestPrepareRegex(unittest.TestCase):
    def test_unacceptable(self):
        with self.assertRaises(ValueError):
            prepare_regex('abc123$')

    def test_miss_opening_bracket(self):
        with self.assertRaises(ValueError):
            prepare_regex('a|b)')

    def test_miss_closing_bracket(self):
        with self.assertRaises(ValueError):
            prepare_regex('(a|b')

    def test_spaces(self):
        result = ''.join(prepare_regex('a | b'))
        self.assertEqual(result, 'ab|')

    def test_correct_simple(self):
        result = ''.join(prepare_regex('(a|b)*&a?&b?&c'))
        self.assertEqual(result, 'ab|*a?&b?&c&')

    def test_concatenation(self):
        result = ''.join(prepare_regex('(a|b)*a?b?c'))
        self.assertEqual(result, 'ab|*a?&b?&c&')

    def test(self):
        result = ''.join(prepare_regex('(a|b|c)&(a|b)'))
        print(result)


if __name__ == "__main__":
    unittest.main()
