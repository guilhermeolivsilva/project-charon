"""Implement unit tests for the `src.abstract_syntax_tree.AbstractSyntaxTree` class."""

from pytest import fixture

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.ast_nodes.basic.PROG import PROG


SOURCE_CODE = {
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

EXPECTED_PRINT_TREE = """
ID: 0, Value: None, Kind: PROG
  ID: 1, Value: 1, Kind: STRUCT_DEF
   Attributes: int, float
  ID: 2, Value: 2, Kind: STRUCT_DEF
   Attributes: int, int
  ID: 3, Value: 1, Kind: VAR_DEF
    Name: a, Type: int (array), Length: 10
  ID: 4, Value: 2, Kind: VAR_DEF
    Name: global_var, Type: my_struct
  ID: function_that_returns_struct, Value: None, Kind: FUNC_DEF, Type: my_struct
    ID: 11, Value: None, Kind: SEQ
      ID: 8, Value: 5, Kind: VAR_DEF
        Name: internal_guy, Type: int
      ID: 12, Value: None, Kind: RET_SYM
        ID: 13, Value: None, Kind: EXPR
          ID: 15, Value: None, Kind: ADD, Type: int
            ID: 14, Value: 3, Kind: VAR, Type: int
            ID: 16, Value: 4, Kind: VAR, Type: int
  ID: some_simple_function, Value: None, Kind: FUNC_DEF, Type: int
    ID: 19, Value: None, Kind: SEQ
      ID: 20, Value: None, Kind: RET_SYM
        ID: 21, Value: None, Kind: EXPR
          ID: 23, Value: None, Kind: DIV, Type: float
            ID: 22, Value: 3, Kind: VAR, Type: float
            ID: 24, Value: 4, Kind: VAR, Type: int
  ID: abc, Value: None, Kind: FUNC_DEF, Type: int
    ID: 71, Value: None, Kind: SEQ
      ID: 28, Value: 5, Kind: VAR_DEF
        Name: bla, Type: int
      ID: 32, Value: None, Kind: EXPR
        ID: 34, Value: None, Kind: ASSIGN, Type: int
          ID: 33, Value: 5, Kind: VAR, Type: int
          ID: 35, Value: 1, Kind: CST, Type: int
      ID: 37, Value: 6, Kind: VAR_DEF
        Name: blabla, Type: float
      ID: 41, Value: None, Kind: EXPR
        ID: 43, Value: None, Kind: ASSIGN, Type: float
          ID: 42, Value: 6, Kind: VAR, Type: float
          ID: 44, Value: 2.0, Kind: CST, Type: float
      ID: 46, Value: 7, Kind: VAR_DEF
        Name: xaxaxa, Type: short
      ID: 50, Value: 8, Kind: VAR_DEF
        Name: internal_struct_var, Type: my_struct
      ID: 54, Value: None, Kind: EXPR
        ID: 58, Value: None, Kind: ASSIGN, Type: int
          ID: 56, Value: None, Kind: ELEMENT_ACCESS, Type: int
            ID: 55, Value: 8, Kind: VAR, Type: my_struct
            ID: 57, Value: 0, Kind: CST, Type: int
          ID: 59, Value: 1, Kind: CST, Type: int
      ID: 61, Value: None, Kind: EXPR
        ID: 63, Value: None, Kind: ASSIGN, Type: int
          ID: 62, Value: 5, Kind: VAR, Type: int
          ID: 65, Value: None, Kind: ADD, Type: int
            ID: 64, Value: 5, Kind: VAR, Type: int
            ID: 66, Value: 2, Kind: FUNC_CALL, Type: int
              ID: 67, Value: 6, Kind: VAR, Type: float
              ID: 68, Value: 123, Kind: CST, Type: int
      ID: 68, Value: 3, Kind: FUNC_CALL, Type: int
        ID: 69, Value: 1, Kind: CST, Type: int
        ID: 70, Value: 2, Kind: CST, Type: int
      ID: 72, Value: None, Kind: RET_SYM
        ID: 73, Value: None, Kind: EXPR
          ID: 75, Value: None, Kind: ADD, Type: float
            ID: 74, Value: 6, Kind: VAR, Type: float
            ID: 76, Value: 5, Kind: VAR, Type: int
  ID: main, Value: None, Kind: FUNC_DEF, Type: int
    ID: 134, Value: None, Kind: SEQ
      ID: 80, Value: 3, Kind: VAR_DEF
        Name: x, Type: int
      ID: 84, Value: None, Kind: EXPR
        ID: 86, Value: None, Kind: ASSIGN, Type: int
          ID: 85, Value: 3, Kind: VAR, Type: int
          ID: 87, Value: 3, Kind: FUNC_CALL, Type: int
      ID: 89, Value: 4, Kind: VAR_DEF
        Name: array, Type: int (array), Length: 10
      ID: 93, Value: None, Kind: EXPR
        ID: 97, Value: None, Kind: ASSIGN, Type: int
          ID: 95, Value: None, Kind: ELEMENT_ACCESS, Type: int
            ID: 94, Value: 4, Kind: VAR, Type: int (array), Length: 10
            ID: 96, Value: 5, Kind: CST, Type: int
          ID: 98, Value: 1, Kind: CST, Type: int
      ID: 100, Value: 5, Kind: VAR_DEF
        Name: y, Type: int
      ID: 104, Value: None, Kind: IFELSE
        ID: 114, Value: None, Kind: AND, Type: int
          ID: 110, Value: None, Kind: OR, Type: int
            ID: 108, Value: None, Kind: EQUAL, Type: int
              ID: 106, Value: None, Kind: LSHIFT, Type: int
                ID: 105, Value: 3, Kind: VAR, Type: int
                ID: 107, Value: 4, Kind: CST, Type: int
              ID: 109, Value: 1, Kind: CST, Type: int
            ID: 112, Value: None, Kind: GREATER, Type: int
              ID: 111, Value: 3, Kind: VAR, Type: int
              ID: 113, Value: 1, Kind: CST, Type: int
          ID: 116, Value: None, Kind: LESS, Type: int
            ID: 115, Value: 3, Kind: VAR, Type: int
            ID: 117, Value: 10, Kind: CST, Type: int
        ID: 119, Value: None, Kind: SEQ
          ID: 120, Value: None, Kind: EXPR
            ID: 122, Value: None, Kind: ASSIGN, Type: int
              ID: 121, Value: 5, Kind: VAR, Type: int
              ID: 124, Value: None, Kind: BITAND, Type: int
                ID: 123, Value: 3, Kind: VAR, Type: int
                ID: 125, Value: 1, Kind: CST, Type: int
        ID: 127, Value: None, Kind: SEQ
          ID: 128, Value: None, Kind: EXPR
            ID: 130, Value: None, Kind: ASSIGN, Type: int
              ID: 129, Value: 5, Kind: VAR, Type: int
              ID: 132, Value: None, Kind: BITOR, Type: int
                ID: 131, Value: 3, Kind: VAR, Type: int
                ID: 133, Value: 1, Kind: CST, Type: int
      ID: 135, Value: None, Kind: RET_SYM
        ID: 136, Value: None, Kind: EXPR
          ID: 142, Value: None, Kind: RSHIFT, Type: int
            ID: 140, Value: None, Kind: DIV, Type: int
              ID: 138, Value: None, Kind: MULT, Type: int
                ID: 137, Value: 3, Kind: VAR, Type: int
                ID: 139, Value: 5, Kind: VAR, Type: int
              ID: 141, Value: 2, Kind: CST, Type: int
            ID: 143, Value: 1, Kind: CST, Type: int
"""

def test_init() -> None:
    """Test the instantiation of AbstractSyntaxTree objects."""

    ast = AbstractSyntaxTree(source_code=SOURCE_CODE)

    assert ast.node_id_manager == 1
    assert ast.source_code == SOURCE_CODE
    assert ast.current_symbol is None
    assert ast.current_value == {}
    assert ast.root == PROG(id=0)


def test_build(capfd: fixture) -> None:
    """
    Test if the `build` method works as expected.

    To run this test, we compare the output of an auxiliary `_dfs` function
    ran on the AST to a known, expected result. This is achieved by capturing
    the console output with pytest's `capfd` fixture.
    """

    ast = AbstractSyntaxTree(source_code=SOURCE_CODE)
    ast.build()

    ast.print_tree()

    out, _ = capfd.readouterr()
    out = "\n" + out

    assert out == EXPECTED_PRINT_TREE
