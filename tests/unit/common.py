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

TOKENIZED_SOURCE_CODE = {
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

_source = deepcopy(TOKENIZED_SOURCE_CODE)
ast = AbstractSyntaxTree(source_code=_source)
ABSTRACT_SYNTAX_TREE_ROOT = ast.build()

MACHINE_CODE = {
    "structs": {"my_struct": ["int", "float"], "test_struct": ["int", "int"]},
    "global_vars": [
        {
            "instruction": "ALLOC",
            "metadata": {
                "id": 3,
                "register": 0,
                "type": "int",
                "relative_position": 1,
                "length": 10,
            },
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "id": 4,
                "register": 1,
                "type": "my_struct",
                "relative_position": 2,
                "length": 1,
            },
        },
    ],
    "functions": {
        "function_that_returns_struct": [
            {
                "instruction": "ALLOC",
                "metadata": {
                    "id": None,
                    "register": 2,
                    "type": "int",
                    "relative_position": 3,
                    "length": 1,
                },
            },
            {
                "instruction": "ALLOC",
                "metadata": {
                    "id": None,
                    "register": 3,
                    "type": "int",
                    "relative_position": 4,
                    "length": 1,
                },
            },
            {"instruction": "SEQ", "metadata": {}},
            {
                "instruction": "ALLOC",
                "metadata": {
                    "id": 8,
                    "register": 4,
                    "type": "int",
                    "relative_position": 5,
                    "length": 1,
                },
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 14, "register": 5, "value": 3, "type": "int"},
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 16, "register": 6, "value": 4, "type": "int"},
            },
            {
                "instruction": "ADD",
                "metadata": {
                    "id": 15,
                    "register": 7,
                    "lhs_register": 5,
                    "rhs_register": 6,
                },
            },
            {"instruction": "POP", "metadata": {"id": 13}},
            {"instruction": "RET", "metadata": {"id": 12, "register": 7}},
        ],
        "some_simple_function": [
            {
                "instruction": "ALLOC",
                "metadata": {
                    "id": None,
                    "register": 2,
                    "type": "float",
                    "relative_position": 3,
                    "length": 1,
                },
            },
            {
                "instruction": "ALLOC",
                "metadata": {
                    "id": None,
                    "register": 3,
                    "type": "int",
                    "relative_position": 4,
                    "length": 1,
                },
            },
            {"instruction": "SEQ", "metadata": {}},
            {
                "instruction": "FETCH",
                "metadata": {"id": 22, "register": 4, "value": 3, "type": "float"},
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 24, "register": 5, "value": 4, "type": "int"},
            },
            {
                "instruction": "SITOFP",
                "metadata": {"source_register": 5, "destination_register": 6},
            },
            {
                "instruction": "FDIV",
                "metadata": {
                    "id": 23,
                    "register": 7,
                    "lhs_register": 4,
                    "rhs_register": 6,
                },
            },
            {"instruction": "POP", "metadata": {"id": 21}},
            {"instruction": "RET", "metadata": {"id": 20, "register": 7}},
        ],
        "abc": [
            {
                "instruction": "ALLOC",
                "metadata": {
                    "id": None,
                    "register": 2,
                    "type": "int",
                    "relative_position": 3,
                    "length": 1,
                },
            },
            {
                "instruction": "ALLOC",
                "metadata": {
                    "id": None,
                    "register": 3,
                    "type": "int",
                    "relative_position": 4,
                    "length": 1,
                },
            },
            {"instruction": "SEQ", "metadata": {}},
            {
                "instruction": "ALLOC",
                "metadata": {
                    "id": 28,
                    "register": 4,
                    "type": "int",
                    "relative_position": 5,
                    "length": 1,
                },
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 33, "register": 5, "value": 5, "type": "int"},
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 35, "register": 6, "value": 1, "type": "int"},
            },
            {
                "instruction": "STORE",
                "metadata": {"id": 34, "lhs_register": 5, "rhs_register": 6},
            },
            {"instruction": "POP", "metadata": {"id": 32}},
            {
                "instruction": "ALLOC",
                "metadata": {
                    "id": 37,
                    "register": 7,
                    "type": "float",
                    "relative_position": 6,
                    "length": 1,
                },
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 42, "register": 8, "value": 6, "type": "float"},
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 44, "register": 9, "value": 2.0, "type": "float"},
            },
            {
                "instruction": "STORE",
                "metadata": {"id": 43, "lhs_register": 8, "rhs_register": 9},
            },
            {"instruction": "POP", "metadata": {"id": 41}},
            {
                "instruction": "ALLOC",
                "metadata": {
                    "id": 46,
                    "register": 10,
                    "type": "short",
                    "relative_position": 7,
                    "length": 1,
                },
            },
            {
                "instruction": "ALLOC",
                "metadata": {
                    "id": 50,
                    "register": 11,
                    "type": "my_struct",
                    "relative_position": 8,
                    "length": 1,
                },
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 55, "register": 12, "value": 8, "type": "my_struct"},
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 57, "register": 13, "value": 0, "type": "int"},
            },
            {
                "instruction": "ELEMENT_PTR",
                "metadata": {
                    "id": 56,
                    "register": 14,
                    "variable_register": 12,
                    "element_register": 13,
                },
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 59, "register": 15, "value": 1, "type": "int"},
            },
            {
                "instruction": "STORE",
                "metadata": {"id": 58, "lhs_register": 14, "rhs_register": 15},
            },
            {"instruction": "POP", "metadata": {"id": 54}},
            {
                "instruction": "FETCH",
                "metadata": {"id": 62, "register": 16, "value": 5, "type": "int"},
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 64, "register": 17, "value": 5, "type": "int"},
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 67, "register": 18, "value": 6, "type": "float"},
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 68, "register": 19, "value": 123, "type": "int"},
            },
            {
                "instruction": "CALL",
                "metadata": {
                    "id": 66,
                    "register": 20,
                    "value": 2,
                    "type": "int",
                    "parameters_registers": [18, 19],
                },
            },
            {
                "instruction": "ADD",
                "metadata": {
                    "id": 65,
                    "register": 21,
                    "lhs_register": 17,
                    "rhs_register": 20,
                },
            },
            {
                "instruction": "STORE",
                "metadata": {"id": 63, "lhs_register": 16, "rhs_register": 21},
            },
            {"instruction": "POP", "metadata": {"id": 61}},
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 69, "register": 22, "value": 1, "type": "int"},
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 70, "register": 23, "value": 2, "type": "int"},
            },
            {
                "instruction": "CALL",
                "metadata": {
                    "id": 68,
                    "register": 24,
                    "value": 3,
                    "type": "int",
                    "parameters_registers": [22, 23],
                },
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 74, "register": 25, "value": 6, "type": "float"},
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 76, "register": 26, "value": 5, "type": "int"},
            },
            {
                "instruction": "SITOFP",
                "metadata": {"source_register": 26, "destination_register": 27},
            },
            {
                "instruction": "FADD",
                "metadata": {
                    "id": 75,
                    "register": 28,
                    "lhs_register": 25,
                    "rhs_register": 27,
                },
            },
            {"instruction": "POP", "metadata": {"id": 73}},
            {"instruction": "RET", "metadata": {"id": 72, "register": 28}},
        ],
        "main": [
            {"instruction": "SEQ", "metadata": {}},
            {
                "instruction": "ALLOC",
                "metadata": {
                    "id": 80,
                    "register": 2,
                    "type": "int",
                    "relative_position": 3,
                    "length": 1,
                },
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 85, "register": 3, "value": 3, "type": "int"},
            },
            {
                "instruction": "CALL",
                "metadata": {
                    "id": 87,
                    "register": 4,
                    "value": 3,
                    "type": "int",
                    "parameters_registers": [],
                },
            },
            {
                "instruction": "STORE",
                "metadata": {"id": 86, "lhs_register": 3, "rhs_register": 4},
            },
            {"instruction": "POP", "metadata": {"id": 84}},
            {
                "instruction": "ALLOC",
                "metadata": {
                    "id": 89,
                    "register": 5,
                    "type": "int",
                    "relative_position": 4,
                    "length": 10,
                },
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 94, "register": 6, "value": 4, "type": "int"},
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 96, "register": 7, "value": 5, "type": "int"},
            },
            {
                "instruction": "ELEMENT_PTR",
                "metadata": {
                    "id": 95,
                    "register": 8,
                    "variable_register": 6,
                    "element_register": 7,
                },
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 98, "register": 9, "value": 1, "type": "int"},
            },
            {
                "instruction": "STORE",
                "metadata": {"id": 97, "lhs_register": 8, "rhs_register": 9},
            },
            {"instruction": "POP", "metadata": {"id": 93}},
            {
                "instruction": "ALLOC",
                "metadata": {
                    "id": 100,
                    "register": 10,
                    "type": "int",
                    "relative_position": 5,
                    "length": 1,
                },
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 105, "register": 11, "value": 3, "type": "int"},
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 107, "register": 12, "value": 4, "type": "int"},
            },
            {
                "instruction": "LSHIFT",
                "metadata": {
                    "id": 106,
                    "register": 13,
                    "lhs_register": 11,
                    "rhs_register": 12,
                },
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 109, "register": 14, "value": 1, "type": "int"},
            },
            {
                "instruction": "EQ",
                "metadata": {
                    "id": 108,
                    "register": 15,
                    "lhs_register": 13,
                    "rhs_register": 14,
                },
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 111, "register": 16, "value": 3, "type": "int"},
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 113, "register": 17, "value": 1, "type": "int"},
            },
            {
                "instruction": "GT",
                "metadata": {
                    "id": 112,
                    "register": 18,
                    "lhs_register": 16,
                    "rhs_register": 17,
                },
            },
            {
                "instruction": "OR",
                "metadata": {
                    "id": 110,
                    "register": 19,
                    "lhs_register": 15,
                    "rhs_register": 18,
                },
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 115, "register": 20, "value": 3, "type": "int"},
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 117, "register": 21, "value": 10, "type": "int"},
            },
            {
                "instruction": "LT",
                "metadata": {
                    "id": 116,
                    "register": 22,
                    "lhs_register": 20,
                    "rhs_register": 21,
                },
            },
            {
                "instruction": "AND",
                "metadata": {
                    "id": 114,
                    "register": 23,
                    "lhs_register": 19,
                    "rhs_register": 22,
                },
            },
            {"instruction": "JZ", "metadata": {"jump_size": 9}},
            {"instruction": "SEQ", "metadata": {}},
            {
                "instruction": "FETCH",
                "metadata": {"id": 121, "register": 24, "value": 5, "type": "int"},
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 123, "register": 25, "value": 3, "type": "int"},
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 125, "register": 26, "value": 1, "type": "int"},
            },
            {
                "instruction": "BITAND",
                "metadata": {
                    "id": 124,
                    "register": 27,
                    "lhs_register": 25,
                    "rhs_register": 26,
                },
            },
            {
                "instruction": "STORE",
                "metadata": {"id": 122, "lhs_register": 24, "rhs_register": 27},
            },
            {"instruction": "POP", "metadata": {"id": 120}},
            {"instruction": "JMP", "metadata": {"jump_size": 8}},
            {"instruction": "SEQ", "metadata": {}},
            {
                "instruction": "FETCH",
                "metadata": {"id": 129, "register": 28, "value": 5, "type": "int"},
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 131, "register": 29, "value": 3, "type": "int"},
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 133, "register": 30, "value": 1, "type": "int"},
            },
            {
                "instruction": "BITOR",
                "metadata": {
                    "id": 132,
                    "register": 31,
                    "lhs_register": 29,
                    "rhs_register": 30,
                },
            },
            {
                "instruction": "STORE",
                "metadata": {"id": 130, "lhs_register": 28, "rhs_register": 31},
            },
            {"instruction": "POP", "metadata": {"id": 128}},
            {
                "instruction": "FETCH",
                "metadata": {"id": 137, "register": 32, "value": 3, "type": "int"},
            },
            {
                "instruction": "FETCH",
                "metadata": {"id": 139, "register": 33, "value": 5, "type": "int"},
            },
            {
                "instruction": "MULT",
                "metadata": {
                    "id": 138,
                    "register": 34,
                    "lhs_register": 32,
                    "rhs_register": 33,
                },
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 141, "register": 35, "value": 2, "type": "int"},
            },
            {
                "instruction": "DIV",
                "metadata": {
                    "id": 140,
                    "register": 36,
                    "lhs_register": 34,
                    "rhs_register": 35,
                },
            },
            {
                "instruction": "CONSTANT",
                "metadata": {"id": 143, "register": 37, "value": 1, "type": "int"},
            },
            {
                "instruction": "RSHIFT",
                "metadata": {
                    "id": 142,
                    "register": 38,
                    "lhs_register": 36,
                    "rhs_register": 37,
                },
            },
            {"instruction": "POP", "metadata": {"id": 136}},
            {"instruction": "RET", "metadata": {"id": 135, "register": 38}},
        ],
    },
}

