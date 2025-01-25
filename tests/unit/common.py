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
    "functions": {
        "function_that_returns_struct": {"start": 0, "end": 16},
        "some_simple_function": {"start": 16, "end": 27},
        "abc": {"start": 27, "end": 61},
        "main": {"start": 61, "end": 109},
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
            "metadata": {"register": 5, "id": 5},
            "instruction_id": 8,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 6, "id": 3},
            "instruction_id": 9,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 7, "id": 4},
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
            "instruction": "ADDRESS",
            "metadata": {"register": 9, "id": 2, "offset_size": 0},
            "instruction_id": 13,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 10, "id": 5},
            "instruction_id": 14,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 9, "value": 10},
            "instruction_id": 15,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 11, "id": 2},
            "instruction_id": 16,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 11},
            "instruction_id": 17,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 18,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 6, "size": 4, "register": 12},
            "instruction_id": 19,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 12, "value": "arg"},
            "instruction_id": 20,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 7, "size": 4, "register": 13},
            "instruction_id": 21,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 13, "value": "arg"},
            "instruction_id": 22,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 14, "id": 6},
            "instruction_id": 23,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 15, "id": 7},
            "instruction_id": 24,
        },
        {
            "instruction": "SITOFP",
            "metadata": {"register": 16, "value": 15},
            "instruction_id": 25,
        },
        {
            "instruction": "FDIV",
            "metadata": {"register": 17, "lhs_register": 14, "rhs_register": 16},
            "instruction_id": 26,
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"register": 18, "value": 17},
            "instruction_id": 27,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 18},
            "instruction_id": 28,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 29,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 8, "size": 4, "register": 19},
            "instruction_id": 30,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 19, "value": "arg"},
            "instruction_id": 31,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 9, "size": 4, "register": 20},
            "instruction_id": 32,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 20, "value": "arg"},
            "instruction_id": 33,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 10, "size": 4, "register": 21},
            "instruction_id": 34,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 22, "id": 10},
            "instruction_id": 35,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 23, "value": 1},
            "instruction_id": 36,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 22, "value": 23},
            "instruction_id": 37,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 11, "size": 4, "register": 24},
            "instruction_id": 38,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 25, "id": 11},
            "instruction_id": 39,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 26, "value": 2.0},
            "instruction_id": 40,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 25, "value": 26},
            "instruction_id": 41,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 12, "size": 2, "register": 27},
            "instruction_id": 42,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 13, "size": 8, "register": 28},
            "instruction_id": 43,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 29, "id": 13, "offset_size": 0},
            "instruction_id": 44,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 30, "value": 1},
            "instruction_id": 45,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 29, "value": 30},
            "instruction_id": 46,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 31, "id": 10},
            "instruction_id": 47,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 32, "id": 10},
            "instruction_id": 48,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 33, "id": 11},
            "instruction_id": 49,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 33},
            "instruction_id": 50,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 34, "value": 123},
            "instruction_id": 51,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 34},
            "instruction_id": 52,
        },
        {"instruction": "JAL", "metadata": {"value": 2}, "instruction_id": 53},
        {
            "instruction": "MOV",
            "metadata": {"register": 35, "value": "ret_value"},
            "instruction_id": 54,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 36, "lhs_register": 32, "rhs_register": 35},
            "instruction_id": 55,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 31, "value": 36},
            "instruction_id": 56,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 37, "id": 11},
            "instruction_id": 57,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 38, "id": 10},
            "instruction_id": 58,
        },
        {
            "instruction": "SITOFP",
            "metadata": {"register": 39, "value": 38},
            "instruction_id": 59,
        },
        {
            "instruction": "FADD",
            "metadata": {"register": 40, "lhs_register": 37, "rhs_register": 39},
            "instruction_id": 60,
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"register": 41, "value": 40},
            "instruction_id": 61,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 41},
            "instruction_id": 62,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 63,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 14, "size": 4, "register": 42},
            "instruction_id": 64,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 43, "id": 14},
            "instruction_id": 65,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 44, "value": 1},
            "instruction_id": 66,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 44},
            "instruction_id": 67,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 45, "value": 2},
            "instruction_id": 68,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 45},
            "instruction_id": 69,
        },
        {"instruction": "JAL", "metadata": {"value": 3}, "instruction_id": 70},
        {
            "instruction": "MOV",
            "metadata": {"register": 46, "value": "ret_value"},
            "instruction_id": 71,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 43, "value": 46},
            "instruction_id": 72,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 15, "size": 40, "register": 47},
            "instruction_id": 73,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 48, "id": 15, "offset_size": 20},
            "instruction_id": 74,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 49, "value": 1},
            "instruction_id": 75,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 48, "value": 49},
            "instruction_id": 76,
        },
        {
            "instruction": "ALLOC",
            "metadata": {"id": 16, "size": 4, "register": 50},
            "instruction_id": 77,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 51, "id": 14},
            "instruction_id": 78,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 52, "value": 4},
            "instruction_id": 79,
        },
        {
            "instruction": "LSHIFT",
            "metadata": {"register": 53, "lhs_register": 51, "rhs_register": 52},
            "instruction_id": 80,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 54, "value": 1},
            "instruction_id": 81,
        },
        {
            "instruction": "EQ",
            "metadata": {"register": 55, "lhs_register": 53, "rhs_register": 54},
            "instruction_id": 82,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 56, "id": 14},
            "instruction_id": 83,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 57, "value": 1},
            "instruction_id": 84,
        },
        {
            "instruction": "GT",
            "metadata": {"register": 58, "lhs_register": 56, "rhs_register": 57},
            "instruction_id": 85,
        },
        {
            "instruction": "OR",
            "metadata": {"register": 59, "lhs_register": 55, "rhs_register": 58},
            "instruction_id": 86,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 60, "id": 14},
            "instruction_id": 87,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 61, "value": 10},
            "instruction_id": 88,
        },
        {
            "instruction": "LT",
            "metadata": {"register": 62, "lhs_register": 60, "rhs_register": 61},
            "instruction_id": 89,
        },
        {
            "instruction": "AND",
            "metadata": {"register": 63, "lhs_register": 59, "rhs_register": 62},
            "instruction_id": 90,
        },
        {
            "instruction": "JZ",
            "metadata": {"conditional_register": 63, "jump_size": 7},
            "instruction_id": 91,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 64, "id": 16},
            "instruction_id": 92,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 65, "id": 14},
            "instruction_id": 93,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 66, "value": 1},
            "instruction_id": 94,
        },
        {
            "instruction": "BITAND",
            "metadata": {"register": 67, "lhs_register": 65, "rhs_register": 66},
            "instruction_id": 95,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 64, "value": 67},
            "instruction_id": 96,
        },
        {
            "instruction": "JZ",
            "metadata": {"conditional_register": "zero", "jump_size": 6},
            "instruction_id": 97,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 68, "id": 16},
            "instruction_id": 98,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 69, "id": 14},
            "instruction_id": 99,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 70, "value": 1},
            "instruction_id": 100,
        },
        {
            "instruction": "BITOR",
            "metadata": {"register": 71, "lhs_register": 69, "rhs_register": 70},
            "instruction_id": 101,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 68, "value": 71},
            "instruction_id": 102,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 72, "id": 14},
            "instruction_id": 103,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 73, "id": 16},
            "instruction_id": 104,
        },
        {
            "instruction": "MULT",
            "metadata": {"register": 74, "lhs_register": 72, "rhs_register": 73},
            "instruction_id": 105,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 75, "value": 2},
            "instruction_id": 106,
        },
        {
            "instruction": "DIV",
            "metadata": {"register": 76, "lhs_register": 74, "rhs_register": 75},
            "instruction_id": 107,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 77, "value": 1},
            "instruction_id": 108,
        },
        {
            "instruction": "RSHIFT",
            "metadata": {"register": 78, "lhs_register": 76, "rhs_register": 77},
            "instruction_id": 109,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 78},
            "instruction_id": 110,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "instruction_id": 111,
        },
        {"instruction": "HALT", "metadata": {}, "instruction_id": 112},
    ],
}

