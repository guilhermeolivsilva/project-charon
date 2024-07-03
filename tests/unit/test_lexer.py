"""Implement unit tests for the `src.lexer.Lexer` class."""

import pytest

from src.lexer import Lexer


SOURCE_CODE = """
int a = 1;

struct my_struct {
    int x;
    float y;
};

my_struct global_var;

int abc(int asda) {
    int bla = 1;
    float blabla = 2.0;
    long int xaxaxa;

    my_struct internal_struct_var;
    internal_struct_var.x = 1;

    bla = bla + function_that_returns_struct(blabla);

    return blabla + bla;
}

my_struct function_that_returns_struct(int xyz) {
    return xyz;
}

struct test_struct {
    int abcd;
    int xyz;
}

int main() {
    int x = abc();
    int array[10];

    array[5] = 1;

    if(((x << 4) == 1 or x > 1) and (x < 10)) {
        int y = x & 1;
    }
    else {
        int y = x | 1;
    }

    return ((x * y) / 2) >> 1;
}
"""

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
    "int var ." 
]

INVALID_FUNCTIONS = [
    # 1. Call of undefined function
    "int main() { int abc; abc = func(); }",

    # 2. Malformed function definitions
    "int abc(int) { return x; }",
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

    expected_parsed_code = {
        'globals': {
            'variables': {
                'a': {'type': 'int'},
                'global_var': {'type': 'my_struct'}
            },
            'structs': {
                'my_struct': {'x': 'int', 'y': 'float'},
                'test_struct': {'abcd': 'int', 'xyz': 'int'}
            }
        },
        'functions': {
            'abc': {
                'type': 'int',
                'arguments': {'asda': 'int'},
                'statements': [
                    ('VAR_DEF', {'name': 'bla', 'type': 'int'}),
                    'ASSIGN',
                    ('CST', {'type': 'int', 'value': 1}),
                    'SEMI',
                    ('VAR_DEF', {'name': 'blabla', 'type': 'float'}),
                    'ASSIGN',
                    ('CST', {'type': 'float', 'value': 2.0}),
                    'SEMI',
                    ('VAR_DEF', {'name': 'xaxaxa', 'type': 'long'}),
                    'SEMI',
                    ('VAR_DEF', {'name': 'internal_struct_var', 'type': 'my_struct'}),
                    'SEMI',
                    ('VAR', 'internal_struct_var'),
                    'DOT',
                    ('STRUCT_ATTR', 'x'),
                    'ASSIGN',
                    ('CST', {'type': 'int', 'value': 1}),
                    'SEMI',
                    ('VAR', 'bla'),
                    'ASSIGN',
                    ('VAR', 'bla'),
                    'PLUS',
                    ('FUNC_CALL',
                    {'function': 'function_that_returns_struct', 'parameters': ['blabla']}),
                    'LPAR',
                    ('VAR', 'blabla'),
                    'RPAR',
                    'SEMI',
                    'RET_SYM',
                    ('VAR', 'blabla'),
                    'PLUS',
                    ('VAR', 'bla'),
                    'SEMI'
                ]
            },
            'function_that_returns_struct': {
                'type': 'my_struct',
                'arguments': {'xyz': 'int'},
                'statements': [
                    'RET_SYM',
                    ('VAR', 'xyz'),
                    'SEMI'
                ]
            },
            'main': {
                'type': 'int',
                'arguments': {},
                'statements': [
                    ('VAR_DEF', {'name': 'x', 'type': 'int'}),
                    'ASSIGN',
                    ('FUNC_CALL', {'function': 'abc', 'parameters': []}),
                    'LPAR',
                    'RPAR',
                    'SEMI',
                    ('VAR_DEF', {'name': 'array', 'type': 'int', 'length': 10}),
                    'LBRA',
                    ('CST', {'type': 'int', 'value': 10}),
                    'RBRA',
                    'SEMI',
                    ('VAR', 'array'),
                    'LBRA',
                    ('CST', {'type': 'int', 'value': 5}),
                    'RBRA',
                    'ASSIGN',
                    ('CST', {'type': 'int', 'value': 1}),
                    'SEMI',
                    'IF_SYM',
                    'LPAR',
                    'LPAR',
                    'LPAR',
                    ('VAR', 'x'),
                    'LSHIFT',
                    ('CST', {'type': 'int', 'value': 4}),
                    'RPAR',
                    'EQUAL',
                    ('CST', {'type': 'int', 'value': 1}),
                    'OR',
                    ('VAR', 'x'),
                    'GREATER',
                    ('CST', {'type': 'int', 'value': 1}),
                    'RPAR',
                    'AND',
                    'LPAR',
                    ('VAR', 'x'),
                    'LESS',
                    ('CST', {'type': 'int', 'value': 10}),
                    'RPAR',
                    'RPAR',
                    'LCBRA',
                    ('VAR_DEF', {'name': 'y', 'type': 'int'}),
                    'ASSIGN',
                    ('VAR', 'x'),
                    'BITAND',
                    ('CST', {'type': 'int', 'value': 1}),
                    'SEMI',
                    'RCBRA',
                    'ELSE_SYM',
                    'LCBRA',
                    ('VAR', 'y'),
                    'ASSIGN',
                    ('VAR', 'x'),
                    'BITOR',
                    ('CST', {'type': 'int', 'value': 1}),
                    'SEMI',
                    'RCBRA',
                    'RET_SYM',
                    'LPAR',
                    'LPAR',
                    ('VAR', 'x'),
                    'MULT',
                    ('VAR', 'y'),
                    'RPAR',
                    'DIV',
                    ('CST', {'type': 'int', 'value': 2}),
                    'RPAR',
                    'RSHIFT',
                    ('CST', {'type': 'int', 'value': 1}),
                    'SEMI'
                ]
            }
        }
    }

    lexer = Lexer(SOURCE_CODE)
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
        '=',
        '1',
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
        'int',
        'abc',
        '(',
        'int',
        'asda',
        ')',
        '{',
        'int',
        'bla',
        '=',
        '1',
        ';',
        'float',
        'blabla',
        '=',
        '2.0',
        ';',
        'long',
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
        'function_that_returns_struct',
        '(',
        'blabla',
        ')',
        ';',
        'return',
        'blabla',
        '+',
        'bla',
        ';',
        '}',
        'my_struct',
        'function_that_returns_struct',
        '(',
        'int',
        'xyz',
        ')',
        '{',
        'return',
        'xyz',
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
        'if',
        '(',
        '(',
        '(',
        'x',
        '<<',
        '4',
        ')',
        '==',
        '1',
        'or',
        'x',
        '>',
        '1',
        ')',
        'and',
        '(',
        'x',
        '<',
        '10',
        ')',
        ')',
        '{',
        'int',
        'y',
        '=',
        'x',
        '&',
        '1',
        ';',
        '}',
        'else',
        '{',
        'int',
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

    lexer = Lexer(SOURCE_CODE)

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
        lexer = Lexer(source_code)
        _ = lexer.parse_source_code()
