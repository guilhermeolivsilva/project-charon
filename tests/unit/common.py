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

MACHINE_CODE = {
    "structs": {"my_struct": ["int", "float"]},
    "functions": {
        "function_that_returns_struct": {"start": 0, "end": 17},
        "some_simple_function": {"start": 17, "end": 28},
        "abc": {"start": 28, "end": 63},
        "main": {"start": 63, "end": 112},
    },
    "global_vars": [
        {
            "instruction": "ALLOC",
            "metadata": {"id": 1, "size": 40, "register": 0},
            "instruction_id": 1,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 2, "size": 8, "register": 1},
            "instruction_id": 2,
        },
    ],
    "code": [
        {
            "instruction": "ALLOC",
            "metadata": {"id": 3, "size": 4, "register": 2},
            "instruction_id": 3,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 2, "value": "arg"},
            "instruction_id": 4,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 4, "size": 4, "register": 3},
            "instruction_id": 5,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 3, "value": "arg"},
            "instruction_id": 6,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 5, "size": 4, "register": 4},
            "instruction_id": 7,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 5, "value": 5},
            "instruction_id": 8,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 6, "value": 3},
            "instruction_id": 9,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 7, "value": 4},
            "instruction_id": 10,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 8, "lhs_register": 6, "rhs_register": 7},
            "instruction_id": 11,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 5, "value": 8},
            "instruction_id": 12,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 9, "value": 2},
            "instruction_id": 13,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 10, "value": 2, "offset_size": 0},
            "instruction_id": 14,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 11, "value": 5},
            "instruction_id": 15,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 10, "value": 11},
            "instruction_id": 16,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 12, "value": 2},
            "instruction_id": 17,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 12},
            "instruction_id": 18,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 19,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 6, "size": 4, "register": 13},
            "instruction_id": 20,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 13, "value": "arg"},
            "instruction_id": 21,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 7, "size": 4, "register": 14},
            "instruction_id": 22,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 14, "value": "arg"},
            "instruction_id": 23,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 15, "value": 6},
            "instruction_id": 24,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 16, "value": 7},
            "instruction_id": 25,
        },
        {
            "instruction": "SITOFP",
            "metadata": {"source_register": 16, "destination_register": 17},
            "instruction_id": 26,
        },
        {
            "instruction": "FDIV",
            "metadata": {"register": 18, "lhs_register": 15, "rhs_register": 17},
            "instruction_id": 27,
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"source_register": 18, "destination_register": 19},
            "instruction_id": 28,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 19},
            "instruction_id": 29,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 30,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 8, "size": 4, "register": 20},
            "instruction_id": 31,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 20, "value": "arg"},
            "instruction_id": 32,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 9, "size": 4, "register": 21},
            "instruction_id": 33,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 21, "value": "arg"},
            "instruction_id": 34,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 10, "size": 4, "register": 22},
            "instruction_id": 35,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 23, "value": 10},
            "instruction_id": 36,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 24, "value": 1},
            "instruction_id": 37,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 23, "value": 24},
            "instruction_id": 38,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 11, "size": 4, "register": 25},
            "instruction_id": 39,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 26, "value": 11},
            "instruction_id": 40,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 27, "value": 2.0},
            "instruction_id": 41,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 26, "value": 27},
            "instruction_id": 42,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 12, "size": 2, "register": 28},
            "instruction_id": 43,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 13, "size": 8, "register": 29},
            "instruction_id": 44,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 30, "value": 13},
            "instruction_id": 45,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 31, "value": 13, "offset_size": 0},
            "instruction_id": 46,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 32, "value": 1},
            "instruction_id": 47,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 31, "value": 32},
            "instruction_id": 48,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 33, "value": 10},
            "instruction_id": 49,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 34, "value": 10},
            "instruction_id": 50,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 35, "value": 11},
            "instruction_id": 51,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 35},
            "instruction_id": 52,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 36, "value": 123},
            "instruction_id": 53,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 36},
            "instruction_id": 54,
        },
        {"instruction": "JAL", "metadata": {"value": 2}, "instruction_id": 55},
        {
            "instruction": "MOV",
            "metadata": {"register": 37, "value": "ret_value"},
            "instruction_id": 56,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 38, "lhs_register": 34, "rhs_register": 37},
            "instruction_id": 57,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 33, "value": 38},
            "instruction_id": 58,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 39, "value": 11},
            "instruction_id": 59,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 40, "value": 10},
            "instruction_id": 60,
        },
        {
            "instruction": "SITOFP",
            "metadata": {"source_register": 40, "destination_register": 41},
            "instruction_id": 61,
        },
        {
            "instruction": "FADD",
            "metadata": {"register": 42, "lhs_register": 39, "rhs_register": 41},
            "instruction_id": 62,
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"source_register": 42, "destination_register": 43},
            "instruction_id": 63,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 43},
            "instruction_id": 64,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 65,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 14, "size": 4, "register": 44},
            "instruction_id": 66,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 45, "value": 14},
            "instruction_id": 67,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 46, "value": 1},
            "instruction_id": 68,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 46},
            "instruction_id": 69,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 47, "value": 2},
            "instruction_id": 70,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 47},
            "instruction_id": 71,
        },
        {"instruction": "JAL", "metadata": {"value": 3}, "instruction_id": 72},
        {
            "instruction": "MOV",
            "metadata": {"register": 48, "value": "ret_value"},
            "instruction_id": 73,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 45, "value": 48},
            "instruction_id": 74,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 15, "size": 40, "register": 49},
            "instruction_id": 75,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 50, "value": 15},
            "instruction_id": 76,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 51, "value": 15, "offset_size": 20},
            "instruction_id": 77,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 52, "value": 1},
            "instruction_id": 78,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 51, "value": 52},
            "instruction_id": 79,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 16, "size": 4, "register": 53},
            "instruction_id": 80,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 54, "value": 14},
            "instruction_id": 81,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 55, "value": 4},
            "instruction_id": 82,
        },
        {
            "instruction": "LSHIFT",
            "metadata": {"register": 56, "lhs_register": 54, "rhs_register": 55},
            "instruction_id": 83,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 57, "value": 1},
            "instruction_id": 84,
        },
        {
            "instruction": "EQ",
            "metadata": {"register": 58, "lhs_register": 56, "rhs_register": 57},
            "instruction_id": 85,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 59, "value": 14},
            "instruction_id": 86,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 60, "value": 1},
            "instruction_id": 87,
        },
        {
            "instruction": "GT",
            "metadata": {"register": 61, "lhs_register": 59, "rhs_register": 60},
            "instruction_id": 88,
        },
        {
            "instruction": "OR",
            "metadata": {"register": 62, "lhs_register": 58, "rhs_register": 61},
            "instruction_id": 89,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 63, "value": 14},
            "instruction_id": 90,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 64, "value": 10},
            "instruction_id": 91,
        },
        {
            "instruction": "LT",
            "metadata": {"register": 65, "lhs_register": 63, "rhs_register": 64},
            "instruction_id": 92,
        },
        {
            "instruction": "AND",
            "metadata": {"register": 66, "lhs_register": 62, "rhs_register": 65},
            "instruction_id": 93,
        },
        {
            "instruction": "JZ",
            "metadata": {"conditional_register": 66, "jump_size": 7},
            "instruction_id": 94,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 67, "value": 16},
            "instruction_id": 95,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 68, "value": 14},
            "instruction_id": 96,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 69, "value": 1},
            "instruction_id": 97,
        },
        {
            "instruction": "BITAND",
            "metadata": {"register": 70, "lhs_register": 68, "rhs_register": 69},
            "instruction_id": 98,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 67, "value": 70},
            "instruction_id": 99,
        },
        {
            "instruction": "JZ",
            "metadata": {"conditional_register": "zero", "jump_size": 6},
            "instruction_id": 100,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 71, "value": 16},
            "instruction_id": 101,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 72, "value": 14},
            "instruction_id": 102,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 73, "value": 1},
            "instruction_id": 103,
        },
        {
            "instruction": "BITOR",
            "metadata": {"register": 74, "lhs_register": 72, "rhs_register": 73},
            "instruction_id": 104,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 71, "value": 74},
            "instruction_id": 105,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 75, "value": 14},
            "instruction_id": 106,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 76, "value": 16},
            "instruction_id": 107,
        },
        {
            "instruction": "MULT",
            "metadata": {"register": 77, "lhs_register": 75, "rhs_register": 76},
            "instruction_id": 108,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 78, "value": 2},
            "instruction_id": 109,
        },
        {
            "instruction": "DIV",
            "metadata": {"register": 79, "lhs_register": 77, "rhs_register": 78},
            "instruction_id": 110,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 80, "value": 1},
            "instruction_id": 111,
        },
        {
            "instruction": "RSHIFT",
            "metadata": {"register": 81, "lhs_register": 79, "rhs_register": 80},
            "instruction_id": 112,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 81},
            "instruction_id": 113,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 114,
        },
        {"instruction": "HALT", "metadata": {}, "instruction_id": 115},
    ],
}
