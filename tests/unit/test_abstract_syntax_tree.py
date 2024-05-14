"""Implement unit tests for the `src.abstract_syntax_tree.AbstractSyntaxTree` class."""

from pytest import fixture

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.nodes.PROG import PROG


SOURCE_CODE = [
    ("LBRA", None),
    ("ID", "a"),
    ("EQUAL", None),
    ("INT", 5),
    ("SEMI", None),
    ("ID", "b"),
    ("EQUAL", None),
    ("ID", "a"),
    ("MINUS", None),
    ("INT", 1),
    ("SEMI", None),
    ("DO_SYM", None),
    ("LBRA", None),
    ("ID", "c"),
    ("EQUAL", None),
    ("ID", "a"),
    ("MINUS", None),
    ("ID", "b"),
    ("SEMI", None),
    ("ID", "b"),
    ("EQUAL", None),
    ("ID", "b"),
    ("PLUS", None),
    ("INT", 1),
    ("SEMI", None),
    ("IF_SYM", None),
    ("LPAR", None),
    ("ID", "a"),
    ("LESS", None),
    ("ID", "c"),
    ("RPAR", None),
    ("LBRA", None),
    ("ID", "d"),
    ("EQUAL", None),
    ("INT", 10),
    ("SEMI", None),
    ("RBRA", None),
    ("ELSE_SYM", None),
    ("LBRA", None),
    ("ID", "d"),
    ("EQUAL", None),
    ("INT", 0),
    ("SEMI", None),
    ("RBRA", None),
    ("RBRA", None),
    ("WHILE_SYM", None),
    ("LPAR", None),
    ("ID", "b"),
    ("LESS", None),
    ("ID", "a"),
    ("RPAR", None),
    ("SEMI", None),
    ("RBRA", None),
]


EXPECTED_PRINT_TREE = """
ID: 0, Value: None, Kind: PROG
  ID: 14, Value: None, Kind: SEQ
    ID: 3, Value: None, Kind: EXPR
      ID: 5, Value: a, Kind: SET
        ID: 6, Value: 5, Kind: CST
    ID: 8, Value: None, Kind: EXPR
      ID: 10, Value: b, Kind: SET
        ID: 12, Value: None, Kind: SUB
          ID: 11, Value: a, Kind: VAR
          ID: 13, Value: 1, Kind: CST
    ID: 15, Value: None, Kind: DO
      ID: 49, Value: None, Kind: LT
        ID: 48, Value: b, Kind: VAR
        ID: 50, Value: a, Kind: VAR
      ID: 31, Value: None, Kind: SEQ
        ID: 18, Value: None, Kind: EXPR
          ID: 20, Value: c, Kind: SET
            ID: 22, Value: None, Kind: SUB
              ID: 21, Value: a, Kind: VAR
              ID: 23, Value: b, Kind: VAR
        ID: 25, Value: None, Kind: EXPR
          ID: 27, Value: b, Kind: SET
            ID: 29, Value: None, Kind: ADD
              ID: 28, Value: b, Kind: VAR
              ID: 30, Value: 1, Kind: CST
        ID: 32, Value: None, Kind: IFELSE
          ID: 34, Value: None, Kind: LT
            ID: 33, Value: a, Kind: VAR
            ID: 35, Value: c, Kind: VAR
          ID: 37, Value: None, Kind: SEQ
            ID: 38, Value: None, Kind: EXPR
              ID: 40, Value: d, Kind: SET
                ID: 41, Value: 10, Kind: CST
          ID: 43, Value: None, Kind: SEQ
            ID: 44, Value: None, Kind: EXPR
              ID: 46, Value: d, Kind: SET
                ID: 47, Value: 0, Kind: CST
"""


def test_init() -> None:
    """Test the instantiation of AbstractSyntaxTree objects."""

    ast = AbstractSyntaxTree(source_code=SOURCE_CODE)

    assert ast.node_id_manager == 1
    assert ast.source_code == SOURCE_CODE
    assert ast.current_symbol is None
    assert ast.current_value is None
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
