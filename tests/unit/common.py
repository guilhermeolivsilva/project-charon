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
            "global_var": {
                "type": "my_struct",
                "attributes": {
                    "x": {"type": "int", "attr_pointer": 0},
                    "y": {"type": "float", "attr_pointer": 1},
                },
                "relative_position": 2,
                "prime": 3,
            },
        },
    },
    "functions": {
        "function_that_returns_struct": {
            "relative_position": 1,
            "prime": 2,
            "type": "my_struct",
            "parameters": {
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
                (
                    "VAR",
                    {
                        "type": "my_struct",
                        "attributes": {
                            "x": {"type": "int", "attr_pointer": 0},
                            "y": {"type": "float", "attr_pointer": 1},
                        },
                        "relative_position": 2,
                        "prime": 3,
                    },
                ),
                ("SEMI", {}),
                ("RCBRA", {}),
            ],
        },
        "some_simple_function": {
            "relative_position": 2,
            "prime": 3,
            "type": "int",
            "parameters": {
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
            "parameters": {
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
                        "arguments": [
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
            "parameters": {},
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
                        "arguments": [
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
ABSTRACT_SYNTAX_TREE = AbstractSyntaxTree(source_code=_source)
ABSTRACT_SYNTAX_TREE_ROOT = ABSTRACT_SYNTAX_TREE.build()

MACHINE_CODE = {
    "structs": {"my_struct": ["int", "float"]},
    "functions": {
        "function_that_returns_struct": {"start": 0, "end": 17},
        "some_simple_function": {"start": 17, "end": 27},
        "abc": {"start": 27, "end": 62},
        "main": {"start": 62, "end": 111},
    },
    "global_vars": [
        {
            "instruction": "ALLOC",
            "metadata": {"id": 3, "relative_position": 1, "size": 40, "register": 0},
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 4, "relative_position": 2, "size": 8, "register": 1},
        },
    ],
    "code": [
        {
            "instruction": "ALLOC",
            "metadata": {"id": None, "relative_position": 3, "size": 4, "register": 2},
        },
        {
            "instruction": "STORE",
            "metadata": {"lhs_register": 2, "rhs_register": "arg", "type": "int"},
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": None, "relative_position": 4, "size": 4, "register": 3},
        },
        {
            "instruction": "STORE",
            "metadata": {"lhs_register": 3, "rhs_register": "arg", "type": "int"},
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 8, "relative_position": 5, "size": 4, "register": 4},
        },
        {
            "instruction": "ADDRESS",
            "metadata": {
                "id": 12,
                "register": 5,
                "value": 5,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 14,
                "register": 6,
                "value": 3,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 16,
                "register": 7,
                "value": 4,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "ADD",
            "metadata": {"id": 15, "register": 8, "lhs_register": 6, "rhs_register": 7},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 13, "lhs_register": 5, "rhs_register": 8},
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 18,
                "register": 9,
                "value": 2,
                "type": "my_struct",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 20, "register": 10, "value": 0, "type": "int"},
        },
        {
            "instruction": "ADDRESS",
            "metadata": {
                "id": 19,
                "register": 11,
                "value": 2,
                "type": "int",
                "offset_register": -1,
                "offset_size": 0,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 22,
                "register": 12,
                "value": 5,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 21, "lhs_register": 11, "rhs_register": 12},
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 25,
                "register": 13,
                "value": 2,
                "type": "my_struct",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "RET",
            "metadata": {"id": 24, "type": "my_struct", "register": 13},
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": None, "relative_position": 6, "size": 4, "register": 14},
        },
        {
            "instruction": "STORE",
            "metadata": {"lhs_register": 14, "rhs_register": "arg", "type": "float"},
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": None, "relative_position": 7, "size": 4, "register": 15},
        },
        {
            "instruction": "STORE",
            "metadata": {"lhs_register": 15, "rhs_register": "arg", "type": "int"},
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 30,
                "register": 16,
                "value": 6,
                "type": "float",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 32,
                "register": 17,
                "value": 7,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "SITOFP",
            "metadata": {"source_register": 17, "destination_register": 18},
        },
        {
            "instruction": "FDIV",
            "metadata": {
                "id": 31,
                "register": 19,
                "lhs_register": 16,
                "rhs_register": 18,
            },
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"source_register": 19, "destination_register": 20},
        },
        {"instruction": "RET", "metadata": {"id": 29, "type": "int", "register": 20}},
        {
            "instruction": "ALLOC",
            "metadata": {"id": None, "relative_position": 8, "size": 4, "register": 21},
        },
        {
            "instruction": "STORE",
            "metadata": {"lhs_register": 21, "rhs_register": "arg", "type": "int"},
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": None, "relative_position": 9, "size": 4, "register": 22},
        },
        {
            "instruction": "STORE",
            "metadata": {"lhs_register": 22, "rhs_register": "arg", "type": "int"},
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 36, "relative_position": 10, "size": 4, "register": 23},
        },
        {
            "instruction": "ADDRESS",
            "metadata": {
                "id": 40,
                "register": 24,
                "value": 10,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 42, "register": 25, "value": 1, "type": "int"},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 41, "lhs_register": 24, "rhs_register": 25},
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 44, "relative_position": 11, "size": 4, "register": 26},
        },
        {
            "instruction": "ADDRESS",
            "metadata": {
                "id": 48,
                "register": 27,
                "value": 11,
                "type": "float",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 50, "register": 28, "value": 2.0, "type": "float"},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 49, "lhs_register": 27, "rhs_register": 28},
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 52, "relative_position": 12, "size": 2, "register": 29},
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 56, "relative_position": 13, "size": 8, "register": 30},
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 60,
                "register": 31,
                "value": 13,
                "type": "my_struct",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 62, "register": 32, "value": 0, "type": "int"},
        },
        {
            "instruction": "ADDRESS",
            "metadata": {
                "id": 61,
                "register": 33,
                "value": 13,
                "type": "int",
                "offset_register": -1,
                "offset_size": 0,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 64, "register": 34, "value": 1, "type": "int"},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 63, "lhs_register": 33, "rhs_register": 34},
        },
        {
            "instruction": "ADDRESS",
            "metadata": {
                "id": 66,
                "register": 35,
                "value": 10,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 68,
                "register": 36,
                "value": 10,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 71,
                "register": 37,
                "value": 11,
                "type": "float",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "MOV",
            "metadata": {"lhs_register": "arg", "rhs_register": 37, "type": None},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 72, "register": 38, "value": 123, "type": "int"},
        },
        {
            "instruction": "MOV",
            "metadata": {"lhs_register": "arg", "rhs_register": 38, "type": None},
        },
        {"instruction": "JAL", "metadata": {"value": 2}},
        {
            "instruction": "MOV",
            "metadata": {
                "lhs_register": 39,
                "rhs_register": "ret_value",
                "type": "int",
            },
        },
        {
            "instruction": "ADD",
            "metadata": {
                "id": 69,
                "register": 40,
                "lhs_register": 36,
                "rhs_register": 39,
            },
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 67, "lhs_register": 35, "rhs_register": 40},
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 73,
                "register": 41,
                "value": 11,
                "type": "float",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 75,
                "register": 42,
                "value": 10,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "SITOFP",
            "metadata": {"source_register": 42, "destination_register": 43},
        },
        {
            "instruction": "FADD",
            "metadata": {
                "id": 74,
                "register": 44,
                "lhs_register": 41,
                "rhs_register": 43,
            },
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"source_register": 44, "destination_register": 45},
        },
        {"instruction": "RET", "metadata": {"id": 72, "type": "int", "register": 45}},
        {
            "instruction": "ALLOC",
            "metadata": {"id": 79, "relative_position": 14, "size": 4, "register": 46},
        },
        {
            "instruction": "ADDRESS",
            "metadata": {
                "id": 83,
                "register": 47,
                "value": 14,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 86, "register": 48, "value": 1, "type": "int"},
        },
        {
            "instruction": "MOV",
            "metadata": {"lhs_register": "arg", "rhs_register": 48, "type": None},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 87, "register": 49, "value": 2, "type": "int"},
        },
        {
            "instruction": "MOV",
            "metadata": {"lhs_register": "arg", "rhs_register": 49, "type": None},
        },
        {"instruction": "JAL", "metadata": {"value": 3}},
        {
            "instruction": "MOV",
            "metadata": {
                "lhs_register": 50,
                "rhs_register": "ret_value",
                "type": "int",
            },
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 84, "lhs_register": 47, "rhs_register": 50},
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 87, "relative_position": 15, "size": 40, "register": 51},
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 91,
                "register": 52,
                "value": 15,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 93, "register": 53, "value": 5, "type": "int"},
        },
        {
            "instruction": "ADDRESS",
            "metadata": {
                "id": 92,
                "register": 54,
                "value": 15,
                "type": "int",
                "offset_register": -1,
                "offset_size": 20,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 95, "register": 55, "value": 1, "type": "int"},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 94, "lhs_register": 54, "rhs_register": 55},
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 97, "relative_position": 16, "size": 4, "register": 56},
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 102,
                "register": 57,
                "value": 14,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 104, "register": 58, "value": 4, "type": "int"},
        },
        {
            "instruction": "LSHIFT",
            "metadata": {
                "id": 103,
                "register": 59,
                "lhs_register": 57,
                "rhs_register": 58,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 106, "register": 60, "value": 1, "type": "int"},
        },
        {
            "instruction": "EQ",
            "metadata": {
                "id": 105,
                "register": 61,
                "lhs_register": 59,
                "rhs_register": 60,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 108,
                "register": 62,
                "value": 14,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 110, "register": 63, "value": 1, "type": "int"},
        },
        {
            "instruction": "GT",
            "metadata": {
                "id": 109,
                "register": 64,
                "lhs_register": 62,
                "rhs_register": 63,
            },
        },
        {
            "instruction": "OR",
            "metadata": {
                "id": 107,
                "register": 65,
                "lhs_register": 61,
                "rhs_register": 64,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 112,
                "register": 66,
                "value": 14,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 114, "register": 67, "value": 10, "type": "int"},
        },
        {
            "instruction": "LT",
            "metadata": {
                "id": 113,
                "register": 68,
                "lhs_register": 66,
                "rhs_register": 67,
            },
        },
        {
            "instruction": "AND",
            "metadata": {
                "id": 111,
                "register": 69,
                "lhs_register": 65,
                "rhs_register": 68,
            },
        },
        {"instruction": "JZ", "metadata": {"conditional_register": 69, "jump_size": 7}},
        {
            "instruction": "ADDRESS",
            "metadata": {
                "id": 117,
                "register": 70,
                "value": 16,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 119,
                "register": 71,
                "value": 14,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 121, "register": 72, "value": 1, "type": "int"},
        },
        {
            "instruction": "BITAND",
            "metadata": {
                "id": 120,
                "register": 73,
                "lhs_register": 71,
                "rhs_register": 72,
            },
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 118, "lhs_register": 70, "rhs_register": 73},
        },
        {"instruction": "JMP", "metadata": {"jump_size": 6}},
        {
            "instruction": "ADDRESS",
            "metadata": {
                "id": 124,
                "register": 74,
                "value": 16,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 126,
                "register": 75,
                "value": 14,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 128, "register": 76, "value": 1, "type": "int"},
        },
        {
            "instruction": "BITOR",
            "metadata": {
                "id": 127,
                "register": 77,
                "lhs_register": 75,
                "rhs_register": 76,
            },
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 125, "lhs_register": 74, "rhs_register": 77},
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 131,
                "register": 78,
                "value": 14,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {
                "id": 133,
                "register": 79,
                "value": 16,
                "type": "int",
                "offset_size": -1,
                "offset_register": -1,
            },
        },
        {
            "instruction": "MULT",
            "metadata": {
                "id": 132,
                "register": 80,
                "lhs_register": 78,
                "rhs_register": 79,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 135, "register": 81, "value": 2, "type": "int"},
        },
        {
            "instruction": "DIV",
            "metadata": {
                "id": 134,
                "register": 82,
                "lhs_register": 80,
                "rhs_register": 81,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 137, "register": 83, "value": 1, "type": "int"},
        },
        {
            "instruction": "RSHIFT",
            "metadata": {
                "id": 136,
                "register": 84,
                "lhs_register": 82,
                "rhs_register": 83,
            },
        },
        {"instruction": "RET", "metadata": {"id": 130, "type": "int", "register": 84}},
        {"instruction": "HALT", "metadata": {}},
    ],
}
