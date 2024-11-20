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
        "function_that_returns_struct": {"start": 0, "end": 18},
        "some_simple_function": {"start": 18, "end": 29},
        "abc": {"start": 29, "end": 65},
        "main": {"start": 65, "end": 115},
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
            "instruction": "CONSTANT",
            "metadata": {"register": 10, "value": 0},
            "instruction_id": 14,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {
                "register": 11,
                "value": 2,
                "offset_register": None,
                "offset_size": 0,
            },
            "instruction_id": 15,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 12, "value": 5},
            "instruction_id": 16,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 11, "value": 12},
            "instruction_id": 17,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 13, "value": 2},
            "instruction_id": 18,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 13},
            "instruction_id": 19,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 20,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 6, "size": 4, "register": 14},
            "instruction_id": 21,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 14, "value": "arg"},
            "instruction_id": 22,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 7, "size": 4, "register": 15},
            "instruction_id": 23,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 15, "value": "arg"},
            "instruction_id": 24,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 16, "value": 6},
            "instruction_id": 25,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 17, "value": 7},
            "instruction_id": 26,
        },
        {
            "instruction": "SITOFP",
            "metadata": {"source_register": 17, "destination_register": 18},
            "instruction_id": 27,
        },
        {
            "instruction": "FDIV",
            "metadata": {"register": 19, "lhs_register": 16, "rhs_register": 18},
            "instruction_id": 28,
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"source_register": 19, "destination_register": 20},
            "instruction_id": 29,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 20},
            "instruction_id": 30,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 31,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 8, "size": 4, "register": 21},
            "instruction_id": 32,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 21, "value": "arg"},
            "instruction_id": 33,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 9, "size": 4, "register": 22},
            "instruction_id": 34,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 22, "value": "arg"},
            "instruction_id": 35,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 10, "size": 4, "register": 23},
            "instruction_id": 36,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 24, "value": 10},
            "instruction_id": 37,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 25, "value": 1},
            "instruction_id": 38,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 24, "value": 25},
            "instruction_id": 39,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 11, "size": 4, "register": 26},
            "instruction_id": 40,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 27, "value": 11},
            "instruction_id": 41,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 28, "value": 2.0},
            "instruction_id": 42,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 27, "value": 28},
            "instruction_id": 43,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 12, "size": 2, "register": 29},
            "instruction_id": 44,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 13, "size": 8, "register": 30},
            "instruction_id": 45,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 31, "value": 13},
            "instruction_id": 46,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 32, "value": 0},
            "instruction_id": 47,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {
                "register": 33,
                "value": 13,
                "offset_register": None,
                "offset_size": 0,
            },
            "instruction_id": 48,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 34, "value": 1},
            "instruction_id": 49,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 33, "value": 34},
            "instruction_id": 50,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 35, "value": 10},
            "instruction_id": 51,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 36, "value": 10},
            "instruction_id": 52,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 37, "value": 11},
            "instruction_id": 53,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 37},
            "instruction_id": 54,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 38, "value": 123},
            "instruction_id": 55,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 38},
            "instruction_id": 56,
        },
        {"instruction": "JAL", "metadata": {"value": 2}, "instruction_id": 57},
        {
            "instruction": "MOV",
            "metadata": {"register": 39, "value": "ret_value"},
            "instruction_id": 58,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 40, "lhs_register": 36, "rhs_register": 39},
            "instruction_id": 59,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 35, "value": 40},
            "instruction_id": 60,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 41, "value": 11},
            "instruction_id": 61,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 42, "value": 10},
            "instruction_id": 62,
        },
        {
            "instruction": "SITOFP",
            "metadata": {"source_register": 42, "destination_register": 43},
            "instruction_id": 63,
        },
        {
            "instruction": "FADD",
            "metadata": {"register": 44, "lhs_register": 41, "rhs_register": 43},
            "instruction_id": 64,
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"source_register": 44, "destination_register": 45},
            "instruction_id": 65,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 45},
            "instruction_id": 66,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 67,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 14, "size": 4, "register": 46},
            "instruction_id": 68,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 47, "value": 14},
            "instruction_id": 69,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 48, "value": 1},
            "instruction_id": 70,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 48},
            "instruction_id": 71,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 49, "value": 2},
            "instruction_id": 72,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 49},
            "instruction_id": 73,
        },
        {"instruction": "JAL", "metadata": {"value": 3}, "instruction_id": 74},
        {
            "instruction": "MOV",
            "metadata": {"register": 50, "value": "ret_value"},
            "instruction_id": 75,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 47, "value": 50},
            "instruction_id": 76,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 15, "size": 40, "register": 51},
            "instruction_id": 77,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 52, "value": 15},
            "instruction_id": 78,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 53, "value": 5},
            "instruction_id": 79,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 54, "value": 15, "offset_size": 20},
            "instruction_id": 80,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 55, "value": 1},
            "instruction_id": 81,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 54, "value": 55},
            "instruction_id": 82,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 16, "size": 4, "register": 56},
            "instruction_id": 83,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 57, "value": 14},
            "instruction_id": 84,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 58, "value": 4},
            "instruction_id": 85,
        },
        {
            "instruction": "LSHIFT",
            "metadata": {"register": 59, "lhs_register": 57, "rhs_register": 58},
            "instruction_id": 86,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 60, "value": 1},
            "instruction_id": 87,
        },
        {
            "instruction": "EQ",
            "metadata": {"register": 61, "lhs_register": 59, "rhs_register": 60},
            "instruction_id": 88,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 62, "value": 14},
            "instruction_id": 89,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 63, "value": 1},
            "instruction_id": 90,
        },
        {
            "instruction": "GT",
            "metadata": {"register": 64, "lhs_register": 62, "rhs_register": 63},
            "instruction_id": 91,
        },
        {
            "instruction": "OR",
            "metadata": {"register": 65, "lhs_register": 61, "rhs_register": 64},
            "instruction_id": 92,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 66, "value": 14},
            "instruction_id": 93,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 67, "value": 10},
            "instruction_id": 94,
        },
        {
            "instruction": "LT",
            "metadata": {"register": 68, "lhs_register": 66, "rhs_register": 67},
            "instruction_id": 95,
        },
        {
            "instruction": "AND",
            "metadata": {"register": 69, "lhs_register": 65, "rhs_register": 68},
            "instruction_id": 96,
        },
        {
            "instruction": "JZ",
            "metadata": {"conditional_register": 69, "jump_size": 7},
            "instruction_id": 97,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 70, "value": 16},
            "instruction_id": 98,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 71, "value": 14},
            "instruction_id": 99,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 72, "value": 1},
            "instruction_id": 100,
        },
        {
            "instruction": "BITAND",
            "metadata": {"register": 73, "lhs_register": 71, "rhs_register": 72},
            "instruction_id": 101,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 70, "value": 73},
            "instruction_id": 102,
        },
        {
            "instruction": "JZ",
            "metadata": {"conditional_register": "zero", "jump_size": 6},
            "instruction_id": 103,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 74, "value": 16},
            "instruction_id": 104,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 75, "value": 14},
            "instruction_id": 105,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 76, "value": 1},
            "instruction_id": 106,
        },
        {
            "instruction": "BITOR",
            "metadata": {"register": 77, "lhs_register": 75, "rhs_register": 76},
            "instruction_id": 107,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 74, "value": 77},
            "instruction_id": 108,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 78, "value": 14},
            "instruction_id": 109,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 79, "value": 16},
            "instruction_id": 110,
        },
        {
            "instruction": "MULT",
            "metadata": {"register": 80, "lhs_register": 78, "rhs_register": 79},
            "instruction_id": 111,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 81, "value": 2},
            "instruction_id": 112,
        },
        {
            "instruction": "DIV",
            "metadata": {"register": 82, "lhs_register": 80, "rhs_register": 81},
            "instruction_id": 113,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 83, "value": 1},
            "instruction_id": 114,
        },
        {
            "instruction": "RSHIFT",
            "metadata": {"register": 84, "lhs_register": 82, "rhs_register": 83},
            "instruction_id": 115,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 84},
            "instruction_id": 116,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 117,
        },
        {"instruction": "HALT", "metadata": {}, "instruction_id": 118},
    ],
}
