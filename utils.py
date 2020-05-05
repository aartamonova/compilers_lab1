from config import RegexConfig


def get_dict_value_by_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def check_regex_symbols(regex_str):
    for char in regex_str:
        if char not in RegexConfig.VALID_CHARS:
            return False
    return True


def prepare_regex(infix_regex_str):
    """
    Фильтрация пробельных символов входной строки, добавление неявных знаков
    конкатенации и преобразование в postfix-форму. Включает так же проверку
    на допустимые символы и корректность расставленных скобок.
    Выход в виде списка.
    """
    infix_regex_str = infix_regex_str.replace(' ', '')

    if not check_regex_symbols(infix_regex_str):
        raise ValueError('Unacceptable symbols in regex')

    infix_list = list(infix_regex_str)

    # Добавление неявных знаков конкатенации
    infix_list_concat = []
    for i, char in enumerate(infix_list):
        infix_list_concat.append(char)
        if (char not in [RegexConfig.OPEN_BRACKET, RegexConfig.OR,
                         RegexConfig.AND]) and (i + 1 < len(infix_list)):
            if infix_list[i + 1] not in [RegexConfig.ONE_OR_MORE,
                                         RegexConfig.ZERO_OR_MORE,
                                         RegexConfig.OR,
                                         RegexConfig.CLOSE_BRACKET,
                                         RegexConfig.AND]:
                infix_list_concat.append(RegexConfig.AND)

    # Преобразование к postfix-форме
    postfix_list = []
    operators = []
    brackets_count = 0

    for char in infix_list_concat:
        if char in [RegexConfig.OR, RegexConfig.AND]:
            if operators and operators[-1] != RegexConfig.OPEN_BRACKET:
                postfix_list.append(operators.pop())
            operators.append(char)

        elif char == RegexConfig.OPEN_BRACKET:
            brackets_count += 1
            operators.append(char)

        elif char == RegexConfig.CLOSE_BRACKET:
            if not operators:
                raise ValueError('Missing opening bracket(s)')

            brackets_count -= 1

            if operators[-1] != RegexConfig.OPEN_BRACKET:
                postfix_list.append(operators.pop())

            if not operators:
                raise ValueError('Missing opening bracket(s)')
            operators.pop()

        else:
            postfix_list.append(char)

    if operators:
        postfix_list.append(operators.pop())

    if brackets_count != 0:
        raise ValueError('Missing closing bracket(s)')

    return postfix_list
