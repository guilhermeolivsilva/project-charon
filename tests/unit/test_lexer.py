"""Implement unit tests for the `src.lexer.Lexer` class."""

import pytest
from string import ascii_lowercase

from src.lexer import Lexer


SOURCE_CODE = """
    int main()
    {
        struct my_struct {
            int x;
            float y;
        };

        int a;
        my_struct b;

        do {
            if (a < b.x) { a = a + 1; }
            else { b.y = b.y - 1.0; }
        }
        while (a < 10);
    }
"""


def test_parse_source_code():
    """
    Test the `Lexer.parse_source_code` method.
     
    This test uses a snippet that uses all reserved words.
    """

    expected_parsed_code = [
        ('INT_TYPE', None),
        ('FUNC', 'main'),
        ('LPAR', None),
        ('RPAR', None),
        ('LCBRA', None),
        ('STRUCT_DEF', 'my_struct'),
        ('LCBRA', None),
        ('INT_TYPE', None),
        ('ID', 'x'),
        ('SEMI', None),
        ('FLOAT_TYPE', None),
        ('ID', 'y'),
        ('SEMI', None),
        ('RCBRA', None),
        ('SEMI', None),
        ('INT_TYPE', None),
        ('ID', 'a'),
        ('SEMI', None),
        ('STRUCT_TYPE', 'my_struct'),
        ('ID', 'b'),
        ('SEMI', None),
        ('DO_SYM', None),
        ('LCBRA', None),
        ('IF_SYM', None),
        ('LPAR', None),
        ('ID', 'a'),
        ('LESS', None),
        ('ID', 'b'),
        ('DOT', None),
        ('PROP', 'x'),
        ('RPAR', None),
        ('LCBRA', None),
        ('ID', 'a'),
        ('EQUAL', None),
        ('ID', 'a'),
        ('PLUS', None),
        ('INT', 1),
        ('SEMI', None),
        ('RCBRA', None),
        ('ELSE_SYM', None),
        ('LCBRA', None),
        ('ID', 'b'),
        ('DOT', None),
        ('PROP', 'y'),
        ('EQUAL', None),
        ('ID', 'b'),
        ('DOT', None),
        ('PROP', 'y'),
        ('MINUS', None),
        ('FLOAT', 1.0),
        ('SEMI', None),
        ('RCBRA', None),
        ('RCBRA', None),
        ('WHILE_SYM', None),
        ('LPAR', None),
        ('ID', 'a'),
        ('LESS', None),
        ('INT', 10),
        ('RPAR', None),
        ('SEMI', None),
        ('RCBRA', None)
    ]

    lexer = Lexer(SOURCE_CODE)
    lexer_parsed_code = lexer.parse_source_code()

    assert list(lexer_parsed_code) == expected_parsed_code


@pytest.mark.parametrize(
    "word_tuple",
    [
        ("int", ("INT_TYPE", None)),
        ("float", ("FLOAT_TYPE", None)),
        ("do", ("DO_SYM", None)),
        ("while", ("WHILE_SYM", None)),
        ("if", ("IF_SYM", None)),
        ("else", ("ELSE_SYM", None)),
        ("return", ("RET_SYM", None)),
        ("{", ("LCBRA", None)),
        ("}", ("RCBRA", None)),
        ("(", ("LPAR", None)),
        (")", ("RPAR", None)),
        ("+", ("PLUS", None)),
        ("-", ("MINUS", None)),
        ("<", ("LESS", None)),
        (";", ("SEMI", None)),
        ("=", ("EQUAL", None))
    ]
)
def test_parse_word_symbols_and_words(word_tuple):
    """
    Test the `Lexer.parse_word` method with all the reserved words and symbols.

    Parameters
    ----------
    word_tuple : tuple
        A tuple of (word_to_parse, expected_symbol).
    """

    lexer = Lexer(None)

    word_to_parse, expected_symbol = word_tuple
    assert expected_symbol == lexer.parse_word(word_to_parse)


@pytest.mark.parametrize(
    "variable_tuple",
    [(f"var_{letter}", ("ID", letter)) for letter in ascii_lowercase]
)
def test_parse_word_variables(variable_tuple):
    """
    Test the `Lexer.parse_word` method with all the variables (i.e., a-z).

    Parameters
    ----------
    variable_tuple : tuple
        A tuple of (variable_to_parse, expected_symbol).
    """

    lexer = Lexer(None)

    variable_to_parse, expected_symbol = variable_tuple
    assert expected_symbol == lexer.parse_word(variable_to_parse)


@pytest.mark.parametrize(
    "literal_tuple",
    [
        *[(f"int_{str(i)}", ("INT", i)) for i in range(0, 10)],
        *[(f"float_{str(i)}.0", ("FLOAT", float(i))) for i in range(0, 10)]
    ]
)
def test_parse_word_literals(literal_tuple):
    """
    Test the `Lexer.parse_word` method with all the basic literals (0-9).

    Parameters
    ----------
    literal_tuple : tuple
        A tuple of (literal_to_parse, expected_symbol).
    """

    lexer = Lexer(None)

    literal_to_parse, expected_symbol = literal_tuple
    assert expected_symbol == lexer.parse_word(literal_to_parse)


def test_tokenize_source_code():
    """
    Test the `Lexer.tokenize_source_code` method.
     
    This test uses a snippet that uses all reserved words.
    """

    expected_preprocessed_code = [
        'int',
        'func_main',
        '(',
        ')',
        '{',
        'struct',
        'struct_my_struct',
        '{',
        'int',
        'var_x',
        ';',
        'float',
        'var_y',
        ';',
        '}',
        ';',
        'int',
        'var_a',
        ';',
        'var_my_struct',
        'var_b',
        ';',
        'do',
        '{',
        'if',
        '(',
        'var_a',
        '<',
        'var_b.x',
        ')',
        '{',
        'var_a',
        '=',
        'var_a',
        '+',
        'int_1',
        ';',
        '}',
        'else',
        '{',
        'var_b.y',
        '=',
        'var_b.y',
        '-',
        'float_1.0',
        ';',
        '}',
        '}',
        'while',
        '(',
        'var_a',
        '<',
        'int_10',
        ')',
        ';',
        '}'
    ]

    lexer = Lexer(SOURCE_CODE)

    assert lexer.tokenize_source_code() == expected_preprocessed_code

