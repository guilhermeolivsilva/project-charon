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
                "relative_position": 1,
                "prime": 2,
                "attributes": {
                    "x": {"type": "int", "attr_pointer": 0},
                    "y": {"type": "float", "attr_pointer": 1},
                },
                "active": True,
            },
            "test_struct": {
                "relative_position": 2,
                "prime": 3,
                "attributes": {
                    "abcd": {"type": "int", "attr_pointer": 0},
                    "xyz": {"type": "int", "attr_pointer": 1},
                },
                "active": False,
            },
        },
        "variables": {
            "a": {"type": "int", "length": 10, "relative_position": 1, "prime": 2},
            "global_var": {"type": "my_struct", "relative_position": 2, "prime": 3},
        },
    },
    "functions": {
        "function_that_returns_struct": {
            "relative_position": 1,
            "prime": 2,
            "type": "my_struct",
            "arguments": {
                "xyz": {"type": "int", "relative_position": 3, "prime": 5},
                "aaa": {"type": "int", "relative_position": 4, "prime": 7},
            },
            "statements": [
                ("LCBRA", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "internal_guy",
                        "relative_position": 5,
                        "prime": 11,
                        "type": "int",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "name": "internal_guy",
                        "relative_position": 5,
                        "prime": 11,
                        "type": "int",
                    },
                ),
                ("ASSIGN", {}),
                ("VAR", {"type": "int", "relative_position": 3, "prime": 5}),
                ("ADD", {}),
                ("VAR", {"type": "int", "relative_position": 4, "prime": 7}),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "relative_position": 2,
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
                        "relative_position": 5,
                        "prime": 11,
                        "type": "int",
                    },
                ),
                ("SEMI", {}),
                ("RET_SYM", {}),
                ("VAR", {"type": "my_struct", "relative_position": 2, "prime": 3}),
                ("SEMI", {}),
                ("RCBRA", {}),
            ],
        },
        "some_simple_function": {
            "relative_position": 2,
            "prime": 3,
            "type": "int",
            "arguments": {
                "param_1": {"type": "float", "relative_position": 6, "prime": 13},
                "param_2": {"type": "int", "relative_position": 7, "prime": 17},
            },
            "statements": [
                ("LCBRA", {}),
                ("RET_SYM", {}),
                ("VAR", {"type": "float", "relative_position": 6, "prime": 13}),
                ("DIV", {}),
                ("VAR", {"type": "int", "relative_position": 7, "prime": 17}),
                ("SEMI", {}),
                ("RCBRA", {}),
            ],
        },
        "abc": {
            "relative_position": 3,
            "prime": 5,
            "type": "int",
            "arguments": {
                "asda": {"type": "int", "relative_position": 8, "prime": 19},
                "abcdef": {"type": "int", "relative_position": 9, "prime": 23},
            },
            "statements": [
                ("LCBRA", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "bla",
                        "relative_position": 10,
                        "prime": 29,
                        "type": "int",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "name": "bla",
                        "relative_position": 10,
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
                        "relative_position": 11,
                        "prime": 31,
                        "type": "float",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "name": "blabla",
                        "relative_position": 11,
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
                        "relative_position": 12,
                        "prime": 37,
                        "type": "short",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "internal_struct_var",
                        "relative_position": 13,
                        "prime": 41,
                        "type": "my_struct",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "relative_position": 13,
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
                        "relative_position": 10,
                        "prime": 29,
                        "type": "int",
                    },
                ),
                ("ASSIGN", {}),
                (
                    "VAR",
                    {
                        "name": "bla",
                        "relative_position": 10,
                        "prime": 29,
                        "type": "int",
                    },
                ),
                ("ADD", {}),
                (
                    "FUNC_CALL",
                    {
                        "function": 2,
                        "prime": 3,
                        "return_type": "int",
                        "parameters": [
                            {
                                "variable": True,
                                "name": "blabla",
                                "relative_position": 11,
                                "prime": 31,
                                "type": "float",
                            },
                            {"variable": False, "type": "int", "value": 123},
                        ],
                    },
                ),
                ("SEMI", {}),
                ("RET_SYM", {}),
                (
                    "VAR",
                    {
                        "name": "blabla",
                        "relative_position": 11,
                        "prime": 31,
                        "type": "float",
                    },
                ),
                ("ADD", {}),
                (
                    "VAR",
                    {
                        "name": "bla",
                        "relative_position": 10,
                        "prime": 29,
                        "type": "int",
                    },
                ),
                ("SEMI", {}),
                ("RCBRA", {}),
            ],
        },
        "main": {
            "relative_position": 4,
            "prime": 7,
            "type": "int",
            "arguments": {},
            "statements": [
                ("LCBRA", {}),
                (
                    "VAR_DEF",
                    {"name": "x", "relative_position": 14, "prime": 43, "type": "int"},
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {"name": "x", "relative_position": 14, "prime": 43, "type": "int"},
                ),
                ("ASSIGN", {}),
                (
                    "FUNC_CALL",
                    {
                        "function": 3,
                        "prime": 5,
                        "return_type": "int",
                        "parameters": [
                            {"variable": False, "type": "int", "value": 1},
                            {"variable": False, "type": "int", "value": 2},
                        ],
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "array",
                        "relative_position": 15,
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
                        "relative_position": 15,
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
                    {"name": "y", "relative_position": 16, "prime": 53, "type": "int"},
                ),
                ("SEMI", {}),
                ("IF_SYM", {}),
                ("LPAR", {}),
                ("LPAR", {}),
                ("LPAR", {}),
                ("LPAR", {}),
                (
                    "VAR",
                    {"name": "x", "relative_position": 14, "prime": 43, "type": "int"},
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
                    {"name": "x", "relative_position": 14, "prime": 43, "type": "int"},
                ),
                ("GREATER", {}),
                ("CST", {"type": "int", "value": 1}),
                ("RPAR", {}),
                ("RPAR", {}),
                ("AND", {}),
                ("LPAR", {}),
                (
                    "VAR",
                    {"name": "x", "relative_position": 14, "prime": 43, "type": "int"},
                ),
                ("LESS", {}),
                ("CST", {"type": "int", "value": 10}),
                ("RPAR", {}),
                ("RPAR", {}),
                ("LCBRA", {}),
                (
                    "VAR",
                    {"name": "y", "relative_position": 16, "prime": 53, "type": "int"},
                ),
                ("ASSIGN", {}),
                (
                    "VAR",
                    {"name": "x", "relative_position": 14, "prime": 43, "type": "int"},
                ),
                ("BITAND", {}),
                ("CST", {"type": "int", "value": 1}),
                ("SEMI", {}),
                ("RCBRA", {}),
                ("ELSE_SYM", {}),
                ("LCBRA", {}),
                (
                    "VAR",
                    {"name": "y", "relative_position": 16, "prime": 53, "type": "int"},
                ),
                ("ASSIGN", {}),
                (
                    "VAR",
                    {"name": "x", "relative_position": 14, "prime": 43, "type": "int"},
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
                    {"name": "x", "relative_position": 14, "prime": 43, "type": "int"},
                ),
                ("MULT", {}),
                (
                    "VAR",
                    {"name": "y", "relative_position": 16, "prime": 53, "type": "int"},
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
ast = AbstractSyntaxTree(source_code=_source)
ABSTRACT_SYNTAX_TREE_ROOT = ast.build()

MACHINE_CODE = {
    "structs": {"my_struct": ["int", "float"]},
    "functions": {
        "function_that_returns_struct": {"start": 0, "end": 15},
        "some_simple_function": {"start": 15, "end": 23},
        "abc": {"start": 23, "end": 53},
        "main": {"start": 53, "end": 99},
    },
    "global_vars": [
        {
            "instruction": "ALLOC",
            "metadata": {"id": 3, "type": "int", "relative_position": 1, "length": 10},
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "id": 4,
                "type": "my_struct",
                "relative_position": 2,
                "length": 1,
            },
        },
    ],
    "code": [
        {
            "instruction": "PARAM",
            "metadata": {
                "id": None,
                "type": "int",
                "relative_position": 3,
                "length": 1,
            },
        },
        {
            "instruction": "PARAM",
            "metadata": {
                "id": None,
                "type": "int",
                "relative_position": 4,
                "length": 1,
            },
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 8, "type": "int", "relative_position": 5, "length": 1},
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"id": 12, "register": 0, "value": 5, "type": "int"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 14, "register": 1, "value": 3, "type": "int"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 16, "register": 2, "value": 4, "type": "int"},
        },
        {
            "instruction": "ADD",
            "metadata": {"id": 15, "register": 3, "lhs_register": 1, "rhs_register": 2},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 13, "lhs_register": 0, "rhs_register": 3},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 18, "register": 4, "value": 2, "type": "my_struct"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 20, "register": 5, "value": 0, "type": "int"},
        },
        {
            "instruction": "ELEMENT_ADDRESS",
            "metadata": {
                "id": 19,
                "register": 6,
                "variable_relative_position": 2,
                "offset_size": 0,
                "offset_mode": "static",
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 22, "register": 7, "value": 5, "type": "int"},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 21, "lhs_register": 6, "rhs_register": 7},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 25, "register": 8, "value": 2, "type": "my_struct"},
        },
        {
            "instruction": "RET",
            "metadata": {"id": 24, "type": "my_struct", "register": 8},
        },
        {
            "instruction": "PARAM",
            "metadata": {
                "id": None,
                "type": "float",
                "relative_position": 6,
                "length": 1,
            },
        },
        {
            "instruction": "PARAM",
            "metadata": {
                "id": None,
                "type": "int",
                "relative_position": 7,
                "length": 1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 30, "register": 9, "value": 6, "type": "float"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 32, "register": 10, "value": 7, "type": "int"},
        },
        {
            "instruction": "SITOFP",
            "metadata": {"source_register": 10, "destination_register": 11},
        },
        {
            "instruction": "FDIV",
            "metadata": {
                "id": 31,
                "register": 12,
                "lhs_register": 9,
                "rhs_register": 11,
            },
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"source_register": 12, "destination_register": 13},
        },
        {"instruction": "RET", "metadata": {"id": 29, "type": "int", "register": 13}},
        {
            "instruction": "PARAM",
            "metadata": {
                "id": None,
                "type": "int",
                "relative_position": 8,
                "length": 1,
            },
        },
        {
            "instruction": "PARAM",
            "metadata": {
                "id": None,
                "type": "int",
                "relative_position": 9,
                "length": 1,
            },
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 36, "type": "int", "relative_position": 10, "length": 1},
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"id": 40, "register": 14, "value": 10, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 42, "register": 15, "value": 1, "type": "int"},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 41, "lhs_register": 14, "rhs_register": 15},
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "id": 44,
                "type": "float",
                "relative_position": 11,
                "length": 1,
            },
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"id": 48, "register": 16, "value": 11, "type": "float"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 50, "register": 17, "value": 2.0, "type": "float"},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 49, "lhs_register": 16, "rhs_register": 17},
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "id": 52,
                "type": "short",
                "relative_position": 12,
                "length": 1,
            },
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "id": 56,
                "type": "my_struct",
                "relative_position": 13,
                "length": 1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 60, "register": 18, "value": 13, "type": "my_struct"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 62, "register": 19, "value": 0, "type": "int"},
        },
        {
            "instruction": "ELEMENT_ADDRESS",
            "metadata": {
                "id": 61,
                "register": 20,
                "variable_relative_position": 13,
                "offset_size": 0,
                "offset_mode": "static",
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 64, "register": 21, "value": 1, "type": "int"},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 63, "lhs_register": 20, "rhs_register": 21},
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"id": 66, "register": 22, "value": 10, "type": "int"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 68, "register": 23, "value": 10, "type": "int"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 71, "register": 24, "value": 11, "type": "float"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 72, "register": 25, "value": 123, "type": "int"},
        },
        {
            "instruction": "CALL",
            "metadata": {
                "id": 70,
                "register": 26,
                "value": 2,
                "type": "int",
                "parameters_registers": [24, 25],
            },
        },
        {
            "instruction": "ADD",
            "metadata": {
                "id": 69,
                "register": 27,
                "lhs_register": 23,
                "rhs_register": 26,
            },
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 67, "lhs_register": 22, "rhs_register": 27},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 73, "register": 28, "value": 11, "type": "float"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 75, "register": 29, "value": 10, "type": "int"},
        },
        {
            "instruction": "SITOFP",
            "metadata": {"source_register": 29, "destination_register": 30},
        },
        {
            "instruction": "FADD",
            "metadata": {
                "id": 74,
                "register": 31,
                "lhs_register": 28,
                "rhs_register": 30,
            },
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"source_register": 31, "destination_register": 32},
        },
        {"instruction": "RET", "metadata": {"id": 72, "type": "int", "register": 32}},
        {
            "instruction": "ALLOC",
            "metadata": {"id": 79, "type": "int", "relative_position": 14, "length": 1},
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"id": 83, "register": 33, "value": 14, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 86, "register": 34, "value": 1, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 87, "register": 35, "value": 2, "type": "int"},
        },
        {
            "instruction": "CALL",
            "metadata": {
                "id": 85,
                "register": 36,
                "value": 3,
                "type": "int",
                "parameters_registers": [34, 35],
            },
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 84, "lhs_register": 33, "rhs_register": 36},
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "id": 87,
                "type": "int",
                "relative_position": 15,
                "length": 10,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 91, "register": 37, "value": 15, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 93, "register": 38, "value": 5, "type": "int"},
        },
        {
            "instruction": "ELEMENT_ADDRESS",
            "metadata": {
                "id": 92,
                "register": 39,
                "variable_relative_position": 15,
                "offset_size": 20,
                "offset_mode": "static",
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 95, "register": 40, "value": 1, "type": "int"},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 94, "lhs_register": 39, "rhs_register": 40},
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 97, "type": "int", "relative_position": 16, "length": 1},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 102, "register": 41, "value": 14, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 104, "register": 42, "value": 4, "type": "int"},
        },
        {
            "instruction": "LSHIFT",
            "metadata": {
                "id": 103,
                "register": 43,
                "lhs_register": 41,
                "rhs_register": 42,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 106, "register": 44, "value": 1, "type": "int"},
        },
        {
            "instruction": "EQ",
            "metadata": {
                "id": 105,
                "register": 45,
                "lhs_register": 43,
                "rhs_register": 44,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 108, "register": 46, "value": 14, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 110, "register": 47, "value": 1, "type": "int"},
        },
        {
            "instruction": "GT",
            "metadata": {
                "id": 109,
                "register": 48,
                "lhs_register": 46,
                "rhs_register": 47,
            },
        },
        {
            "instruction": "OR",
            "metadata": {
                "id": 107,
                "register": 49,
                "lhs_register": 45,
                "rhs_register": 48,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 112, "register": 50, "value": 14, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 114, "register": 51, "value": 10, "type": "int"},
        },
        {
            "instruction": "LT",
            "metadata": {
                "id": 113,
                "register": 52,
                "lhs_register": 50,
                "rhs_register": 51,
            },
        },
        {
            "instruction": "AND",
            "metadata": {
                "id": 111,
                "register": 53,
                "lhs_register": 49,
                "rhs_register": 52,
            },
        },
        {"instruction": "JZ", "metadata": {"conditional_register": 53, "jump_size": 7}},
        {
            "instruction": "ADDRESS",
            "metadata": {"id": 117, "register": 54, "value": 16, "type": "int"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 119, "register": 55, "value": 14, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 121, "register": 56, "value": 1, "type": "int"},
        },
        {
            "instruction": "BITAND",
            "metadata": {
                "id": 120,
                "register": 57,
                "lhs_register": 55,
                "rhs_register": 56,
            },
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 118, "lhs_register": 54, "rhs_register": 57},
        },
        {"instruction": "JMP", "metadata": {"jump_size": 6}},
        {
            "instruction": "ADDRESS",
            "metadata": {"id": 124, "register": 58, "value": 16, "type": "int"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 126, "register": 59, "value": 14, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 128, "register": 60, "value": 1, "type": "int"},
        },
        {
            "instruction": "BITOR",
            "metadata": {
                "id": 127,
                "register": 61,
                "lhs_register": 59,
                "rhs_register": 60,
            },
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 125, "lhs_register": 58, "rhs_register": 61},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 131, "register": 62, "value": 14, "type": "int"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 133, "register": 63, "value": 16, "type": "int"},
        },
        {
            "instruction": "MULT",
            "metadata": {
                "id": 132,
                "register": 64,
                "lhs_register": 62,
                "rhs_register": 63,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 135, "register": 65, "value": 2, "type": "int"},
        },
        {
            "instruction": "DIV",
            "metadata": {
                "id": 134,
                "register": 66,
                "lhs_register": 64,
                "rhs_register": 65,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 137, "register": 67, "value": 1, "type": "int"},
        },
        {
            "instruction": "RSHIFT",
            "metadata": {
                "id": 136,
                "register": 68,
                "lhs_register": 66,
                "rhs_register": 67,
            },
        },
        {"instruction": "RET", "metadata": {"id": 130, "type": "int", "register": 68}},
        {"instruction": "HALT", "metadata": {}},
    ],
}
