"""Implement unit tests for the `src.lexer.Lexer` class."""

import pytest
from string import ascii_lowercase

from src.lexer import Lexer


def test_parse_source_code():
    """
    Test the `Lexer.parse_source_code` method.
     
    This test uses a snippet that uses all reserved words.
    """

    source_code = """
    do {
        if (a < b) { a = a + 1; }
        else {b = b - 1;}
    }
    while (b < 10)
    """

    expected_parsed_code = [
        ("DO_SYM", None),
        ("LBRA", None),
        ("IF_SYM", None),
        ("LPAR", None),
        ("ID", "a"),
        ("LESS", None),
        ("ID", "b"),
        ("RPAR", None),
        ("LBRA", None),
        ("ID", "a"),
        ("EQUAL", None),
        ("ID", "a"),
        ("PLUS", None),
        ("INT", 1),
        ("SEMI", None),
        ("RBRA", None),
        ("ELSE_SYM", None),
        ("LBRA", None),
        ("ID", "b"), 
        ("EQUAL", None),
        ("ID", "b"),
        ("MINUS", None), 
        ("INT", 1),
        ("SEMI", None),
        ("RBRA", None), 
        ("RBRA", None),
        ("WHILE_SYM", None),
        ("LPAR", None),
        ("ID", "b"),
        ("LESS", None),
        ("INT", 10),
        ("RPAR", None)
    ]

    lexer_parsed_code = Lexer.parse_source_code(source_code)

    assert list(lexer_parsed_code) == expected_parsed_code


@pytest.mark.parametrize(
    "word_tuple",
    [
        ("do", ("DO_SYM", None)),
        ("while", ("WHILE_SYM", None)),
        ("if", ("IF_SYM", None)),
        ("else", ("ELSE_SYM", None)),
        ("{", ("LBRA", None)),
        ("}", ("RBRA", None)),
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

    word_to_parse, expected_symbol = word_tuple

    assert expected_symbol == Lexer.parse_word(word_to_parse)


@pytest.mark.parametrize(
    "variable_tuple",
    [(letter, ("ID", letter)) for letter in ascii_lowercase]
)
def test_parse_word_variables(variable_tuple):
    """
    Test the `Lexer.parse_word` method with all the variables (i.e., a-z).

    Parameters
    ----------
    variable_tuple : tuple
        A tuple of (variable_to_parse, expected_symbol).
    """

    variable_to_parse, expected_symbol = variable_tuple

    assert expected_symbol == Lexer.parse_word(variable_to_parse)


@pytest.mark.parametrize(
    "literal_tuple",
    [(str(i), ("INT", i)) for i in range(0, 10)]
)
def test_parse_word_literals(literal_tuple):
    """
    Test the `Lexer.parse_word` method with all the basic literals (0-9).

    Parameters
    ----------
    literal_tuple : tuple
        A tuple of (literal_to_parse, expected_symbol).
    """

    literal_to_parse, expected_symbol = literal_tuple

    assert expected_symbol == Lexer.parse_word(literal_to_parse)


def test_preprocess_source_code():
    """
    Test the `Lexer.preprocess_source_code` method.
     
    This test uses a snippet that uses all reserved words.
    """

    source_code = """
    do {
        if (a < b) { a = a + 1; }
        else {b = b - 1;}
    }
    while (b < 10)
    """

    expected_preprocessed_code = [
        "do",
        "{",
        "if",
        "(",
        "a",
        "<",
        "b",
        ")",
        "{",
        "a",
        "=",
        "a",
        "+",
        "1",
        ";",
        "}",
        "else",
        "{",
        "b",
        "=",
        "b",
        "-",
        "1",
        ";",
        "}",
        "}", 
        "while",
        "(",
        "b",
        "<",
        "10",
        ")"
    ]

    assert Lexer.preprocess_source_code(source_code) == expected_preprocessed_code

