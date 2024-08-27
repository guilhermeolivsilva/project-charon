"""Implement unit tests for the `src.abstract_syntax_tree.AbstractSyntaxTree` class."""

from pytest import fixture

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.ast_nodes.basic.PROG import PROG


SOURCE_CODE = {
    "globals": {
        "structs": {
            "my_struct": {
                "pseudonymous": "%struct.1",
                "attributes": {
                    "x": {"type": "int", "attr_pointer": 1, "type_pseudonymous": "2"},
                    "y": {"type": "float", "attr_pointer": 2, "type_pseudonymous": "3"},
                },
                "active": True,
            },
            "test_struct": {
                "pseudonymous": "%struct.2",
                "attributes": {
                    "abcd": {
                        "type": "int",
                        "attr_pointer": 1,
                        "type_pseudonymous": "2",
                    },
                    "xyz": {"type": "int", "attr_pointer": 2, "type_pseudonymous": "2"},
                },
                "active": False,
            },
        },
        "variables": {
            "a": {"type": "int", "type_pseudonymous": "2", "pseudonymous": "%1"},
            "global_var": {
                "type": "my_struct",
                "type_pseudonymous": "%struct.1",
                "pseudonymous": "%2",
            },
        },
    },
    "functions": {
        "abc": {
            "pseudonymous": "#1",
            "type": "int",
            "arguments": {
                "asda": {"type": "int", "pseudonymous": "%3"},
                "abcdef": {"type": "int", "pseudonymous": "%4"},
            },
            "statements": [
                ("LCBRA", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "bla",
                        "pseudonymous": "%5",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "name": "bla",
                        "pseudonymous": "%5",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
                ),
                ("ASSIGN", {}),
                ("CST", {"type": "int", "value": 1}),
                ("SEMI", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "blabla",
                        "pseudonymous": "%6",
                        "type": "float",
                        "type_pseudonymous": "3",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "name": "blabla",
                        "pseudonymous": "%6",
                        "type": "float",
                        "type_pseudonymous": "3",
                    },
                ),
                ("ASSIGN", {}),
                ("CST", {"type": "float", "value": 2.0}),
                ("SEMI", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "xaxaxa",
                        "pseudonymous": "%7",
                        "type": "short",
                        "type_pseudonymous": "4",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "internal_struct_var",
                        "pseudonymous": "%8",
                        "type": "my_struct",
                        "type_pseudonymous": "%struct.1",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "name": "internal_struct_var",
                        "pseudonymous": "%8",
                        "type": "my_struct",
                        "type_pseudonymous": "%struct.1",
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
                        "pseudonymous": "%5",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
                ),
                ("ASSIGN", {}),
                (
                    "VAR",
                    {
                        "name": "bla",
                        "pseudonymous": "%5",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
                ),
                ("ADD", {}),
                (
                    "FUNC_CALL",
                    {
                        "function": "#2",
                        "parameters": [
                            {"variable": True, "name": "blabla", "pseudonymous": "%6", "type": "float", "type_pseudonymous": "3", },
                            {"variable": False, "type": "int", "value": 123},
                        ],
                    },
                ),
                ("SEMI", {}),
                (
                    "FUNC_CALL",
                    {
                        "function": "#1",
                        "parameters": [
                            {"variable": False, "type": "int", "value": 1},
                            {"variable": False, "type": "int", "value": 2},
                        ],
                    },
                ),
                ("SEMI", {}),
                ("RET_SYM", {}),
                (
                    "VAR",
                    {
                        "name": "blabla",
                        "pseudonymous": "%6",
                        "type": "float",
                        "type_pseudonymous": "3",
                    },
                ),
                ("ADD", {}),
                (
                    "VAR",
                    {
                        "name": "bla",
                        "pseudonymous": "%5",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
                ),
                ("SEMI", {}),
                ("RCBRA", {}),
            ],
        },
        "function_that_returns_struct": {
            "pseudonymous": "#2",
            "type": "my_struct",
            "arguments": {
                "xyz": {"type": "int", "pseudonymous": "%3"},
                "aaa": {"type": "int", "pseudonymous": "%4"},
            },
            "statements": [
                ("LCBRA", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "internal_guy",
                        "pseudonymous": "%5",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
                ),
                ("SEMI", {}),
                ("RET_SYM", {}),
                ("VAR", {"type": "int", "pseudonymous": "%3"}),
                ("ADD", {}),
                ("VAR", {"type": "int", "pseudonymous": "%4"}),
                ("SEMI", {}),
                ("RCBRA", {}),
            ],
        },
        "main": {
            "pseudonymous": "#3",
            "type": "int",
            "arguments": {},
            "statements": [
                ("LCBRA", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "x",
                        "pseudonymous": "%3",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "name": "x",
                        "pseudonymous": "%3",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
                ),
                ("ASSIGN", {}),
                ("FUNC_CALL", {"function": "#1", "parameters": []}),
                ("SEMI", {}),
                (
                    "VAR_DEF",
                    {
                        "name": "array",
                        "pseudonymous": "%4",
                        "type": "int",
                        "type_pseudonymous": "2",
                        "length": 10,
                    },
                ),
                ("SEMI", {}),
                (
                    "VAR",
                    {
                        "name": "array",
                        "pseudonymous": "%4",
                        "type": "int",
                        "type_pseudonymous": "2",
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
                    {
                        "name": "y",
                        "pseudonymous": "%5",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
                ),
                ("SEMI", {}),
                ("IF_SYM", {}),
                ("LPAR", {}),
                ("LPAR", {}),
                ("LPAR", {}),
                ("LPAR", {}),
                (
                    "VAR",
                    {
                        "name": "x",
                        "pseudonymous": "%3",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
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
                    {
                        "name": "x",
                        "pseudonymous": "%3",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
                ),
                ("GREATER", {}),
                ("CST", {"type": "int", "value": 1}),
                ("RPAR", {}),
                ("RPAR", {}),
                ("AND", {}),
                ("LPAR", {}),
                (
                    "VAR",
                    {
                        "name": "x",
                        "pseudonymous": "%3",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
                ),
                ("LESS", {}),
                ("CST", {"type": "int", "value": 10}),
                ("RPAR", {}),
                ("RPAR", {}),
                ("LCBRA", {}),
                (
                    "VAR",
                    {
                        "name": "y",
                        "pseudonymous": "%5",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
                ),
                ("ASSIGN", {}),
                (
                    "VAR",
                    {
                        "name": "x",
                        "pseudonymous": "%3",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
                ),
                ("BITAND", {}),
                ("CST", {"type": "int", "value": 1}),
                ("SEMI", {}),
                ("RCBRA", {}),
                ("ELSE_SYM", {}),
                ("LCBRA", {}),
                (
                    "VAR",
                    {
                        "name": "y",
                        "pseudonymous": "%5",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
                ),
                ("ASSIGN", {}),
                (
                    "VAR",
                    {
                        "name": "x",
                        "pseudonymous": "%3",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
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
                    {
                        "name": "x",
                        "pseudonymous": "%3",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
                ),
                ("MULT", {}),
                (
                    "VAR",
                    {
                        "name": "y",
                        "pseudonymous": "%5",
                        "type": "int",
                        "type_pseudonymous": "2",
                    },
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


EXPECTED_PRINT_TREE = """
ID: 0, Value: None, Kind: PROG
  ID: 1, Value: 1, Kind: STRUCT_DEF
   Attributes: int, float
  ID: 2, Value: 2, Kind: STRUCT_DEF
   Attributes: int, int
  ID: 3, Value: 1, Kind: VAR_DEF
    Name: a, Type: int
  ID: 4, Value: 2, Kind: VAR_DEF
    Name: global_var, Type: my_struct
  ID: abc, Value: None, Kind: FUNC_DEF
    ID: 51, Value: None, Kind: SEQ
      ID: 8, Value: 5, Kind: VAR_DEF
        Name: bla, Type: int
      ID: 12, Value: None, Kind: EXPR
        ID: 14, Value: None, Kind: ASSIGN
          ID: 13, Value: 5, Kind: VAR, Type: int
          ID: 15, Value: 1, Kind: CST, Type: int
      ID: 17, Value: 6, Kind: VAR_DEF
        Name: blabla, Type: float
      ID: 21, Value: None, Kind: EXPR
        ID: 23, Value: None, Kind: ASSIGN
          ID: 22, Value: 6, Kind: VAR, Type: float
          ID: 24, Value: 2.0, Kind: CST, Type: float
      ID: 26, Value: 7, Kind: VAR_DEF
        Name: xaxaxa, Type: short
      ID: 30, Value: 8, Kind: VAR_DEF
        Name: internal_struct_var, Type: my_struct
      ID: 34, Value: None, Kind: EXPR
        ID: 38, Value: None, Kind: ASSIGN
          ID: 36, Value: None, Kind: ELEMENT_ACCESS
            ID: 35, Value: 8, Kind: VAR, Type: my_struct
            ID: 37, Value: 0, Kind: CST, Type: int
          ID: 39, Value: 1, Kind: CST, Type: int
      ID: 41, Value: None, Kind: EXPR
        ID: 43, Value: None, Kind: ASSIGN
          ID: 42, Value: 5, Kind: VAR, Type: int
          ID: 45, Value: None, Kind: ADD
            ID: 44, Value: 5, Kind: VAR, Type: int
            ID: 46, Value: 2, Kind: FUNC_CALL
              ID: 47, Value: 6, Kind: VAR, Type: float
              ID: 48, Value: 123, Kind: CST, Type: int
      ID: 48, Value: 1, Kind: FUNC_CALL
        ID: 49, Value: 1, Kind: CST, Type: int
        ID: 50, Value: 2, Kind: CST, Type: int
      ID: 52, Value: None, Kind: RET_SYM
        ID: 53, Value: None, Kind: EXPR
          ID: 55, Value: None, Kind: ADD
            ID: 54, Value: 6, Kind: VAR, Type: float
            ID: 56, Value: 5, Kind: VAR, Type: int
  ID: function_that_returns_struct, Value: None, Kind: FUNC_DEF
    ID: 63, Value: None, Kind: SEQ
      ID: 60, Value: 5, Kind: VAR_DEF
        Name: internal_guy, Type: int
      ID: 64, Value: None, Kind: RET_SYM
        ID: 65, Value: None, Kind: EXPR
          ID: 67, Value: None, Kind: ADD
            ID: 66, Value: 3, Kind: VAR, Type: int
            ID: 68, Value: 4, Kind: VAR, Type: int
  ID: main, Value: None, Kind: FUNC_DEF
    ID: 126, Value: None, Kind: SEQ
      ID: 72, Value: 3, Kind: VAR_DEF
        Name: x, Type: int
      ID: 76, Value: None, Kind: EXPR
        ID: 78, Value: None, Kind: ASSIGN
          ID: 77, Value: 3, Kind: VAR, Type: int
          ID: 79, Value: 1, Kind: FUNC_CALL
      ID: 81, Value: 4, Kind: VAR_DEF
        Name: array, Type: int (array), Length: 10
      ID: 85, Value: None, Kind: EXPR
        ID: 89, Value: None, Kind: ASSIGN
          ID: 87, Value: None, Kind: ELEMENT_ACCESS
            ID: 86, Value: 4, Kind: VAR, Type: int (array), Length: 10
            ID: 88, Value: 5, Kind: CST, Type: int
          ID: 90, Value: 1, Kind: CST, Type: int
      ID: 92, Value: 5, Kind: VAR_DEF
        Name: y, Type: int
      ID: 96, Value: None, Kind: IFELSE
        ID: 106, Value: None, Kind: AND
          ID: 102, Value: None, Kind: OR
            ID: 100, Value: None, Kind: EQUAL
              ID: 98, Value: None, Kind: LSHIFT
                ID: 97, Value: 3, Kind: VAR, Type: int
                ID: 99, Value: 4, Kind: CST, Type: int
              ID: 101, Value: 1, Kind: CST, Type: int
            ID: 104, Value: None, Kind: GREATER
              ID: 103, Value: 3, Kind: VAR, Type: int
              ID: 105, Value: 1, Kind: CST, Type: int
          ID: 108, Value: None, Kind: LESS
            ID: 107, Value: 3, Kind: VAR, Type: int
            ID: 109, Value: 10, Kind: CST, Type: int
        ID: 111, Value: None, Kind: SEQ
          ID: 112, Value: None, Kind: EXPR
            ID: 114, Value: None, Kind: ASSIGN
              ID: 113, Value: 5, Kind: VAR, Type: int
              ID: 116, Value: None, Kind: BITAND
                ID: 115, Value: 3, Kind: VAR, Type: int
                ID: 117, Value: 1, Kind: CST, Type: int
        ID: 119, Value: None, Kind: SEQ
          ID: 120, Value: None, Kind: EXPR
            ID: 122, Value: None, Kind: ASSIGN
              ID: 121, Value: 5, Kind: VAR, Type: int
              ID: 124, Value: None, Kind: BITOR
                ID: 123, Value: 3, Kind: VAR, Type: int
                ID: 125, Value: 1, Kind: CST, Type: int
      ID: 127, Value: None, Kind: RET_SYM
        ID: 128, Value: None, Kind: EXPR
          ID: 134, Value: None, Kind: RSHIFT
            ID: 132, Value: None, Kind: DIV
              ID: 130, Value: None, Kind: MULT
                ID: 129, Value: 3, Kind: VAR, Type: int
                ID: 131, Value: 5, Kind: VAR, Type: int
              ID: 133, Value: 2, Kind: CST, Type: int
            ID: 135, Value: 1, Kind: CST, Type: int
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
