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
                        "called_function_metadata": {
                            "relative_position": 2,
                            "prime": 3,
                            "type": "int",
                            "parameters": {
                                "param_1": {
                                    "type": "float",
                                    "relative_position": 6,
                                    "prime": 13,
                                },
                                "param_2": {
                                    "type": "int",
                                    "relative_position": 7,
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
                                        "relative_position": 6,
                                        "prime": 13,
                                    },
                                ),
                                ("DIV", {}),
                                (
                                    "VAR",
                                    {
                                        "type": "int",
                                        "relative_position": 7,
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
                        "arguments": [
                            {"variable": False, "type": "int", "value": 1},
                            {"variable": False, "type": "int", "value": 2},
                        ],
                        "called_function_metadata": {
                            "relative_position": 3,
                            "prime": 5,
                            "type": "int",
                            "parameters": {
                                "asda": {
                                    "type": "int",
                                    "relative_position": 8,
                                    "prime": 19,
                                },
                                "abcdef": {
                                    "type": "int",
                                    "relative_position": 9,
                                    "prime": 23,
                                },
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
                                        "arguments": [
                                            {
                                                "variable": True,
                                                "name": "blabla",
                                                "relative_position": 11,
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
                                            "relative_position": 2,
                                            "prime": 3,
                                            "type": "int",
                                            "parameters": {
                                                "param_1": {
                                                    "type": "float",
                                                    "relative_position": 6,
                                                    "prime": 13,
                                                },
                                                "param_2": {
                                                    "type": "int",
                                                    "relative_position": 7,
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
                                                        "relative_position": 6,
                                                        "prime": 13,
                                                    },
                                                ),
                                                ("DIV", {}),
                                                (
                                                    "VAR",
                                                    {
                                                        "type": "int",
                                                        "relative_position": 7,
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
        "function_that_returns_struct": {"start": 0, "end": 18},
        "some_simple_function": {"start": 18, "end": 29},
        "abc": {"start": 29, "end": 65},
        "main": {"start": 65, "end": 115},
    },
    "global_vars": [
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 1,
                "type": "int",
                "size": 40,
                "register": 0,
            },
            "id": 1,
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 2,
                "type": "int",
                "size": 8,
                "register": 1,
            },
            "id": 2,
        },
    ],
    "code": [
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 3,
                "type": "int",
                "size": 4,
                "register": 2,
            },
            "id": 3,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 2, "value": "arg", "type": "int"},
            "id": 4,
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 4,
                "type": "int",
                "size": 4,
                "register": 3,
            },
            "id": 5,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 3, "value": "arg", "type": "int"},
            "id": 6,
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 5,
                "type": "int",
                "size": 4,
                "register": 4,
            },
            "id": 7,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 5, "value": 5, "type": "int"},
            "id": 8,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 6, "value": 3, "type": "int"},
            "id": 9,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 7, "value": 4, "type": "int"},
            "id": 10,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 8, "lhs_register": 6, "rhs_register": 7},
            "id": 11,
        },
        {"instruction": "STORE", "metadata": {"register": 5, "value": 8}, "id": 12},
        {
            "instruction": "LOAD",
            "metadata": {"register": 9, "value": 2, "type": "my_struct"},
            "id": 13,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 10, "value": 0, "type": "int"},
            "id": 14,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {
                "register": 11,
                "value": 2,
                "type": "int",
                "offset_register": None,
                "offset_size": 0,
            },
            "id": 15,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 12, "value": 5, "type": "int"},
            "id": 16,
        },
        {"instruction": "STORE", "metadata": {"register": 11, "value": 12}, "id": 17},
        {
            "instruction": "LOAD",
            "metadata": {"register": 13, "value": 2, "type": "my_struct"},
            "id": 18,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 13},
            "id": 19,
        },
        {"instruction": "JR", "metadata": {"register": "ret_address"}, "id": 20},
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 6,
                "type": "int",
                "size": 4,
                "register": 14,
            },
            "id": 21,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 14, "value": "arg", "type": "float"},
            "id": 22,
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 7,
                "type": "int",
                "size": 4,
                "register": 15,
            },
            "id": 23,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 15, "value": "arg", "type": "int"},
            "id": 24,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 16, "value": 6, "type": "float"},
            "id": 25,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 17, "value": 7, "type": "int"},
            "id": 26,
        },
        {
            "instruction": "SITOFP",
            "metadata": {"source_register": 17, "destination_register": 18},
            "id": 27,
        },
        {
            "instruction": "FDIV",
            "metadata": {"register": 19, "lhs_register": 16, "rhs_register": 18},
            "id": 28,
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"source_register": 19, "destination_register": 20},
            "id": 29,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 20},
            "id": 30,
        },
        {"instruction": "JR", "metadata": {"register": "ret_address"}, "id": 31},
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 8,
                "type": "int",
                "size": 4,
                "register": 21,
            },
            "id": 32,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 21, "value": "arg", "type": "int"},
            "id": 33,
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 9,
                "type": "int",
                "size": 4,
                "register": 22,
            },
            "id": 34,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 22, "value": "arg", "type": "int"},
            "id": 35,
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 10,
                "type": "int",
                "size": 4,
                "register": 23,
            },
            "id": 36,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 24, "value": 10, "type": "int"},
            "id": 37,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 25, "value": 1, "type": "int"},
            "id": 38,
        },
        {"instruction": "STORE", "metadata": {"register": 24, "value": 25}, "id": 39},
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 11,
                "type": "int",
                "size": 4,
                "register": 26,
            },
            "id": 40,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 27, "value": 11, "type": "float"},
            "id": 41,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 28, "value": 2.0, "type": "float"},
            "id": 42,
        },
        {"instruction": "STORE", "metadata": {"register": 27, "value": 28}, "id": 43},
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 12,
                "type": "int",
                "size": 2,
                "register": 29,
            },
            "id": 44,
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 13,
                "type": "int",
                "size": 8,
                "register": 30,
            },
            "id": 45,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 31, "value": 13, "type": "my_struct"},
            "id": 46,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 32, "value": 0, "type": "int"},
            "id": 47,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {
                "register": 33,
                "value": 13,
                "type": "int",
                "offset_register": None,
                "offset_size": 0,
            },
            "id": 48,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 34, "value": 1, "type": "int"},
            "id": 49,
        },
        {"instruction": "STORE", "metadata": {"register": 33, "value": 34}, "id": 50},
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 35, "value": 10, "type": "int"},
            "id": 51,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 36, "value": 10, "type": "int"},
            "id": 52,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 37, "value": 11, "type": "float"},
            "id": 53,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 37, "type": None},
            "id": 54,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 38, "value": 123, "type": "int"},
            "id": 55,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 38, "type": None},
            "id": 56,
        },
        {"instruction": "JAL", "metadata": {"value": 2}, "id": 57},
        {
            "instruction": "MOV",
            "metadata": {"register": 39, "value": "ret_value", "type": "int"},
            "id": 58,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 40, "lhs_register": 36, "rhs_register": 39},
            "id": 59,
        },
        {"instruction": "STORE", "metadata": {"register": 35, "value": 40}, "id": 60},
        {
            "instruction": "LOAD",
            "metadata": {"register": 41, "value": 11, "type": "float"},
            "id": 61,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 42, "value": 10, "type": "int"},
            "id": 62,
        },
        {
            "instruction": "SITOFP",
            "metadata": {"source_register": 42, "destination_register": 43},
            "id": 63,
        },
        {
            "instruction": "FADD",
            "metadata": {"register": 44, "lhs_register": 41, "rhs_register": 43},
            "id": 64,
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"source_register": 44, "destination_register": 45},
            "id": 65,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 45},
            "id": 66,
        },
        {"instruction": "JR", "metadata": {"register": "ret_address"}, "id": 67},
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 14,
                "type": "int",
                "size": 4,
                "register": 46,
            },
            "id": 68,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 47, "value": 14, "type": "int"},
            "id": 69,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 48, "value": 1, "type": "int"},
            "id": 70,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 48, "type": None},
            "id": 71,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 49, "value": 2, "type": "int"},
            "id": 72,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 49, "type": None},
            "id": 73,
        },
        {"instruction": "JAL", "metadata": {"value": 3}, "id": 74},
        {
            "instruction": "MOV",
            "metadata": {"register": 50, "value": "ret_value", "type": "int"},
            "id": 75,
        },
        {"instruction": "STORE", "metadata": {"register": 47, "value": 50}, "id": 76},
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 15,
                "type": "int",
                "size": 40,
                "register": 51,
            },
            "id": 77,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 52, "value": 15, "type": "int"},
            "id": 78,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 53, "value": 5, "type": "int"},
            "id": 79,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 54, "value": 15, "type": "int", "offset_size": 20},
            "id": 80,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 55, "value": 1, "type": "int"},
            "id": 81,
        },
        {"instruction": "STORE", "metadata": {"register": 54, "value": 55}, "id": 82},
        {
            "instruction": "ALLOC",
            "metadata": {
                "relative_position": 16,
                "type": "int",
                "size": 4,
                "register": 56,
            },
            "id": 83,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 57, "value": 14, "type": "int"},
            "id": 84,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 58, "value": 4, "type": "int"},
            "id": 85,
        },
        {
            "instruction": "LSHIFT",
            "metadata": {"register": 59, "lhs_register": 57, "rhs_register": 58},
            "id": 86,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 60, "value": 1, "type": "int"},
            "id": 87,
        },
        {
            "instruction": "EQ",
            "metadata": {"register": 61, "lhs_register": 59, "rhs_register": 60},
            "id": 88,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 62, "value": 14, "type": "int"},
            "id": 89,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 63, "value": 1, "type": "int"},
            "id": 90,
        },
        {
            "instruction": "GT",
            "metadata": {"register": 64, "lhs_register": 62, "rhs_register": 63},
            "id": 91,
        },
        {
            "instruction": "OR",
            "metadata": {"register": 65, "lhs_register": 61, "rhs_register": 64},
            "id": 92,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 66, "value": 14, "type": "int"},
            "id": 93,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 67, "value": 10, "type": "int"},
            "id": 94,
        },
        {
            "instruction": "LT",
            "metadata": {"register": 68, "lhs_register": 66, "rhs_register": 67},
            "id": 95,
        },
        {
            "instruction": "AND",
            "metadata": {"register": 69, "lhs_register": 65, "rhs_register": 68},
            "id": 96,
        },
        {
            "instruction": "JZ",
            "metadata": {"conditional_register": 69, "jump_size": 7},
            "id": 97,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 70, "value": 16, "type": "int"},
            "id": 98,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 71, "value": 14, "type": "int"},
            "id": 99,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 72, "value": 1, "type": "int"},
            "id": 100,
        },
        {
            "instruction": "BITAND",
            "metadata": {"register": 73, "lhs_register": 71, "rhs_register": 72},
            "id": 101,
        },
        {"instruction": "STORE", "metadata": {"register": 70, "value": 73}, "id": 102},
        {
            "instruction": "JZ",
            "metadata": {"conditional_register": "zero", "jump_size": 6},
            "id": 103,
        },
        {
            "instruction": "ADDRESS",
            "metadata": {"register": 74, "value": 16, "type": "int"},
            "id": 104,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 75, "value": 14, "type": "int"},
            "id": 105,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 76, "value": 1, "type": "int"},
            "id": 106,
        },
        {
            "instruction": "BITOR",
            "metadata": {"register": 77, "lhs_register": 75, "rhs_register": 76},
            "id": 107,
        },
        {"instruction": "STORE", "metadata": {"register": 74, "value": 77}, "id": 108},
        {
            "instruction": "LOAD",
            "metadata": {"register": 78, "value": 14, "type": "int"},
            "id": 109,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 79, "value": 16, "type": "int"},
            "id": 110,
        },
        {
            "instruction": "MULT",
            "metadata": {"register": 80, "lhs_register": 78, "rhs_register": 79},
            "id": 111,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 81, "value": 2, "type": "int"},
            "id": 112,
        },
        {
            "instruction": "DIV",
            "metadata": {"register": 82, "lhs_register": 80, "rhs_register": 81},
            "id": 113,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 83, "value": 1, "type": "int"},
            "id": 114,
        },
        {
            "instruction": "RSHIFT",
            "metadata": {"register": 84, "lhs_register": 82, "rhs_register": 83},
            "id": 115,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 84},
            "id": 116,
        },
        {"instruction": "JR", "metadata": {"register": "ret_address"}, "id": 117},
        {"instruction": "HALT", "metadata": {}, "id": 118},
    ],
}
