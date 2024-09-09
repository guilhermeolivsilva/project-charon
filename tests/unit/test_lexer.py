"""Implement unit tests for the `src.lexer.Lexer` class."""

import pytest

from src.lexer import Lexer


SOURCE_CODE = """
int a[10];

struct my_struct {
    int x;
    float y;
};

my_struct global_var;

my_struct function_that_returns_struct(int xyz, int aaa) {
    int internal_guy;
    return xyz + aaa;
}

int some_simple_function(float param_1, int param_2) {
    return param_1 / param_2;
}

int abc(int asda, int abcdef) {
    int bla;
    bla = 1;

    float blabla;
    blabla = 2.0;

    short xaxaxa;

    my_struct internal_struct_var;
    internal_struct_var.x = 1;

    bla = bla + some_simple_function(blabla, 123);

    abc(1, 2);

    return blabla + bla;
}

struct test_struct {
    int abcd;
    int xyz;
}

int main() {
    int x;
    x = abc();

    int array[10];

    array[5] = 1;
    int y;

    if((((x << 4) == 1) || (x > 1)) && (x < 10)) {
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

    expected_parsed_code = {
        "globals": {
            "structs": {
                "my_struct": {
                    "relative_position": 1,
                    "attributes": {
                        "x": {"type": "int", "attr_pointer": 0},
                        "y": {"type": "float", "attr_pointer": 1},
                    },
                    "active": True,
                },
                "test_struct": {
                    "relative_position": 2,
                    "attributes": {
                        "abcd": {"type": "int", "attr_pointer": 0},
                        "xyz": {"type": "int", "attr_pointer": 1},
                    },
                    "active": False,
                },
            },
            "variables": {
                "a": {"type": "int", "length": 10, "relative_position": 1},
                "global_var": {"type": "my_struct", "relative_position": 2},
            },
        },
        "functions": {
            "function_that_returns_struct": {
                "relative_position": 1,
                "type": "my_struct",
                "arguments": {
                    "xyz": {"type": "int", "relative_position": 3},
                    "aaa": {"type": "int", "relative_position": 4},
                },
                "statements": [
                    ("LCBRA", {}),
                    (
                        "VAR_DEF",
                        {"name": "internal_guy", "relative_position": 5, "type": "int"},
                    ),
                    ("SEMI", {}),
                    ("RET_SYM", {}),
                    ("VAR", {"type": "int", "relative_position": 3}),
                    ("ADD", {}),
                    ("VAR", {"type": "int", "relative_position": 4}),
                    ("SEMI", {}),
                    ("RCBRA", {}),
                ],
            },
            "some_simple_function": {
                "relative_position": 2,
                "type": "int",
                "arguments": {
                    "param_1": {"type": "float", "relative_position": 3},
                    "param_2": {"type": "int", "relative_position": 4},
                },
                "statements": [
                    ("LCBRA", {}),
                    ("RET_SYM", {}),
                    ("VAR", {"type": "float", "relative_position": 3}),
                    ("DIV", {}),
                    ("VAR", {"type": "int", "relative_position": 4}),
                    ("SEMI", {}),
                    ("RCBRA", {}),
                ],
            },
            "abc": {
                "relative_position": 3,
                "type": "int",
                "arguments": {
                    "asda": {"type": "int", "relative_position": 3},
                    "abcdef": {"type": "int", "relative_position": 4},
                },
                "statements": [
                    ("LCBRA", {}),
                    ("VAR_DEF", {"name": "bla", "relative_position": 5, "type": "int"}),
                    ("SEMI", {}),
                    ("VAR", {"name": "bla", "relative_position": 5, "type": "int"}),
                    ("ASSIGN", {}),
                    ("CST", {"type": "int", "value": 1}),
                    ("SEMI", {}),
                    (
                        "VAR_DEF",
                        {"name": "blabla", "relative_position": 6, "type": "float"},
                    ),
                    ("SEMI", {}),
                    ("VAR", {"name": "blabla", "relative_position": 6, "type": "float"}),
                    ("ASSIGN", {}),
                    ("CST", {"type": "float", "value": 2.0}),
                    ("SEMI", {}),
                    (
                        "VAR_DEF",
                        {"name": "xaxaxa", "relative_position": 7, "type": "short"},
                    ),
                    ("SEMI", {}),
                    (
                        "VAR_DEF",
                        {
                            "name": "internal_struct_var",
                            "relative_position": 8,
                            "type": "my_struct",
                        },
                    ),
                    ("SEMI", {}),
                    (
                        "VAR",
                        {
                            "relative_position": 8,
                            "attributes": {
                                "x": {"type": "int", "attr_pointer": 0},
                                "y": {"type": "float", "attr_pointer": 1},
                            },
                            "active": True,
                            "name": "internal_struct_var",
                            "type": "my_struct",
                        },
                    ),
                    ("DOT", {}),
                    ("CST", {"type": "int", "value": 0}),
                    ("ASSIGN", {}),
                    ("CST", {"type": "int", "value": 1}),
                    ("SEMI", {}),
                    ("VAR", {"name": "bla", "relative_position": 5, "type": "int"}),
                    ("ASSIGN", {}),
                    ("VAR", {"name": "bla", "relative_position": 5, "type": "int"}),
                    ("ADD", {}),
                    (
                        "FUNC_CALL",
                        {
                            "function": 2,
                            "return_type": "int",
                            "parameters": [
                                {
                                    "variable": True,
                                    "name": "blabla",
                                    "relative_position": 6,
                                    "type": "float",
                                },
                                {"variable": False, "type": "int", "value": 123},
                            ],
                        },
                    ),
                    ("SEMI", {}),
                    (
                        "FUNC_CALL",
                        {
                            "function": 3,
                            "return_type": "int",
                            "parameters": [
                                {"variable": False, "type": "int", "value": 1},
                                {"variable": False, "type": "int", "value": 2},
                            ],
                        },
                    ),
                    ("SEMI", {}),
                    ("RET_SYM", {}),
                    ("VAR", {"name": "blabla", "relative_position": 6, "type": "float"}),
                    ("ADD", {}),
                    ("VAR", {"name": "bla", "relative_position": 5, "type": "int"}),
                    ("SEMI", {}),
                    ("RCBRA", {}),
                ],
            },
            "main": {
                "relative_position": 4,
                "type": "int",
                "arguments": {},
                "statements": [
                    ("LCBRA", {}),
                    ("VAR_DEF", {"name": "x", "relative_position": 3, "type": "int"}),
                    ("SEMI", {}),
                    ("VAR", {"name": "x", "relative_position": 3, "type": "int"}),
                    ("ASSIGN", {}),
                    ("FUNC_CALL", {"function": 3, "return_type": "int", "parameters": []}),
                    ("SEMI", {}),
                    (
                        "VAR_DEF",
                        {
                            "name": "array",
                            "relative_position": 4,
                            "type": "int",
                            "length": 10,
                        },
                    ),
                    ("SEMI", {}),
                    (
                        "VAR",
                        {
                            "name": "array",
                            "relative_position": 4,
                            "type": "int",
                            "length": 10,
                        },
                    ),
                    ("LBRA", {}),
                    ("CST", {"type": "int", "value": 5}),
                    ("RBRA", {}),
                    ("ASSIGN", {}),
                    ("CST", {"type": "int", "value": 1}),
                    ("SEMI", {}),
                    ("VAR_DEF", {"name": "y", "relative_position": 5, "type": "int"}),
                    ("SEMI", {}),
                    ("IF_SYM", {}),
                    ("LPAR", {}),
                    ("LPAR", {}),
                    ("LPAR", {}),
                    ("LPAR", {}),
                    ("VAR", {"name": "x", "relative_position": 3, "type": "int"}),
                    ("LSHIFT", {}),
                    ("CST", {"type": "int", "value": 4}),
                    ("RPAR", {}),
                    ("EQUAL", {}),
                    ("CST", {"type": "int", "value": 1}),
                    ("RPAR", {}),
                    ("OR", {}),
                    ("LPAR", {}),
                    ("VAR", {"name": "x", "relative_position": 3, "type": "int"}),
                    ("GREATER", {}),
                    ("CST", {"type": "int", "value": 1}),
                    ("RPAR", {}),
                    ("RPAR", {}),
                    ("AND", {}),
                    ("LPAR", {}),
                    ("VAR", {"name": "x", "relative_position": 3, "type": "int"}),
                    ("LESS", {}),
                    ("CST", {"type": "int", "value": 10}),
                    ("RPAR", {}),
                    ("RPAR", {}),
                    ("LCBRA", {}),
                    ("VAR", {"name": "y", "relative_position": 5, "type": "int"}),
                    ("ASSIGN", {}),
                    ("VAR", {"name": "x", "relative_position": 3, "type": "int"}),
                    ("BITAND", {}),
                    ("CST", {"type": "int", "value": 1}),
                    ("SEMI", {}),
                    ("RCBRA", {}),
                    ("ELSE_SYM", {}),
                    ("LCBRA", {}),
                    ("VAR", {"name": "y", "relative_position": 5, "type": "int"}),
                    ("ASSIGN", {}),
                    ("VAR", {"name": "x", "relative_position": 3, "type": "int"}),
                    ("BITOR", {}),
                    ("CST", {"type": "int", "value": 1}),
                    ("SEMI", {}),
                    ("RCBRA", {}),
                    ("RET_SYM", {}),
                    ("LPAR", {}),
                    ("LPAR", {}),
                    ("VAR", {"name": "x", "relative_position": 3, "type": "int"}),
                    ("MULT", {}),
                    ("VAR", {"name": "y", "relative_position": 5, "type": "int"}),
                    ("RPAR", {}),
                    ("DIV", {}),
                    ("CST", {"type": "int", "value": 2}),
                    ("RPAR", {}),
                    ("RSHIFT", {}),
                    ("CST", {"type": "int", "value": 1}),
                    ("SEMI", {}),
                    ("RCBRA", {}),
                ],
            },
        },
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
        'return',
        'xyz',
        '+',
        'aaa',
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