CERTIFICATE = [
    "2^((3)^(2)^(40))",
    "3^((3)^(3)^(8))",
    "5^((11)^(5)^(4))",
    "7^((11)^(7)^(4))",
    "11^((3)^(11)^(4))",
    "29^(41)*13^((7)^(11)^(2)^(1))*23^(47)*17^((5)^(5)^(2)^(1))*19^((5)^(7)^(2)^(1))",
    "41^(41)*31^((7)^(3)^(2)^(1))*37^((5)^(11)^(2)^(1))",
    "47^(19)*43^((5)^(3)^(2)^(1))",
    "53^((11)^(13)^(4))",
    "59^((11)^(17)^(4))",
    "73^(19)*71^(61)*61^((5)^(13)^(2)^(1))*67^((5)^(17)^(2)^(1))",
    "79^((11)^(19)^(4))",
    "83^((11)^(23)^(4))",
    "89^((3)^(29)^(4))",
    "103^(41)*97^((7)^(29)^(2)^(1))*101^((2)^(2))",
    "107^((3)^(31)^(4))",
    "127^(41)*109^((7)^(31)^(2)^(1))*113^((2)^(3.0))",
    "131^((3)^(37)^(2))",
    "137^((3)^(41)^(8))",
    "151^(41)*139^((7)^(41)^(2)^(1))*149^((2)^(2))",
    "197^(41)*157^((7)^(29)^(2)^(1))*193^(47)*163^((5)^(29)^(2)^(1))*191^((17)^(3))*173^(13)*167^((5)^(31)^(2)^(1))*181^(13)*179^((2)^(124))",
    "227^(19)*223^(47)*199^((5)^(31)^(2)^(1))*211^((5)^(29)^(2)^(1))",
    "229^((3)^(43)^(4))",
    "269^(41)*233^((7)^(43)^(2)^(1))*263^((17)^(5))*241^(13)*239^((2)^(2))*257^(13)*251^((2)^(3))",
    "271^((3)^(47)^(40))",
    "283^(41)*277^((7)^(47)^(2)^(21))*281^((2)^(2))",
    "293^((3)^(53)^(4))",
    "379^(89)*353^(97)*331^(79)*313^(101)*307^((5)^(43)^(2)^(1))*311^((2)^(5))*317^((2)^(2))*349^(73)*337^((5)^(43)^(2)^(1))*347^((2)^(2))*373^(71)*359^((5)^(43)^(2)^(1))*367^((2)^(11))",
    "383^(29)",
    "419^(41)*389^((7)^(53)^(2)^(1))*409^(107)*397^((5)^(43)^(2)^(1))*401^((2)^(2))",
    "443^(41)*421^((7)^(53)^(2)^(1))*439^(109)*431^((5)^(43)^(2)^(1))*433^((2)^(2))",
    "491^(19)*487^(103)*467^(61)*461^(59)*449^((5)^(43)^(2)^(1))*457^((5)^(53)^(2)^(1))*463^((2)^(3))*479^((2)^(2))",
    "499^(113)",
]
