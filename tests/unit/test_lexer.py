"""Implement unit tests for the `src.lexer.Lexer` class."""

from copy import deepcopy

import pytest

from src.lexer import Lexer
from tests.unit.common import SOURCE_CODE, TOKENIZED_SOURCE_CODE


INVALID_STRUCTS = [
    # 1. Struct named after reserved word/symbol
    "struct int { int a; };",

    # 2. Struct attribute named after reserved word
    "struct abc { int float; };",

    # Struct attribute redefinition
    "struct abc { int a; int a; };",

    # Struct attribute with unknown type
    "struct abc { int a; unknown_type b; };"
]

INVALID_VARIABLES = [
    # 1. Variable with unknown type
    "unknown_type var;",

    # 2. Invalid variable definition
    "int var .",

    # 3. Variable redefinition (globals)
    "int abc; int xyz; int abc;",

    # 4. Variable redefinition (local)
    "int main() { int abc; int xyz; int abc; }",

    # 5. Variable redefinition (global + local)
    "int xyz; int main() { int abc; int xyz; }",
]

INVALID_FUNCTIONS = [
    # 1. Call of undefined function
    "int main() { int abc; abc = func(); }",

    # 2. Malformed function definitions
    "int abc(int) { return x; }",

    # 3. Unclosed function definition
    "int main() { int abc; return abc; "
]


INVALID_SOURCES = [
    *INVALID_STRUCTS,
    *INVALID_VARIABLES,
    *INVALID_FUNCTIONS
]


def test_parse_source_code():
    """
    Test the `Lexer.parse_source_code` method.
     
    This test uses a snippet that uses all reserved words.
    """

    expected_parsed_code = TOKENIZED_SOURCE_CODE

    _source = deepcopy(SOURCE_CODE)
    lexer = Lexer(source_code=_source)
    lexer_parsed_code = lexer.parse_source_code()

    assert lexer_parsed_code == expected_parsed_code


def test_split_source(): 
    """
    Test the `Lexer.split_source` method.

    This test uses a snippet that uses all reserved words.
    """

    expected_split_source = [
        'int',
        'a',
        '[',
        '10',
        ']',
        ';',
        'struct',
        'my_struct',
        '{',
        'int',
        'x',
        ';',
        'float',
        'y',
        ';',
        '}',
        ';',
        'my_struct',
        'global_var',
        ';',
        'my_struct',
        'function_that_returns_struct',
        '(',
        'int',
        'xyz',
        'int',
        'aaa',
        ')',
        '{',
        'int',
        'internal_guy',
        ';',
        'internal_guy',
        '=',
        'xyz',
        '+',
        'aaa',
        ';',
        'global_var.x',
        '=',
        'internal_guy',
        ';',
        'return',
        'global_var',
        ';',
        '}',
        'int',
        'some_simple_function',
        '(',
        'float',
        'param_1',
        'int',
        'param_2',
        ')',
        '{',
        'return',
        'param_1',
        '/',
        'param_2',
        ';',
        '}',
        'int',
        'abc',
        '(',
        'int',
        'asda',
        'int',
        'abcdef',
        ')',
        '{',
        'int',
        'bla',
        ';',
        'bla',
        '=',
        '1',
        ';',
        'float',
        'blabla',
        ';',
        'blabla',
        '=',
        '2.0',
        ';',
        'short',
        'xaxaxa',
        ';',
        'my_struct',
        'internal_struct_var',
        ';',
        'internal_struct_var.x',
        '=',
        '1',
        ';',
        'bla',
        '=',
        'bla',
        '+',
        'some_simple_function',
        '(',
        'blabla',
        '123',
        ')',
        ';',
        'abc',
        '(',
        '1',
        '2',
        ')',
        ';',
        'return',
        'blabla',
        '+',
        'bla',
        ';',
        '}',
        'struct',
        'test_struct',
        '{',
        'int',
        'abcd',
        ';',
        'int',
        'xyz',
        ';',
        '}',
        'int',
        'main',
        '(',
        ')',
        '{',
        'int',
        'x',
        ';',
        'x',
        '=',
        'abc',
        '(',
        ')',
        ';',
        'int',
        'array',
        '[',
        '10',
        ']',
        ';',
        'array',
        '[',
        '5',
        ']',
        '=',
        '1',
        ';',
        'int',
        'y',
        ';',
        'if',
        '(',
        '(',
        '(',
        '(',
        'x',
        '<<',
        '4',
        ')',
        '==',
        '1',
        ')',
        '||',
        '(',
        'x',
        '>',
        '1',
        ')',
        ')',
        '&&',
        '(',
        'x',
        '<',
        '10',
        ')',
        ')',
        '{',
        'y',
        '=',
        'x',
        '&',
        '1',
        ';',
        '}',
        'else',
        '{',
        'y',
        '=',
        'x',
        '|',
        '1',
        ';',
        '}',
        'return',
        '(',
        '(',
        'x',
        '*',
        'y',
        ')',
        '/',
        '2',
        ')',
        '>>',
        '1',
        ';',
        '}'
    ]

    _source = deepcopy(SOURCE_CODE)
    lexer = Lexer(source_code=_source)

    assert lexer.split_source() == expected_split_source


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
        lexer = Lexer(source_code=source_code)
        _ = lexer.parse_source_code()
