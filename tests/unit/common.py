"""Common definitions to be used across multiple tests."""

from copy import deepcopy

from src.abstract_syntax_tree import AbstractSyntaxTree


SOURCE_CODE = """
int a[10];

struct my_struct {
    int x;
    float y;
};

my_struct global_var;

my_struct function_that_returns_struct(int xyz, int aaa) {
    int internal_guy;
    internal_guy = xyz + aaa;

    global_var.x = internal_guy;
    return global_var;
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

    return blabla + bla;
}

struct test_struct {
    int abcd;
    int xyz;
};

int main() {
    int x;
    x = abc(1, 2);

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

TOKENIZED_SOURCE_CODE = {
    "globals": {
        "structs": {
            "my_struct": {
                "id": 1,
                "prime": 2,
                "attributes": {
                    "x": {"type": "int", "attr_pointer": 0},
                    "y": {"type": "float", "attr_pointer": 1},
                },
                "active": True,
            },
            "test_struct": {
                "id": 2,
                "prime": 3,
                "attributes": {
                    "abcd": {"type": "int", "attr_pointer": 0},
                    "xyz": {"type": "int", "attr_pointer": 1},
                },
                "active": False,
            },
        },
        "variables": {
            "a": {"type": "int", "length": 10, "id": 1, "prime": 2},
            "global_var": {
                "type": "my_struct",
                "attributes": {
                    "x": {"type": "int", "attr_pointer": 0},
                    "y": {"type": "float", "attr_pointer": 1},
                },
                "id": 2,
                "prime": 3,
            },
        },
    },
    "functions": {
        "function_that_returns_struct": {
            "id": 1,
            "prime": 2,
            "type": "my_struct",
            "parameters": {
                "xyz": {"type": "int", "id": 3, "prime": 5},
                "aaa": {"type": "int", "id": 4, "prime": 7},
            },
            "statements": [
                ("LCBRA", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "internal_guy",
                        "id": 5,
                        "prime": 11,
                        "type": "int",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "name": "internal_guy",
                        "id": 5,
                        "prime": 11,
                        "type": "int",
                    },
                ),
                ("ASSIGN", {}),
                ("VAR", {"type": "int", "id": 3, "prime": 5}),
                ("ADD", {}),
                ("VAR", {"type": "int", "id": 4, "prime": 7}),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "id": 2,
                        "prime": 3,
                        "attributes": {
                            "x": {"type": "int", "attr_pointer": 0},
                            "y": {"type": "float", "attr_pointer": 1},
                        },
                        "active": True,
                        "type": "my_struct",
                    },
                ),
                ("DOT", {}),
                ("CST", {"type": "int", "value": 0}),
                ("ASSIGN", {}),
                (
                    "VAR",
                    {
                        "name": "internal_guy",
                        "id": 5,
                        "prime": 11,
                        "type": "int",
                    },
                ),
                ("SEMI", {}),
                ("RET_SYM", {}),
                (
                    "VAR",
                    {
                        "type": "my_struct",
                        "attributes": {
                            "x": {"type": "int", "attr_pointer": 0},
                            "y": {"type": "float", "attr_pointer": 1},
                        },
                        "id": 2,
                        "prime": 3,
                    },
                ),
                ("SEMI", {}),
                ("RCBRA", {}),
            ],
        },
        "some_simple_function": {
            "id": 2,
            "prime": 3,
            "type": "int",
            "parameters": {
                "param_1": {"type": "float", "id": 6, "prime": 13},
                "param_2": {"type": "int", "id": 7, "prime": 17},
            },
            "statements": [
                ("LCBRA", {}),
                ("RET_SYM", {}),
                ("VAR", {"type": "float", "id": 6, "prime": 13}),
                ("DIV", {}),
                ("VAR", {"type": "int", "id": 7, "prime": 17}),
                ("SEMI", {}),
                ("RCBRA", {}),
            ],
        },
        "abc": {
            "id": 3,
            "prime": 5,
            "type": "int",
            "parameters": {
                "asda": {"type": "int", "id": 8, "prime": 19},
                "abcdef": {"type": "int", "id": 9, "prime": 23},
            },
            "statements": [
                ("LCBRA", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "bla",
                        "id": 10,
                        "prime": 29,
                        "type": "int",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "name": "bla",
                        "id": 10,
                        "prime": 29,
                        "type": "int",
                    },
                ),
                ("ASSIGN", {}),
                ("CST", {"type": "int", "value": 1}),
                ("SEMI", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "blabla",
                        "id": 11,
                        "prime": 31,
                        "type": "float",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "name": "blabla",
                        "id": 11,
                        "prime": 31,
                        "type": "float",
                    },
                ),
                ("ASSIGN", {}),
                ("CST", {"type": "float", "value": 2.0}),
                ("SEMI", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "xaxaxa",
                        "id": 12,
                        "prime": 37,
                        "type": "short",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "internal_struct_var",
                        "id": 13,
                        "prime": 41,
                        "type": "my_struct",
                        "attributes": {
                            "x": {"type": "int", "attr_pointer": 0},
                            "y": {"type": "float", "attr_pointer": 1},
                        },
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "id": 13,
                        "prime": 41,
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
                (
                    "VAR",
                    {
                        "name": "bla",
                        "id": 10,
                        "prime": 29,
                        "type": "int",
                    },
                ),
                ("ASSIGN", {}),
                (
                    "VAR",
                    {
                        "name": "bla",
                        "id": 10,
                        "prime": 29,
                        "type": "int",
                    },
                ),
                ("ADD", {}),
                (
                    "FUNC_CALL",
                    {
                        "arguments": [
                            {
                                "variable": True,
                                "name": "blabla",
                                "id": 11,
                                "prime": 31,
                                "type": "float",
                            },
                            {"variable": False, "type": "int", "value": 123},
                        ],
                        "called_function_metadata": {
                            "id": 2,
                            "prime": 3,
                            "type": "int",
                            "parameters": {
                                "param_1": {
                                    "type": "float",
                                    "id": 6,
                                    "prime": 13,
                                },
                                "param_2": {
                                    "type": "int",
                                    "id": 7,
                                    "prime": 17,
                                },
                            },
                            "statements": [
                                ("LCBRA", {}),
                                ("RET_SYM", {}),
                                (
                                    "VAR",
                                    {
                                        "type": "float",
                                        "id": 6,
                                        "prime": 13,
                                    },
                                ),
                                ("DIV", {}),
                                (
                                    "VAR",
                                    {
                                        "type": "int",
                                        "id": 7,
                                        "prime": 17,
                                    },
                                ),
                                ("SEMI", {}),
                                ("RCBRA", {}),
                            ],
                        },
                    },
                ),
                ("SEMI", {}),
                ("RET_SYM", {}),
                (
                    "VAR",
                    {
                        "name": "blabla",
                        "id": 11,
                        "prime": 31,
                        "type": "float",
                    },
                ),
                ("ADD", {}),
                (
                    "VAR",
                    {
                        "name": "bla",
                        "id": 10,
                        "prime": 29,
                        "type": "int",
                    },
                ),
                ("SEMI", {}),
                ("RCBRA", {}),
            ],
        },
        "main": {
            "id": 4,
            "prime": 7,
            "type": "int",
            "parameters": {},
            "statements": [
                ("LCBRA", {}),
                (
                    "VAR_DEF",
                    {"name": "x", "id": 14, "prime": 43, "type": "int"},
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {"name": "x", "id": 14, "prime": 43, "type": "int"},
                ),
                ("ASSIGN", {}),
                (
                    "FUNC_CALL",
                    {
                        "arguments": [
                            {"variable": False, "type": "int", "value": 1},
                            {"variable": False, "type": "int", "value": 2},
                        ],
                        "called_function_metadata": {
                            "id": 3,
                            "prime": 5,
                            "type": "int",
                            "parameters": {
                                "asda": {
                                    "type": "int",
                                    "id": 8,
                                    "prime": 19,
                                },
                                "abcdef": {
                                    "type": "int",
                                    "id": 9,
                                    "prime": 23,
                                },
                            },
                            "statements": [
                                ("LCBRA", {}),
                                (
                                    "VAR_DEF",
                                    {
                                        "name": "bla",
                                        "id": 10,
                                        "prime": 29,
                                        "type": "int",
                                    },
                                ),
                                ("SEMI", {}),
                                (
                                    "VAR",
                                    {
                                        "name": "bla",
                                        "id": 10,
                                        "prime": 29,
                                        "type": "int",
                                    },
                                ),
                                ("ASSIGN", {}),
                                ("CST", {"type": "int", "value": 1}),
                                ("SEMI", {}),
                                (
                                    "VAR_DEF",
                                    {
                                        "name": "blabla",
                                        "id": 11,
                                        "prime": 31,
                                        "type": "float",
                                    },
                                ),
                                ("SEMI", {}),
                                (
                                    "VAR",
                                    {
                                        "name": "blabla",
                                        "id": 11,
                                        "prime": 31,
                                        "type": "float",
                                    },
                                ),
                                ("ASSIGN", {}),
                                ("CST", {"type": "float", "value": 2.0}),
                                ("SEMI", {}),
                                (
                                    "VAR_DEF",
                                    {
                                        "name": "xaxaxa",
                                        "id": 12,
                                        "prime": 37,
                                        "type": "short",
                                    },
                                ),
                                ("SEMI", {}),
                                (
                                    "VAR_DEF",
                                    {
                                        "name": "internal_struct_var",
                                        "id": 13,
                                        "prime": 41,
                                        "type": "my_struct",
                                        "attributes": {
                                            "x": {"type": "int", "attr_pointer": 0},
                                            "y": {"type": "float", "attr_pointer": 1},
                                        },
                                    },
                                ),
                                ("SEMI", {}),
                                (
                                    "VAR",
                                    {
                                        "id": 13,
                                        "prime": 41,
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
                                (
                                    "VAR",
                                    {
                                        "name": "bla",
                                        "id": 10,
                                        "prime": 29,
                                        "type": "int",
                                    },
                                ),
                                ("ASSIGN", {}),
                                (
                                    "VAR",
                                    {
                                        "name": "bla",
                                        "id": 10,
                                        "prime": 29,
                                        "type": "int",
                                    },
                                ),
                                ("ADD", {}),
                                (
                                    "FUNC_CALL",
                                    {
                                        "arguments": [
                                            {
                                                "variable": True,
                                                "name": "blabla",
                                                "id": 11,
                                                "prime": 31,
                                                "type": "float",
                                            },
                                            {
                                                "variable": False,
                                                "type": "int",
                                                "value": 123,
                                            },
                                        ],
                                        "called_function_metadata": {
                                            "id": 2,
                                            "prime": 3,
                                            "type": "int",
                                            "parameters": {
                                                "param_1": {
                                                    "type": "float",
                                                    "id": 6,
                                                    "prime": 13,
                                                },
                                                "param_2": {
                                                    "type": "int",
                                                    "id": 7,
                                                    "prime": 17,
                                                },
                                            },
                                            "statements": [
                                                ("LCBRA", {}),
                                                ("RET_SYM", {}),
                                                (
                                                    "VAR",
                                                    {
                                                        "type": "float",
                                                        "id": 6,
                                                        "prime": 13,
                                                    },
                                                ),
                                                ("DIV", {}),
                                                (
                                                    "VAR",
                                                    {
                                                        "type": "int",
                                                        "id": 7,
                                                        "prime": 17,
                                                    },
                                                ),
                                                ("SEMI", {}),
                                                ("RCBRA", {}),
                                            ],
                                        },
                                    },
                                ),
                                ("SEMI", {}),
                                ("RET_SYM", {}),
                                (
                                    "VAR",
                                    {
                                        "name": "blabla",
                                        "id": 11,
                                        "prime": 31,
                                        "type": "float",
                                    },
                                ),
                                ("ADD", {}),
                                (
                                    "VAR",
                                    {
                                        "name": "bla",
                                        "id": 10,
                                        "prime": 29,
                                        "type": "int",
                                    },
                                ),
                                ("SEMI", {}),
                                ("RCBRA", {}),
                            ],
                        },
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "array",
                        "id": 15,
                        "prime": 47,
                        "type": "int",
                        "length": 10,
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "name": "array",
                        "id": 15,
                        "prime": 47,
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
                (
                    "VAR_DEF",
                    {"name": "y", "id": 16, "prime": 53, "type": "int"},
                ),
                ("SEMI", {}),
                ("IF_SYM", {}),
                ("LPAR", {}),
                ("LPAR", {}),
                ("LPAR", {}),
                ("LPAR", {}),
                (
                    "VAR",
                    {"name": "x", "id": 14, "prime": 43, "type": "int"},
                ),
                ("LSHIFT", {}),
                ("CST", {"type": "int", "value": 4}),
                ("RPAR", {}),
                ("EQUAL", {}),
                ("CST", {"type": "int", "value": 1}),
                ("RPAR", {}),
                ("OR", {}),
                ("LPAR", {}),
                (
                    "VAR",
                    {"name": "x", "id": 14, "prime": 43, "type": "int"},
                ),
                ("GREATER", {}),
                ("CST", {"type": "int", "value": 1}),
                ("RPAR", {}),
                ("RPAR", {}),
                ("AND", {}),
                ("LPAR", {}),
                (
                    "VAR",
                    {"name": "x", "id": 14, "prime": 43, "type": "int"},
                ),
                ("LESS", {}),
                ("CST", {"type": "int", "value": 10}),
                ("RPAR", {}),
                ("RPAR", {}),
                ("LCBRA", {}),
                (
                    "VAR",
                    {"name": "y", "id": 16, "prime": 53, "type": "int"},
                ),
                ("ASSIGN", {}),
                (
                    "VAR",
                    {"name": "x", "id": 14, "prime": 43, "type": "int"},
                ),
                ("BITAND", {}),
                ("CST", {"type": "int", "value": 1}),
                ("SEMI", {}),
                ("RCBRA", {}),
                ("ELSE_SYM", {}),
                ("LCBRA", {}),
                (
                    "VAR",
                    {"name": "y", "id": 16, "prime": 53, "type": "int"},
                ),
                ("ASSIGN", {}),
                (
                    "VAR",
                    {"name": "x", "id": 14, "prime": 43, "type": "int"},
                ),
                ("BITOR", {}),
                ("CST", {"type": "int", "value": 1}),
                ("SEMI", {}),
                ("RCBRA", {}),
                ("RET_SYM", {}),
                ("LPAR", {}),
                ("LPAR", {}),
                (
                    "VAR",
                    {"name": "x", "id": 14, "prime": 43, "type": "int"},
                ),
                ("MULT", {}),
                (
                    "VAR",
                    {"name": "y", "id": 16, "prime": 53, "type": "int"},
                ),
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

_source = deepcopy(TOKENIZED_SOURCE_CODE)
ABSTRACT_SYNTAX_TREE = AbstractSyntaxTree(source_code=_source)
ABSTRACT_SYNTAX_TREE_ROOT = ABSTRACT_SYNTAX_TREE.build()

ENVIRONMENT = {
    'variables': {
        1: {'address': '0x0', 'size': 40},
        2: {'address': '0x28', 'size': 8}
    },
    'functions': {}
}

MACHINE_CODE = {
    "functions": {
        "function_that_returns_struct": {"start": 0, "end": 28},
        "some_simple_function": {"start": 28, "end": 43},
        "abc": {"start": 43, "end": 88},
        "main": {"start": 88, "end": 155},
    },
    "global_vars": [],
    "code": [
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 0, "value": "0x30"},
            "instruction_id": 1,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 0, "value": "arg"},
            "instruction_id": 2,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 1, "value": "0x34"},
            "instruction_id": 3,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 1, "value": "arg"},
            "instruction_id": 4,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 2, "value": "0x38"},
            "instruction_id": 5,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 3, "lhs_register": 2, "rhs_register": "zero"},
            "instruction_id": 6,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 4, "value": "0x30"},
            "instruction_id": 7,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 5, "lhs_register": 4, "rhs_register": "zero"},
            "instruction_id": 8,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 6, "value": 5},
            "instruction_id": 9,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 7, "value": "0x34"},
            "instruction_id": 10,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 8, "lhs_register": 7, "rhs_register": "zero"},
            "instruction_id": 11,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 9, "value": 8},
            "instruction_id": 12,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 10, "lhs_register": 6, "rhs_register": 9},
            "instruction_id": 13,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 3, "value": 10},
            "instruction_id": 14,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 12, "value": "0x28"},
            "instruction_id": 15,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 13, "lhs_register": 12, "rhs_register": "zero"},
            "instruction_id": 16,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 14, "value": 0},
            "instruction_id": 17,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 15, "value": 0},
            "instruction_id": 18,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 16, "lhs_register": 13, "rhs_register": 15},
            "instruction_id": 19,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 17, "value": "0x38"},
            "instruction_id": 20,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 18, "lhs_register": 17, "rhs_register": "zero"},
            "instruction_id": 21,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 19, "value": 18},
            "instruction_id": 22,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 16, "value": 19},
            "instruction_id": 23,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 21, "value": "0x28"},
            "instruction_id": 24,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 22, "lhs_register": 21, "rhs_register": "zero"},
            "instruction_id": 25,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 23, "value": 22},
            "instruction_id": 26,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 23},
            "instruction_id": 27,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 28,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 24, "value": "0x3c"},
            "instruction_id": 29,
        },
        {
            "instruction": "STOREF",
            "metadata": {"register": 24, "value": "arg"},
            "instruction_id": 30,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 25, "value": "0x40"},
            "instruction_id": 31,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 25, "value": "arg"},
            "instruction_id": 32,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 26, "value": "0x3c"},
            "instruction_id": 33,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 27, "lhs_register": 26, "rhs_register": "zero"},
            "instruction_id": 34,
        },
        {
            "instruction": "LOADF",
            "metadata": {"register": 28, "value": 27},
            "instruction_id": 35,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 29, "value": "0x40"},
            "instruction_id": 36,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 30, "lhs_register": 29, "rhs_register": "zero"},
            "instruction_id": 37,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 31, "value": 30},
            "instruction_id": 38,
        },
        {
            "instruction": "SITOFP",
            "metadata": {"register": 32, "value": 31},
            "instruction_id": 39,
        },
        {
            "instruction": "FDIV",
            "metadata": {"register": 33, "lhs_register": 28, "rhs_register": 32},
            "instruction_id": 40,
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"register": 34, "value": 33},
            "instruction_id": 41,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 34},
            "instruction_id": 42,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 43,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 35, "value": "0x44"},
            "instruction_id": 44,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 35, "value": "arg"},
            "instruction_id": 45,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 36, "value": "0x48"},
            "instruction_id": 46,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 36, "value": "arg"},
            "instruction_id": 47,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 37, "value": "0x4c"},
            "instruction_id": 48,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 38, "lhs_register": 37, "rhs_register": "zero"},
            "instruction_id": 49,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 39, "value": 1},
            "instruction_id": 50,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 38, "value": 39},
            "instruction_id": 51,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 41, "value": "0x50"},
            "instruction_id": 52,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 42, "lhs_register": 41, "rhs_register": "zero"},
            "instruction_id": 53,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 43, "value": 2.0},
            "instruction_id": 54,
        },
        {
            "instruction": "STOREF",
            "metadata": {"register": 42, "value": 43},
            "instruction_id": 55,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 45, "value": "0x58"},
            "instruction_id": 56,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 46, "lhs_register": 45, "rhs_register": "zero"},
            "instruction_id": 57,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 47, "value": 0},
            "instruction_id": 58,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 48, "value": 0},
            "instruction_id": 59,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 49, "lhs_register": 46, "rhs_register": 48},
            "instruction_id": 60,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 50, "value": 1},
            "instruction_id": 61,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 49, "value": 50},
            "instruction_id": 62,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 52, "value": "0x4c"},
            "instruction_id": 63,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 53, "lhs_register": 52, "rhs_register": "zero"},
            "instruction_id": 64,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 54, "value": "0x4c"},
            "instruction_id": 65,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 55, "lhs_register": 54, "rhs_register": "zero"},
            "instruction_id": 66,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 56, "value": 55},
            "instruction_id": 67,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 57, "value": "0x50"},
            "instruction_id": 68,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 58, "lhs_register": 57, "rhs_register": "zero"},
            "instruction_id": 69,
        },
        {
            "instruction": "LOADF",
            "metadata": {"register": 59, "value": 58},
            "instruction_id": 70,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 59},
            "instruction_id": 71,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 60, "value": 123},
            "instruction_id": 72,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 60},
            "instruction_id": 73,
        },
        {"instruction": "JAL", "metadata": {"value": 2}, "instruction_id": 74},
        {
            "instruction": "MOV",
            "metadata": {"register": 61, "value": "ret_value"},
            "instruction_id": 75,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 62, "lhs_register": 56, "rhs_register": 61},
            "instruction_id": 76,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 53, "value": 62},
            "instruction_id": 77,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 64, "value": "0x50"},
            "instruction_id": 78,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 65, "lhs_register": 64, "rhs_register": "zero"},
            "instruction_id": 79,
        },
        {
            "instruction": "LOADF",
            "metadata": {"register": 66, "value": 65},
            "instruction_id": 80,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 67, "value": "0x4c"},
            "instruction_id": 81,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 68, "lhs_register": 67, "rhs_register": "zero"},
            "instruction_id": 82,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 69, "value": 68},
            "instruction_id": 83,
        },
        {
            "instruction": "SITOFP",
            "metadata": {"register": 70, "value": 69},
            "instruction_id": 84,
        },
        {
            "instruction": "FADD",
            "metadata": {"register": 71, "lhs_register": 66, "rhs_register": 70},
            "instruction_id": 85,
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"register": 72, "value": 71},
            "instruction_id": 86,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 72},
            "instruction_id": 87,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 88,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 73, "value": "0x60"},
            "instruction_id": 89,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 74, "lhs_register": 73, "rhs_register": "zero"},
            "instruction_id": 90,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 75, "value": 1},
            "instruction_id": 91,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 75},
            "instruction_id": 92,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 76, "value": 2},
            "instruction_id": 93,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 76},
            "instruction_id": 94,
        },
        {"instruction": "JAL", "metadata": {"value": 3}, "instruction_id": 95},
        {
            "instruction": "MOV",
            "metadata": {"register": 77, "value": "ret_value"},
            "instruction_id": 96,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 74, "value": 77},
            "instruction_id": 97,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 79, "value": "0x64"},
            "instruction_id": 98,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 80, "lhs_register": 79, "rhs_register": "zero"},
            "instruction_id": 99,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 81, "value": 5},
            "instruction_id": 100,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 82, "value": 4},
            "instruction_id": 101,
        },
        {
            "instruction": "MULT",
            "metadata": {"register": 83, "lhs_register": 81, "rhs_register": 82},
            "instruction_id": 102,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 84, "lhs_register": 80, "rhs_register": 83},
            "instruction_id": 103,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 85, "value": 1},
            "instruction_id": 104,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 84, "value": 85},
            "instruction_id": 105,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 87, "value": "0x60"},
            "instruction_id": 106,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 88, "lhs_register": 87, "rhs_register": "zero"},
            "instruction_id": 107,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 89, "value": 88},
            "instruction_id": 108,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 90, "value": 4},
            "instruction_id": 109,
        },
        {
            "instruction": "LSHIFT",
            "metadata": {"register": 91, "lhs_register": 89, "rhs_register": 90},
            "instruction_id": 110,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 92, "value": 1},
            "instruction_id": 111,
        },
        {
            "instruction": "EQ",
            "metadata": {"register": 93, "lhs_register": 91, "rhs_register": 92},
            "instruction_id": 112,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 94, "value": "0x60"},
            "instruction_id": 113,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 95, "lhs_register": 94, "rhs_register": "zero"},
            "instruction_id": 114,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 96, "value": 95},
            "instruction_id": 115,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 97, "value": 1},
            "instruction_id": 116,
        },
        {
            "instruction": "GT",
            "metadata": {"register": 98, "lhs_register": 96, "rhs_register": 97},
            "instruction_id": 117,
        },
        {
            "instruction": "OR",
            "metadata": {"register": 99, "lhs_register": 93, "rhs_register": 98},
            "instruction_id": 118,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 100, "value": "0x60"},
            "instruction_id": 119,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 101, "lhs_register": 100, "rhs_register": "zero"},
            "instruction_id": 120,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 102, "value": 101},
            "instruction_id": 121,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 103, "value": 10},
            "instruction_id": 122,
        },
        {
            "instruction": "LT",
            "metadata": {"register": 104, "lhs_register": 102, "rhs_register": 103},
            "instruction_id": 123,
        },
        {
            "instruction": "AND",
            "metadata": {"register": 105, "lhs_register": 99, "rhs_register": 104},
            "instruction_id": 124,
        },
        {
            "instruction": "JZ",
            "metadata": {"conditional_register": 105, "jump_size": 10},
            "instruction_id": 125,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 106, "value": "0x8c"},
            "instruction_id": 126,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 107, "lhs_register": 106, "rhs_register": "zero"},
            "instruction_id": 127,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 108, "value": "0x60"},
            "instruction_id": 128,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 109, "lhs_register": 108, "rhs_register": "zero"},
            "instruction_id": 129,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 110, "value": 109},
            "instruction_id": 130,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 111, "value": 1},
            "instruction_id": 131,
        },
        {
            "instruction": "BITAND",
            "metadata": {"register": 112, "lhs_register": 110, "rhs_register": 111},
            "instruction_id": 132,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 107, "value": 112},
            "instruction_id": 133,
        },
        {
            "instruction": "JZ",
            "metadata": {"conditional_register": "zero", "jump_size": 9},
            "instruction_id": 134,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 114, "value": "0x8c"},
            "instruction_id": 135,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 115, "lhs_register": 114, "rhs_register": "zero"},
            "instruction_id": 136,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 116, "value": "0x60"},
            "instruction_id": 137,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 117, "lhs_register": 116, "rhs_register": "zero"},
            "instruction_id": 138,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 118, "value": 117},
            "instruction_id": 139,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 119, "value": 1},
            "instruction_id": 140,
        },
        {
            "instruction": "BITOR",
            "metadata": {"register": 120, "lhs_register": 118, "rhs_register": 119},
            "instruction_id": 141,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 115, "value": 120},
            "instruction_id": 142,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 122, "value": "0x60"},
            "instruction_id": 143,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 123, "lhs_register": 122, "rhs_register": "zero"},
            "instruction_id": 144,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 124, "value": 123},
            "instruction_id": 145,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 125, "value": "0x8c"},
            "instruction_id": 146,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 126, "lhs_register": 125, "rhs_register": "zero"},
            "instruction_id": 147,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 127, "value": 126},
            "instruction_id": 148,
        },
        {
            "instruction": "MULT",
            "metadata": {"register": 128, "lhs_register": 124, "rhs_register": 127},
            "instruction_id": 149,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 129, "value": 2},
            "instruction_id": 150,
        },
        {
            "instruction": "DIV",
            "metadata": {"register": 130, "lhs_register": 128, "rhs_register": 129},
            "instruction_id": 151,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 131, "value": 1},
            "instruction_id": 152,
        },
        {
            "instruction": "RSHIFT",
            "metadata": {"register": 132, "lhs_register": 130, "rhs_register": 131},
            "instruction_id": 153,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 132},
            "instruction_id": 154,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 155,
        },
        {"instruction": "HALT", "metadata": {}, "instruction_id": 156},
    ],
}

CERTIFICATE = [
    "2^((3)^(2)^(40))",
    "3^((3)^(3)^(8))",
    "5^((11)^(5)^(4))",
    "7^((11)^(7)^(4))",
    "11^((3)^(11)^(4))",
    "29^(37)*13^((7)^(11)^(2)^(1))*23^(43)*17^((5)^(5)^(2)^(1))*19^((5)^(7)^(2)^(1))",
    "41^(37)*31^((7)^(3)^(2)^(1))*37^((5)^(11)^(2)^(1))",
    "47^(19)*43^((5)^(3)^(2)^(1))",
    "53^((11)^(13)^(4))",
    "59^((11)^(17)^(4))",
    "73^(19)*71^(59)*61^((5)^(13)^(2)^(1))*67^((5)^(17)^(2)^(1))",
    "79^((11)^(19)^(4))",
    "83^((11)^(23)^(4))",
    "89^((3)^(29)^(4))",
    "103^(37)*97^((7)^(29)^(2)^(1))*101^((2)^(2))",
    "107^((3)^(31)^(4))",
    "127^(37)*109^((7)^(31)^(2)^(1))*113^((2)^(3.0))",
    "131^((3)^(37)^(2))",
    "137^((3)^(41)^(8))",
    "151^(37)*139^((7)^(41)^(2)^(1))*149^((2)^(2))",
    "197^(37)*157^((7)^(29)^(2)^(1))*193^(43)*163^((5)^(29)^(2)^(1))*191^((17)^(3))*173^(13)*167^((5)^(31)^(2)^(1))*181^(13)*179^((2)^(124))",
    "227^(19)*223^(43)*199^((5)^(31)^(2)^(1))*211^((5)^(29)^(2)^(1))",
    "229^((3)^(43)^(4))",
    "269^(37)*233^((7)^(43)^(2)^(1))*263^((17)^(5))*241^(13)*239^((2)^(2))*257^(13)*251^((2)^(3))",
    "271^((3)^(47)^(40))",
    "283^(37)*277^((7)^(47)^(2)^(21))*281^((2)^(2))",
    "293^((3)^(53)^(4))",
    "379^(83)*353^(89)*331^(73)*313^(97)*307^((5)^(43)^(2)^(1))*311^((2)^(5))*317^((2)^(2))*349^(71)*337^((5)^(43)^(2)^(1))*347^((2)^(2))*373^(67)*359^((5)^(43)^(2)^(1))*367^((2)^(11))",
    "383^(29)",
    "419^(37)*389^((7)^(53)^(2)^(1))*409^(103)*397^((5)^(43)^(2)^(1))*401^((2)^(2))",
    "443^(37)*421^((7)^(53)^(2)^(1))*439^(107)*431^((5)^(43)^(2)^(1))*433^((2)^(2))",
    "491^(19)*487^(101)*467^(59)*461^(53)*449^((5)^(43)^(2)^(1))*457^((5)^(53)^(2)^(1))*463^((2)^(3))*479^((2)^(2))",
    "499^(109)",
]
