import string
import os

root_dir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    EPSILON = 'ε'
    graphviz_dir = root_dir + '/graphviz'


class RegexConfig:
    OR = '|'
    AND = '&'
    ZERO_OR_MORE = '*'
    ONE_OR_MORE = '?'
    OPEN_BRACKET = '('
    CLOSE_BRACKET = ')'

    VALID_OPERATORS = OR + AND + ZERO_OR_MORE + ONE_OR_MORE + OPEN_BRACKET + CLOSE_BRACKET
    VALID_SYMBOLS = string.ascii_letters + string.digits
    VALID_CHARS = VALID_SYMBOLS + VALID_OPERATORS
