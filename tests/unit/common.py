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
                "attributes": {
                    "x": {"type": "int", "attr_pointer": 0},
                    "y": {"type": "float", "attr_pointer": 1},
                },
                "active": True,
            },
            "test_struct": {
                "id": 2,
                "attributes": {
                    "abcd": {"type": "int", "attr_pointer": 0},
                    "xyz": {"type": "int", "attr_pointer": 1},
                },
                "active": False,
            },
        },
        "variables": {
            "a": {"type": "int", "length": 10, "id": 1},
            "global_var": {
                "type": "my_struct",
                "attributes": {
                    "x": {"type": "int", "attr_pointer": 0},
                    "y": {"type": "float", "attr_pointer": 1},
                },
                "id": 2,
            },
        },
    },
    "functions": {
        "function_that_returns_struct": {
            "id": 1,
            "prime": 2,
            "type": "my_struct",
            "parameters": {
                "xyz": {"type": "int", "id": 3},
                "aaa": {"type": "int", "id": 4},
            },
            "statements": [
                ("LCBRA", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "internal_guy",
                        "id": 5,
                        "type": "int",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "name": "internal_guy",
                        "id": 5,
                        "type": "int",
                    },
                ),
                ("ASSIGN", {}),
                ("VAR", {"type": "int", "id": 3}),
                ("ADD", {}),
                ("VAR", {"type": "int", "id": 4}),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "id": 2,
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
                "param_1": {"type": "float", "id": 6},
                "param_2": {"type": "int", "id": 7},
            },
            "statements": [
                ("LCBRA", {}),
                ("RET_SYM", {}),
                ("VAR", {"type": "float", "id": 6}),
                ("DIV", {}),
                ("VAR", {"type": "int", "id": 7}),
                ("SEMI", {}),
                ("RCBRA", {}),
            ],
        },
        "abc": {
            "id": 3,
            "prime": 5,
            "type": "int",
            "parameters": {
                "asda": {"type": "int", "id": 8},
                "abcdef": {"type": "int", "id": 9},
            },
            "statements": [
                ("LCBRA", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "bla",
                        "id": 10,
                        "type": "int",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "name": "bla",
                        "id": 10,
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
                        "type": "float",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "name": "blabla",
                        "id": 11,
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
                        "type": "short",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "internal_struct_var",
                        "id": 13,
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
                        "type": "int",
                    },
                ),
                ("ASSIGN", {}),
                (
                    "VAR",
                    {
                        "name": "bla",
                        "id": 10,
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
                                },
                                "param_2": {
                                    "type": "int",
                                    "id": 7,
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
                                    },
                                ),
                                ("DIV", {}),
                                (
                                    "VAR",
                                    {
                                        "type": "int",
                                        "id": 7,
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
                        "type": "float",
                    },
                ),
                ("ADD", {}),
                (
                    "VAR",
                    {
                        "name": "bla",
                        "id": 10,
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
                    {"name": "x", "id": 14, "type": "int"},
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {"name": "x", "id": 14, "type": "int"},
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
                                },
                                "abcdef": {
                                    "type": "int",
                                    "id": 9,
                                },
                            },
                            "statements": [
                                ("LCBRA", {}),
                                (
                                    "VAR_DEF",
                                    {
                                        "name": "bla",
                                        "id": 10,
                                        "type": "int",
                                    },
                                ),
                                ("SEMI", {}),
                                (
                                    "VAR",
                                    {
                                        "name": "bla",
                                        "id": 10,
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
                                        "type": "float",
                                    },
                                ),
                                ("SEMI", {}),
                                (
                                    "VAR",
                                    {
                                        "name": "blabla",
                                        "id": 11,
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
                                        "type": "short",
                                    },
                                ),
                                ("SEMI", {}),
                                (
                                    "VAR_DEF",
                                    {
                                        "name": "internal_struct_var",
                                        "id": 13,
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
                                        "type": "int",
                                    },
                                ),
                                ("ASSIGN", {}),
                                (
                                    "VAR",
                                    {
                                        "name": "bla",
                                        "id": 10,
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
                                                },
                                                "param_2": {
                                                    "type": "int",
                                                    "id": 7,
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
                                                    },
                                                ),
                                                ("DIV", {}),
                                                (
                                                    "VAR",
                                                    {
                                                        "type": "int",
                                                        "id": 7,
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
                                        "type": "float",
                                    },
                                ),
                                ("ADD", {}),
                                (
                                    "VAR",
                                    {
                                        "name": "bla",
                                        "id": 10,
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
                    {"name": "y", "id": 16, "type": "int"},
                ),
                ("SEMI", {}),
                ("IF_SYM", {}),
                ("LPAR", {}),
                ("LPAR", {}),
                ("LPAR", {}),
                ("LPAR", {}),
                (
                    "VAR",
                    {"name": "x", "id": 14, "type": "int"},
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
                    {"name": "x", "id": 14, "type": "int"},
                ),
                ("GREATER", {}),
                ("CST", {"type": "int", "value": 1}),
                ("RPAR", {}),
                ("RPAR", {}),
                ("AND", {}),
                ("LPAR", {}),
                (
                    "VAR",
                    {"name": "x", "id": 14, "type": "int"},
                ),
                ("LESS", {}),
                ("CST", {"type": "int", "value": 10}),
                ("RPAR", {}),
                ("RPAR", {}),
                ("LCBRA", {}),
                (
                    "VAR",
                    {"name": "y", "id": 16, "type": "int"},
                ),
                ("ASSIGN", {}),
                (
                    "VAR",
                    {"name": "x", "id": 14, "type": "int"},
                ),
                ("BITAND", {}),
                ("CST", {"type": "int", "value": 1}),
                ("SEMI", {}),
                ("RCBRA", {}),
                ("ELSE_SYM", {}),
                ("LCBRA", {}),
                (
                    "VAR",
                    {"name": "y", "id": 16, "type": "int"},
                ),
                ("ASSIGN", {}),
                (
                    "VAR",
                    {"name": "x", "id": 14, "type": "int"},
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
                    {"name": "x", "id": 14, "type": "int"},
                ),
                ("MULT", {}),
                (
                    "VAR",
                    {"name": "y", "id": 16, "type": "int"},
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
        "function_that_returns_struct": {"start": 0, "end": 27},
        "some_simple_function": {"start": 27, "end": 42},
        "abc": {"start": 42, "end": 86},
        "main": {"start": 86, "end": 151},
    },
    "global_vars": [],
    "data": {
        "0x0": 40,
        "0x28": 8,
        "0x30": 4,
        "0x34": 4,
        "0x38": 4,
        "0x3c": 4,
        "0x40": 4,
        "0x44": 4,
        "0x48": 4,
        "0x4c": 4,
        "0x50": 4,
        "0x54": 4,
        "0x58": 8,
        "0x60": 4,
        "0x64": 40,
        "0x8c": 4,
    },
    "code": [
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 0, "value": "0x30"},
            "bytecode_id": 1,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 0, "value": "arg"},
            "bytecode_id": 2,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 1, "value": "0x34"},
            "bytecode_id": 3,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 1, "value": "arg"},
            "bytecode_id": 4,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 2, "value": "0x38"},
            "bytecode_id": 5,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 3, "lhs_register": 2, "rhs_register": "zero"},
            "bytecode_id": 6,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 4, "value": "0x30"},
            "bytecode_id": 7,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 5, "lhs_register": 4, "rhs_register": "zero"},
            "bytecode_id": 8,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 6, "value": 5},
            "bytecode_id": 9,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 7, "value": "0x34"},
            "bytecode_id": 10,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 8, "lhs_register": 7, "rhs_register": "zero"},
            "bytecode_id": 11,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 9, "value": 8},
            "bytecode_id": 12,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 10, "lhs_register": 6, "rhs_register": 9},
            "bytecode_id": 13,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 3, "value": 10},
            "bytecode_id": 14,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 12, "value": "0x28"},
            "bytecode_id": 15,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 13, "lhs_register": 12, "rhs_register": "zero"},
            "bytecode_id": 16,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 14, "value": 0},
            "bytecode_id": 17,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 15, "lhs_register": 13, "rhs_register": 14},
            "bytecode_id": 18,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 16, "value": "0x38"},
            "bytecode_id": 19,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 17, "lhs_register": 16, "rhs_register": "zero"},
            "bytecode_id": 20,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 18, "value": 17},
            "bytecode_id": 21,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 15, "value": 18},
            "bytecode_id": 22,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 20, "value": "0x28"},
            "bytecode_id": 23,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 21, "lhs_register": 20, "rhs_register": "zero"},
            "bytecode_id": 24,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 22, "value": 21},
            "bytecode_id": 25,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 22},
            "bytecode_id": 26,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "bytecode_id": 27,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 23, "value": "0x3c"},
            "bytecode_id": 28,
        },
        {
            "instruction": "STOREF",
            "metadata": {"register": 23, "value": "arg"},
            "bytecode_id": 29,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 24, "value": "0x40"},
            "bytecode_id": 30,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 24, "value": "arg"},
            "bytecode_id": 31,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 25, "value": "0x3c"},
            "bytecode_id": 32,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 26, "lhs_register": 25, "rhs_register": "zero"},
            "bytecode_id": 33,
        },
        {
            "instruction": "LOADF",
            "metadata": {"register": 27, "value": 26},
            "bytecode_id": 34,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 28, "value": "0x40"},
            "bytecode_id": 35,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 29, "lhs_register": 28, "rhs_register": "zero"},
            "bytecode_id": 36,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 30, "value": 29},
            "bytecode_id": 37,
        },
        {
            "instruction": "SITOFP",
            "metadata": {"register": 31, "value": 30},
            "bytecode_id": 38,
        },
        {
            "instruction": "FDIV",
            "metadata": {"register": 32, "lhs_register": 27, "rhs_register": 31},
            "bytecode_id": 39,
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"register": 33, "value": 32},
            "bytecode_id": 40,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 33},
            "bytecode_id": 41,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "bytecode_id": 42,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 34, "value": "0x44"},
            "bytecode_id": 43,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 34, "value": "arg"},
            "bytecode_id": 44,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 35, "value": "0x48"},
            "bytecode_id": 45,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 35, "value": "arg"},
            "bytecode_id": 46,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 36, "value": "0x4c"},
            "bytecode_id": 47,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 37, "lhs_register": 36, "rhs_register": "zero"},
            "bytecode_id": 48,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 38, "value": 1},
            "bytecode_id": 49,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 37, "value": 38},
            "bytecode_id": 50,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 40, "value": "0x50"},
            "bytecode_id": 51,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 41, "lhs_register": 40, "rhs_register": "zero"},
            "bytecode_id": 52,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 42, "value": 2.0},
            "bytecode_id": 53,
        },
        {
            "instruction": "STOREF",
            "metadata": {"register": 41, "value": 42},
            "bytecode_id": 54,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 44, "value": "0x58"},
            "bytecode_id": 55,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 45, "lhs_register": 44, "rhs_register": "zero"},
            "bytecode_id": 56,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 46, "value": 0},
            "bytecode_id": 57,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 47, "lhs_register": 45, "rhs_register": 46},
            "bytecode_id": 58,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 48, "value": 1},
            "bytecode_id": 59,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 47, "value": 48},
            "bytecode_id": 60,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 50, "value": "0x4c"},
            "bytecode_id": 61,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 51, "lhs_register": 50, "rhs_register": "zero"},
            "bytecode_id": 62,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 52, "value": "0x4c"},
            "bytecode_id": 63,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 53, "lhs_register": 52, "rhs_register": "zero"},
            "bytecode_id": 64,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 54, "value": 53},
            "bytecode_id": 65,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 55, "value": "0x50"},
            "bytecode_id": 66,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 56, "lhs_register": 55, "rhs_register": "zero"},
            "bytecode_id": 67,
        },
        {
            "instruction": "LOADF",
            "metadata": {"register": 57, "value": 56},
            "bytecode_id": 68,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 57},
            "bytecode_id": 69,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 58, "value": 123},
            "bytecode_id": 70,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 58},
            "bytecode_id": 71,
        },
        {"instruction": "JAL", "metadata": {"value": 2}, "bytecode_id": 72},
        {
            "instruction": "MOV",
            "metadata": {"register": 59, "value": "ret_value"},
            "bytecode_id": 73,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 60, "lhs_register": 54, "rhs_register": 59},
            "bytecode_id": 74,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 51, "value": 60},
            "bytecode_id": 75,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 62, "value": "0x50"},
            "bytecode_id": 76,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 63, "lhs_register": 62, "rhs_register": "zero"},
            "bytecode_id": 77,
        },
        {
            "instruction": "LOADF",
            "metadata": {"register": 64, "value": 63},
            "bytecode_id": 78,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 65, "value": "0x4c"},
            "bytecode_id": 79,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 66, "lhs_register": 65, "rhs_register": "zero"},
            "bytecode_id": 80,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 67, "value": 66},
            "bytecode_id": 81,
        },
        {
            "instruction": "SITOFP",
            "metadata": {"register": 68, "value": 67},
            "bytecode_id": 82,
        },
        {
            "instruction": "FADD",
            "metadata": {"register": 69, "lhs_register": 64, "rhs_register": 68},
            "bytecode_id": 83,
        },
        {
            "instruction": "FPTOSI",
            "metadata": {"register": 70, "value": 69},
            "bytecode_id": 84,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 70},
            "bytecode_id": 85,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "bytecode_id": 86,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 71, "value": "0x60"},
            "bytecode_id": 87,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 72, "lhs_register": 71, "rhs_register": "zero"},
            "bytecode_id": 88,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 73, "value": 1},
            "bytecode_id": 89,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 73},
            "bytecode_id": 90,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 74, "value": 2},
            "bytecode_id": 91,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "arg", "value": 74},
            "bytecode_id": 92,
        },
        {"instruction": "JAL", "metadata": {"value": 3}, "bytecode_id": 93},
        {
            "instruction": "MOV",
            "metadata": {"register": 75, "value": "ret_value"},
            "bytecode_id": 94,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 72, "value": 75},
            "bytecode_id": 95,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 77, "value": "0x64"},
            "bytecode_id": 96,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 78, "lhs_register": 77, "rhs_register": "zero"},
            "bytecode_id": 97,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 79, "value": 20},
            "bytecode_id": 98,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 80, "lhs_register": 78, "rhs_register": 79},
            "bytecode_id": 99,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 81, "value": 1},
            "bytecode_id": 100,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 80, "value": 81},
            "bytecode_id": 101,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 83, "value": "0x60"},
            "bytecode_id": 102,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 84, "lhs_register": 83, "rhs_register": "zero"},
            "bytecode_id": 103,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 85, "value": 84},
            "bytecode_id": 104,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 86, "value": 4},
            "bytecode_id": 105,
        },
        {
            "instruction": "LSHIFT",
            "metadata": {"register": 87, "lhs_register": 85, "rhs_register": 86},
            "bytecode_id": 106,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 88, "value": 1},
            "bytecode_id": 107,
        },
        {
            "instruction": "EQ",
            "metadata": {"register": 89, "lhs_register": 87, "rhs_register": 88},
            "bytecode_id": 108,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 90, "value": "0x60"},
            "bytecode_id": 109,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 91, "lhs_register": 90, "rhs_register": "zero"},
            "bytecode_id": 110,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 92, "value": 91},
            "bytecode_id": 111,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 93, "value": 1},
            "bytecode_id": 112,
        },
        {
            "instruction": "GT",
            "metadata": {"register": 94, "lhs_register": 92, "rhs_register": 93},
            "bytecode_id": 113,
        },
        {
            "instruction": "OR",
            "metadata": {"register": 95, "lhs_register": 89, "rhs_register": 94},
            "bytecode_id": 114,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 96, "value": "0x60"},
            "bytecode_id": 115,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 97, "lhs_register": 96, "rhs_register": "zero"},
            "bytecode_id": 116,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 98, "value": 97},
            "bytecode_id": 117,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 99, "value": 10},
            "bytecode_id": 118,
        },
        {
            "instruction": "LT",
            "metadata": {"register": 100, "lhs_register": 98, "rhs_register": 99},
            "bytecode_id": 119,
        },
        {
            "instruction": "AND",
            "metadata": {"register": 101, "lhs_register": 95, "rhs_register": 100},
            "bytecode_id": 120,
        },
        {
            "instruction": "JZ",
            "metadata": {"conditional_register": 101, "jump_size": 10},
            "bytecode_id": 121,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 102, "value": "0x8c"},
            "bytecode_id": 122,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 103, "lhs_register": 102, "rhs_register": "zero"},
            "bytecode_id": 123,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 104, "value": "0x60"},
            "bytecode_id": 124,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 105, "lhs_register": 104, "rhs_register": "zero"},
            "bytecode_id": 125,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 106, "value": 105},
            "bytecode_id": 126,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 107, "value": 1},
            "bytecode_id": 127,
        },
        {
            "instruction": "BITAND",
            "metadata": {"register": 108, "lhs_register": 106, "rhs_register": 107},
            "bytecode_id": 128,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 103, "value": 108},
            "bytecode_id": 129,
        },
        {
            "instruction": "JZ",
            "metadata": {"conditional_register": "zero", "jump_size": 9},
            "bytecode_id": 130,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 110, "value": "0x8c"},
            "bytecode_id": 131,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 111, "lhs_register": 110, "rhs_register": "zero"},
            "bytecode_id": 132,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 112, "value": "0x60"},
            "bytecode_id": 133,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 113, "lhs_register": 112, "rhs_register": "zero"},
            "bytecode_id": 134,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 114, "value": 113},
            "bytecode_id": 135,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 115, "value": 1},
            "bytecode_id": 136,
        },
        {
            "instruction": "BITOR",
            "metadata": {"register": 116, "lhs_register": 114, "rhs_register": 115},
            "bytecode_id": 137,
        },
        {
            "instruction": "STORE",
            "metadata": {"register": 111, "value": 116},
            "bytecode_id": 138,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 118, "value": "0x60"},
            "bytecode_id": 139,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 119, "lhs_register": 118, "rhs_register": "zero"},
            "bytecode_id": 140,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 120, "value": 119},
            "bytecode_id": 141,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 121, "value": "0x8c"},
            "bytecode_id": 142,
        },
        {
            "instruction": "ADD",
            "metadata": {"register": 122, "lhs_register": 121, "rhs_register": "zero"},
            "bytecode_id": 143,
        },
        {
            "instruction": "LOAD",
            "metadata": {"register": 123, "value": 122},
            "bytecode_id": 144,
        },
        {
            "instruction": "MULT",
            "metadata": {"register": 124, "lhs_register": 120, "rhs_register": 123},
            "bytecode_id": 145,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 125, "value": 2},
            "bytecode_id": 146,
        },
        {
            "instruction": "DIV",
            "metadata": {"register": 126, "lhs_register": 124, "rhs_register": 125},
            "bytecode_id": 147,
        },
        {
            "instruction": "CONSTANT",
            "metadata": {"register": 127, "value": 1},
            "bytecode_id": 148,
        },
        {
            "instruction": "RSHIFT",
            "metadata": {"register": 128, "lhs_register": 126, "rhs_register": 127},
            "bytecode_id": 149,
        },
        {
            "instruction": "MOV",
            "metadata": {"register": "ret_value", "value": 128},
            "bytecode_id": 150,
        },
        {
            "instruction": "JR",
            "metadata": {"register": "ret_address"},
            "bytecode_id": 151,
        },
        {"instruction": "HALT", "metadata": {}, "bytecode_id": 152},
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
