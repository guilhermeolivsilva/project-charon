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

int abc(int asda, int abcdef) {
    int bla = 1;
    float blabla = 2.0;
    long int xaxaxa;

    my_struct internal_struct_var;
    internal_struct_var.x = 1;

    bla = bla + function_that_returns_struct(blabla, 123);

    return blabla + bla;
}

my_struct function_that_returns_struct(int xyz, int aaa) {
    int internal_guy;
    return xyz + aaa;
}

struct test_struct {
    int abcd;
    int xyz;
}

int main() {
    int x = abc();
    int array[10];

    array[5] = 1;
    int y;

    if(((x << 4) == 1 or x > 1) and (x < 10)) {
        y = x & 1;
    }
    else {
        y = x | 1;
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
            'structs': {
                'my_struct': {
                    'pseudonymous': '%struct.1',
                    'attributes': {
                        'x': {'type': 'int', 'attr_pointer': 1},
                        'y': {'type': 'float', 'attr_pointer': 2}
                    }
                },
                'test_struct': {
                    'pseudonymous': '%struct.2',
                    'attributes': {
                        'abcd': {'type': 'int', 'attr_pointer': 1},
                        'xyz': {'type': 'int', 'attr_pointer': 2}
                    }
                }
            },
            'variables': {
                'a': {'type': 'int', 'pseudonymous': '%1', 'type_pseudonymous': '2'},
                'global_var': {'type': 'my_struct', 'pseudonymous': '%2', 'type_pseudonymous': '%struct.1'}
            }
        },
        'functions': {
            'abc': {
                'pseudonymous': '#1',
                'type': 'int',
                'arguments': {
                    'asda': {'type': 'int', 'pseudonymous': '%3'},
                    'abcdef': {'type': 'int', 'pseudonymous': '%4'}
                },
                'statements': [
                    ('VAR_DEF', {'name': 'bla', 'pseudonymous': '%5', 'type': 'int', 'type_pseudonymous': '2'}),
                    ('ASSIGN', {}),
                    ('CST', {'type': 'int', 'value': 1}),
                    ('SEMI', {}),
                    ('VAR_DEF', {'name': 'blabla', 'pseudonymous': '%6', 'type': 'float', 'type_pseudonymous': '3'}),
                    ('ASSIGN', {}),
                    ('CST', {'type': 'float', 'value': 2.0}),
                    ('SEMI', {}),
                    ('VAR_DEF', {'name': 'xaxaxa', 'pseudonymous': '%7', 'type': 'long', 'type_pseudonymous': '4'}),
                    ('SEMI', {}),
                    ('VAR_DEF', {'name': 'internal_struct_var', 'pseudonymous': '%8', 'type': 'my_struct', 'type_pseudonymous': '%struct.1'}),
                    ('SEMI', {}),
                    ('VAR', 'internal_struct_var'),
                    ('DOT', {}),
                    ('STRUCT_ATTR', 1),
                    ('ASSIGN', {}),
                    ('CST', {'type': 'int', 'value': 1}),
                    ('SEMI', {}),
                    ('VAR', '%5'),
                    ('ASSIGN', {}),
                    ('VAR', '%5'),
                    ('PLUS', {}),
                    ('FUNC_CALL', {'function': '#2', 'parameters': ['%6', 123]}),
                    ('SEMI', {}),
                    ('RET_SYM', {}),
                    ('VAR', '%6'),
                    ('PLUS', {}),
                    ('VAR', '%5'),
                    ('SEMI', {})
                ]
            },
            'function_that_returns_struct': {
                'pseudonymous': '#2',
                'type': 'my_struct',
                'arguments': {
                    'xyz': {'type': 'int', 'pseudonymous': '%3'},
                    'aaa': {'type': 'int', 'pseudonymous': '%4'}
                },
                'statements': [
                    ('VAR_DEF', {'name': 'internal_guy', 'pseudonymous': '%5', 'type': 'int', 'type_pseudonymous': '2'}),
                    ('SEMI', {}),
                    ('RET_SYM', {}),
                    ('VAR', '%3'),
                    ('PLUS', {}),
                    ('VAR', '%4'),
                    ('SEMI', {})
                ]
            },
            'main': {
                'pseudonymous': '#3',
                'type': 'int',
                'arguments': {},
                 'statements': [
                    ('VAR_DEF', {'name': 'x', 'pseudonymous': '%3', 'type': 'int', 'type_pseudonymous': '2'}),
                    ('ASSIGN', {}),
                    ('FUNC_CALL', {'function': '#1', 'parameters': []}),
                    ('SEMI', {}),
                    ('VAR_DEF', {'name': 'array', 'pseudonymous': '%4', 'type': 'int', 'type_pseudonymous': '2', 'length': 10}),
                    ('LBRA', {}),
                    ('CST', {'type': 'int', 'value': 10}),
                    ('RBRA', {}),
                    ('SEMI', {}),
                    ('VAR', '%4'),
                    ('LBRA', {}),
                    ('CST', {'type': 'int', 'value': 5}),
                    ('RBRA', {}),
                    ('ASSIGN', {}),
                    ('CST', {'type': 'int', 'value': 1}),
                    ('SEMI', {}),
                    ('VAR_DEF', {'name': 'y', 'pseudonymous': '%5', 'type': 'int', 'type_pseudonymous': '2'}),
                    ('SEMI', {}),
                    ('IF_SYM', {}),
                    ('LPAR', {}),
                    ('LPAR', {}),
                    ('LPAR', {}),
                    ('VAR', '%3'),
                    ('LSHIFT', {}),
                    ('CST', {'type': 'int', 'value': 4}),
                    ('RPAR', {}),
                    ('EQUAL', {}),
                    ('CST', {'type': 'int', 'value': 1}),
                    ('OR', {}),
                    ('VAR', '%3'),
                    ('GREATER', {}),
                    ('CST', {'type': 'int', 'value': 1}),
                    ('RPAR', {}),
                    ('AND', {}),
                    ('LPAR', {}),
                    ('VAR', '%3'),
                    ('LESS', {}),
                    ('CST', {'type': 'int', 'value': 10}),
                    ('RPAR', {}),
                    ('RPAR', {}),
                    ('LCBRA', {}),
                    ('VAR', '%5'),
                    ('ASSIGN', {}),
                    ('VAR', '%3'),
                    ('BITAND', {}),
                    ('CST', {'type': 'int', 'value': 1}),
                    ('SEMI', {}),
                    ('RCBRA', {}),
                    ('ELSE_SYM', {}),
                    ('LCBRA', {}),
                    ('VAR', '%5'),
                    ('ASSIGN', {}),
                    ('VAR', '%3'),
                    ('BITOR', {}),
                    ('CST', {'type': 'int', 'value': 1}),
                    ('SEMI', {}),
                    ('RCBRA', {}),
                    ('RET_SYM', {}),
                    ('LPAR', {}),
                    ('LPAR', {}),
                    ('VAR', '%3'),
                    ('MULT', {}),
                    ('VAR', '%5'),
                    ('RPAR', {}),
                    ('DIV', {}),
                    ('CST', {'type': 'int', 'value': 2}),
                    ('RPAR', {}),
                    ('RSHIFT', {}),
                    ('CST', {'type': 'int', 'value': 1}),
                    ('SEMI', {})
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
        'int',
        'abcdef',
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
        '123',
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
        'int',
        'aaa',
        ')',
        '{',
        'int',
        'internal_guy',
        ';',
        'return',
        'xyz',
        '+',
        'aaa',
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
        'int',
        'y',
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
