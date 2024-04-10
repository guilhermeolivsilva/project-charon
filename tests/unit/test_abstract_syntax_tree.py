"""Implement unit tests for the `src.abstract_syntax_tree.AbstractSyntaxTree` class."""

from pytest import fixture

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.node import Node


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


EXPECTED_DFS = """
ID: 0, Value: None, Kind: PROG
ID: 14, Value: None, Kind: SEQ, Parent ID: 0
ID: 1, Value: None, Kind: EMPTY, Parent ID: 2
ID: 3, Value: None, Kind: EXPR, Parent ID: 2
ID: 5, Value: None, Kind: SET, Parent ID: 3
ID: 4, Value: a, Kind: VAR, Parent ID: 5
ID: 6, Value: 5, Kind: CST, Parent ID: 5
ID: 8, Value: None, Kind: EXPR, Parent ID: 7
ID: 10, Value: None, Kind: SET, Parent ID: 8
ID: 9, Value: b, Kind: VAR, Parent ID: 10
ID: 12, Value: None, Kind: SUB, Parent ID: 10
ID: 11, Value: a, Kind: VAR, Parent ID: 12
ID: 13, Value: 1, Kind: CST, Parent ID: 12
ID: 15, Value: None, Kind: DO, Parent ID: 14
ID: 31, Value: None, Kind: SEQ, Parent ID: 15
ID: 16, Value: None, Kind: EMPTY, Parent ID: 17
ID: 18, Value: None, Kind: EXPR, Parent ID: 17
ID: 20, Value: None, Kind: SET, Parent ID: 18
ID: 19, Value: c, Kind: VAR, Parent ID: 20
ID: 22, Value: None, Kind: SUB, Parent ID: 20
ID: 21, Value: a, Kind: VAR, Parent ID: 22
ID: 23, Value: b, Kind: VAR, Parent ID: 22
ID: 25, Value: None, Kind: EXPR, Parent ID: 24
ID: 27, Value: None, Kind: SET, Parent ID: 25
ID: 26, Value: b, Kind: VAR, Parent ID: 27
ID: 29, Value: None, Kind: ADD, Parent ID: 27
ID: 28, Value: b, Kind: VAR, Parent ID: 29
ID: 30, Value: 1, Kind: CST, Parent ID: 29
ID: 32, Value: None, Kind: IFELSE, Parent ID: 31
ID: 34, Value: None, Kind: LT, Parent ID: 32
ID: 33, Value: a, Kind: VAR, Parent ID: 34
ID: 35, Value: c, Kind: VAR, Parent ID: 34
ID: 37, Value: None, Kind: SEQ, Parent ID: 32
ID: 36, Value: None, Kind: EMPTY, Parent ID: 37
ID: 38, Value: None, Kind: EXPR, Parent ID: 37
ID: 40, Value: None, Kind: SET, Parent ID: 38
ID: 39, Value: d, Kind: VAR, Parent ID: 40
ID: 41, Value: 10, Kind: CST, Parent ID: 40
ID: 43, Value: None, Kind: SEQ, Parent ID: 32
ID: 42, Value: None, Kind: EMPTY, Parent ID: 43
ID: 44, Value: None, Kind: EXPR, Parent ID: 43
ID: 46, Value: None, Kind: SET, Parent ID: 44
ID: 45, Value: d, Kind: VAR, Parent ID: 46
ID: 47, Value: 0, Kind: CST, Parent ID: 46
ID: 49, Value: None, Kind: LT, Parent ID: 15
ID: 48, Value: b, Kind: VAR, Parent ID: 49
ID: 50, Value: a, Kind: VAR, Parent ID: 49
"""


def _dfs(node: Node) -> None:
    """
    Print an AbstractSyntaxTree in DFS fashion.

    Parameters
    ----------
    node : Node
        The current `Node` being visited.
    """

    print(node)

    for child in node.children:
        _dfs(child)

    return


def test_init() -> None:
    """Test the instantiation of AbstractSyntaxTree objects."""

    ast = AbstractSyntaxTree(source_code=SOURCE_CODE)

    assert ast.node_id_manager == 1
    assert ast.source_code == SOURCE_CODE
    assert ast.current_symbol is None
    assert ast.current_value is None
    assert ast.root == Node(id=0, kind="PROG")


def test_build(capfd: fixture) -> None:
    """
    Test if the `build` method works as expected.

    To run this test, we compare the output of an auxiliary `_dfs` function
    ran on the AST to a known, expected result. This is achieved by capturing
    the console output with pytest's `capfd` fixture.
    """

    ast = AbstractSyntaxTree(source_code=SOURCE_CODE)
    ast.build()

    _dfs(ast.root)

    out, _ = capfd.readouterr()

    # Add a new line before the contents just to match the formatting in
    # `EXPECTED_DFS`.
    out = "\n" + out

    assert out == EXPECTED_DFS
