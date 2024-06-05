"""Implement unit tests for the `src.lexer.Lexer` class."""

import pytest
from string import ascii_lowercase

from src.lexer import Lexer


SOURCE_CODE = """
    int main()
    {
        struct my_struct {
            int x[5];
            float y;
        };

        int a;
        my_struct b;

        b.x = {1, 2, 3, 4, 5};

        do {
            if (a < b.x) { a = a + 1; }
            else { b.y = b.y - 1.0; }
        }
        while (a < 10);
    }
"""

INVALID_SOURCES = [
    # 1. Variable named after reserved word/symbol.
    "int int;",
    "float return;",
    "int {",

    # 2. Variable named after user-defined type.
    "struct abc { int x; }; int abc;",

    # 3. Multiple variables in a row without operator in between.
    "int a; int b; a b;",

    # 4. Unnamed struct.
    "struct { int x; };"
]


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
        ('LBRA', None),
        ('ARRAY_SIZE', 5),
        ('RBRA', None),
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
        ('ID', 'b'),
        ('DOT', None),
        ('PROP', 'x'),
        ('EQUAL', None),
        ('LCBRA', None),
        ('INT', 1),
        ('INT', 2),
        ('INT', 3),
        ('INT', 4),
        ('INT', 5),
        ('RCBRA', None),
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
        ("struct", ("STRUCT_DEF", None)),
        ("do", ("DO_SYM", None)),
        ("while", ("WHILE_SYM", None)),
        ("if", ("IF_SYM", None)),
        ("else", ("ELSE_SYM", None)),
        ("return", ("RET_SYM", None)),
        ("{", ("LCBRA", None)),
        ("[", ("LBRA", None)),
        ("]", ("RBRA", None)),
        ("}", ("RCBRA", None)),
        ("(", ("LPAR", None)),
        (")", ("RPAR", None)),
        ("+", ("PLUS", None)),
        ("-", ("MINUS", None)),
        ("<", ("LESS", None)),
        (";", ("SEMI", None)),
        ("=", ("EQUAL", None)),
        (".", ("DOT", None))
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

    expected_tokenized_code = [
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
        '[',
        'int_5',
        ']',
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
        'var_b.x',
        '=',
        '{',
        'int_1',
        'int_2',
        'int_3',
        'int_4',
        'int_5',
        '}',
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

    assert lexer.tokenize_source_code() == expected_tokenized_code


@pytest.mark.parametrize(
    "source_code",
    INVALID_SOURCES
)
def test_validate_source_code_syntax(source_code: str):
    """
    Test the `Lexer.tokenize_source_code` method.

    This snippets with covered syntax errors.
    """

    with pytest.raises(SyntaxError):
        lexer = Lexer(source_code)
        _ = lexer.parse_source_code()
