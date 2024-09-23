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
                (
                    "VAR",
                    {"name": "internal_guy", "relative_position": 5, "type": "int"},
                ),
                ("ASSIGN", {}),
                ("VAR", {"type": "int", "relative_position": 3}),
                ("ADD", {}),
                ("VAR", {"type": "int", "relative_position": 4}),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "relative_position": 2,
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
                    {"name": "internal_guy", "relative_position": 5, "type": "int"},
                ),
                ("SEMI", {}),
                ("RET_SYM", {}),
                ("VAR", {"type": "my_struct", "relative_position": 2}),
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
    "structs": {"my_struct": ["int", "float"]},
    "functions": {
        "function_that_returns_struct": {"start": 2, "end": 17},
        "some_simple_function": {"start": 17, "end": 25},
        "abc": {"start": 25, "end": 58},
        "main": {"start": 58, "end": 102},
    },
    "code": [
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
        {
            "instruction": "PARAM",
            "metadata": {
                "id": None,
                "register": 2,
                "type": "int",
                "relative_position": 3,
                "length": 1,
            },
        },
        {
            "instruction": "PARAM",
            "metadata": {
                "id": None,
                "register": 3,
                "type": "int",
                "relative_position": 4,
                "length": 1,
            },
        },
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
            "instruction": "LOAD",
            "metadata": {"id": 12, "register": 5, "value": 5, "type": "int"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 14, "register": 6, "value": 3, "type": "int"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 16, "register": 7, "value": 4, "type": "int"},
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
            "metadata": {"id": 18, "register": 9, "value": 2, "type": "my_struct"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 20, "register": 10, "value": 0, "type": "int"},
        },
        {
            "instruction": "ELEMENT_PTR",
            "metadata": {
                "id": 19,
                "register": 11,
                "variable_register": 9,
                "element_register": 10,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 22, "register": 12, "value": 5, "type": "int"},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 21, "lhs_register": 11, "rhs_register": 12},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 25, "register": 13, "value": 2, "type": "my_struct"},
        },
        {
            "instruction": "RET",
            "metadata": {"id": 24, "type": "my_struct", "register": 13},
        },
        {
            "instruction": "PARAM",
            "metadata": {
                "id": None,
                "register": 2,
                "type": "float",
                "relative_position": 3,
                "length": 1,
            },
        },
        {
            "instruction": "PARAM",
            "metadata": {
                "id": None,
                "register": 3,
                "type": "int",
                "relative_position": 4,
                "length": 1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 30, "register": 4, "value": 3, "type": "float"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 32, "register": 5, "value": 4, "type": "int"},
        },
        {
            "instruction": "SITOFP",
            "metadata": {"source_register": 5, "destination_register": 6},
        },
        {
            "instruction": "FDIV",
            "metadata": {"id": 31, "register": 7, "lhs_register": 4, "rhs_register": 6},
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"source_register": 7, "destination_register": 8},
        },
        {"instruction": "RET", "metadata": {"id": 29, "type": "int", "register": 8}},
        {
            "instruction": "PARAM",
            "metadata": {
                "id": None,
                "register": 2,
                "type": "int",
                "relative_position": 3,
                "length": 1,
            },
        },
        {
            "instruction": "PARAM",
            "metadata": {
                "id": None,
                "register": 3,
                "type": "int",
                "relative_position": 4,
                "length": 1,
            },
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "id": 36,
                "register": 4,
                "type": "int",
                "relative_position": 5,
                "length": 1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 40, "register": 5, "value": 5, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 42, "register": 6, "value": 1, "type": "int"},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 41, "lhs_register": 5, "rhs_register": 6},
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "id": 44,
                "register": 7,
                "type": "float",
                "relative_position": 6,
                "length": 1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 48, "register": 8, "value": 6, "type": "float"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 50, "register": 9, "value": 2.0, "type": "float"},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 49, "lhs_register": 8, "rhs_register": 9},
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "id": 52,
                "register": 10,
                "type": "short",
                "relative_position": 7,
                "length": 1,
            },
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "id": 56,
                "register": 11,
                "type": "my_struct",
                "relative_position": 8,
                "length": 1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 60, "register": 12, "value": 8, "type": "my_struct"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 62, "register": 13, "value": 0, "type": "int"},
        },
        {
            "instruction": "ELEMENT_PTR",
            "metadata": {
                "id": 61,
                "register": 14,
                "variable_register": 12,
                "element_register": 13,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 64, "register": 15, "value": 1, "type": "int"},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 63, "lhs_register": 14, "rhs_register": 15},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 66, "register": 16, "value": 5, "type": "int"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 68, "register": 17, "value": 5, "type": "int"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 71, "register": 18, "value": 6, "type": "float"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 72, "register": 19, "value": 123, "type": "int"},
        },
        {
            "instruction": "CALL",
            "metadata": {
                "id": 70,
                "register": 20,
                "value": 2,
                "type": "int",
                "parameters_registers": [18, 19],
            },
        },
        {
            "instruction": "ADD",
            "metadata": {
                "id": 69,
                "register": 21,
                "lhs_register": 17,
                "rhs_register": 20,
            },
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 67, "lhs_register": 16, "rhs_register": 21},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 73, "register": 22, "value": 1, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 74, "register": 23, "value": 2, "type": "int"},
        },
        {
            "instruction": "CALL",
            "metadata": {
                "id": 72,
                "register": 24,
                "value": 3,
                "type": "int",
                "parameters_registers": [22, 23],
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 77, "register": 25, "value": 6, "type": "float"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 79, "register": 26, "value": 5, "type": "int"},
        },
        {
            "instruction": "SITOFP",
            "metadata": {"source_register": 26, "destination_register": 27},
        },
        {
            "instruction": "FADD",
            "metadata": {
                "id": 78,
                "register": 28,
                "lhs_register": 25,
                "rhs_register": 27,
            },
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"source_register": 28, "destination_register": 29},
        },
        {"instruction": "RET", "metadata": {"id": 76, "type": "int", "register": 29}},
        {
            "instruction": "ALLOC",
            "metadata": {
                "id": 83,
                "register": 2,
                "type": "int",
                "relative_position": 3,
                "length": 1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 87, "register": 3, "value": 3, "type": "int"},
        },
        {
            "instruction": "CALL",
            "metadata": {
                "id": 89,
                "register": 4,
                "value": 3,
                "type": "int",
                "parameters_registers": [],
            },
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 88, "lhs_register": 3, "rhs_register": 4},
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "id": 91,
                "register": 5,
                "type": "int",
                "relative_position": 4,
                "length": 10,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 95, "register": 6, "value": 4, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 97, "register": 7, "value": 5, "type": "int"},
        },
        {
            "instruction": "ELEMENT_PTR",
            "metadata": {
                "id": 96,
                "register": 8,
                "variable_register": 6,
                "element_register": 7,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 99, "register": 9, "value": 1, "type": "int"},
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 98, "lhs_register": 8, "rhs_register": 9},
        },
        {
            "instruction": "ALLOC",
            "metadata": {
                "id": 101,
                "register": 10,
                "type": "int",
                "relative_position": 5,
                "length": 1,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 106, "register": 11, "value": 3, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 108, "register": 12, "value": 4, "type": "int"},
        },
        {
            "instruction": "LSHIFT",
            "metadata": {
                "id": 107,
                "register": 13,
                "lhs_register": 11,
                "rhs_register": 12,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 110, "register": 14, "value": 1, "type": "int"},
        },
        {
            "instruction": "EQ",
            "metadata": {
                "id": 109,
                "register": 15,
                "lhs_register": 13,
                "rhs_register": 14,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 112, "register": 16, "value": 3, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 114, "register": 17, "value": 1, "type": "int"},
        },
        {
            "instruction": "GT",
            "metadata": {
                "id": 113,
                "register": 18,
                "lhs_register": 16,
                "rhs_register": 17,
            },
        },
        {
            "instruction": "OR",
            "metadata": {
                "id": 111,
                "register": 19,
                "lhs_register": 15,
                "rhs_register": 18,
            },
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 116, "register": 20, "value": 3, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 118, "register": 21, "value": 10, "type": "int"},
        },
        {
            "instruction": "LT",
            "metadata": {
                "id": 117,
                "register": 22,
                "lhs_register": 20,
                "rhs_register": 21,
            },
        },
        {
            "instruction": "AND",
            "metadata": {
                "id": 115,
                "register": 23,
                "lhs_register": 19,
                "rhs_register": 22,
            },
        },
        {"instruction": "JZ", "metadata": {"jump_size": 7}},
        {
            "instruction": "LOAD",
            "metadata": {"id": 121, "register": 24, "value": 5, "type": "int"},
        },
        {
            "instruction": "LOAD",
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
        {"instruction": "JMP", "metadata": {"jump_size": 6}},
        {
            "instruction": "LOAD",
            "metadata": {"id": 128, "register": 28, "value": 5, "type": "int"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 130, "register": 29, "value": 3, "type": "int"},
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 132, "register": 30, "value": 1, "type": "int"},
        },
        {
            "instruction": "BITOR",
            "metadata": {
                "id": 131,
                "register": 31,
                "lhs_register": 29,
                "rhs_register": 30,
            },
        },
        {
            "instruction": "STORE",
            "metadata": {"id": 129, "lhs_register": 28, "rhs_register": 31},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 135, "register": 32, "value": 3, "type": "int"},
        },
        {
            "instruction": "LOAD",
            "metadata": {"id": 137, "register": 33, "value": 5, "type": "int"},
        },
        {
            "instruction": "MULT",
            "metadata": {
                "id": 136,
                "register": 34,
                "lhs_register": 32,
                "rhs_register": 33,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 139, "register": 35, "value": 2, "type": "int"},
        },
        {
            "instruction": "DIV",
            "metadata": {
                "id": 138,
                "register": 36,
                "lhs_register": 34,
                "rhs_register": 35,
            },
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"id": 141, "register": 37, "value": 1, "type": "int"},
        },
        {
            "instruction": "RSHIFT",
            "metadata": {
                "id": 140,
                "register": 38,
                "lhs_register": 36,
                "rhs_register": 37,
            },
        },
        {"instruction": "RET", "metadata": {"id": 134, "type": "int", "register": 38}},
    ],
}

first_function_indices = next(iter(MACHINE_CODE["functions"].values()))
GLOBAL_VARS_COUNT = first_function_indices["start"]
