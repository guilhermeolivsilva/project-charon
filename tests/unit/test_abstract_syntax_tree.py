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
ID: 0, Kind: PROG, Value: None
ID: 14, Kind: SEQ, Value: None, Parent ID: 0
ID: 7, Kind: SEQ, Value: None, Parent ID: 14
ID: 2, Kind: SEQ, Value: None, Parent ID: 7
ID: 1, Kind: EMPTY, Value: None, Parent ID: 2
ID: 3, Kind: EXPR, Value: None, Parent ID: 2
ID: 5, Kind: SET, Value: None, Parent ID: 3
ID: 4, Kind: VAR, Value: a, Parent ID: 5
ID: 6, Kind: CST, Value: 5, Parent ID: 5
ID: 8, Kind: EXPR, Value: None, Parent ID: 7
ID: 10, Kind: SET, Value: None, Parent ID: 8
ID: 9, Kind: VAR, Value: b, Parent ID: 10
ID: 12, Kind: SUB, Value: None, Parent ID: 10
ID: 11, Kind: VAR, Value: a, Parent ID: 12
ID: 13, Kind: CST, Value: 1, Parent ID: 12
ID: 15, Kind: DO, Value: None, Parent ID: 14
ID: 31, Kind: SEQ, Value: None, Parent ID: 15
ID: 24, Kind: SEQ, Value: None, Parent ID: 31
ID: 17, Kind: SEQ, Value: None, Parent ID: 24
ID: 16, Kind: EMPTY, Value: None, Parent ID: 17
ID: 18, Kind: EXPR, Value: None, Parent ID: 17
ID: 20, Kind: SET, Value: None, Parent ID: 18
ID: 19, Kind: VAR, Value: c, Parent ID: 20
ID: 22, Kind: SUB, Value: None, Parent ID: 20
ID: 21, Kind: VAR, Value: a, Parent ID: 22
ID: 23, Kind: VAR, Value: b, Parent ID: 22
ID: 25, Kind: EXPR, Value: None, Parent ID: 24
ID: 27, Kind: SET, Value: None, Parent ID: 25
ID: 26, Kind: VAR, Value: b, Parent ID: 27
ID: 29, Kind: ADD, Value: None, Parent ID: 27
ID: 28, Kind: VAR, Value: b, Parent ID: 29
ID: 30, Kind: CST, Value: 1, Parent ID: 29
ID: 32, Kind: IFELSE, Value: None, Parent ID: 31
ID: 34, Kind: LT, Value: None, Parent ID: 32
ID: 33, Kind: VAR, Value: a, Parent ID: 34
ID: 35, Kind: VAR, Value: c, Parent ID: 34
ID: 37, Kind: SEQ, Value: None, Parent ID: 32
ID: 36, Kind: EMPTY, Value: None, Parent ID: 37
ID: 38, Kind: EXPR, Value: None, Parent ID: 37
ID: 40, Kind: SET, Value: None, Parent ID: 38
ID: 39, Kind: VAR, Value: d, Parent ID: 40
ID: 41, Kind: CST, Value: 10, Parent ID: 40
ID: 43, Kind: SEQ, Value: None, Parent ID: 32
ID: 42, Kind: EMPTY, Value: None, Parent ID: 43
ID: 44, Kind: EXPR, Value: None, Parent ID: 43
ID: 46, Kind: SET, Value: None, Parent ID: 44
ID: 45, Kind: VAR, Value: d, Parent ID: 46
ID: 47, Kind: CST, Value: 0, Parent ID: 46
ID: 49, Kind: LT, Value: None, Parent ID: 15
ID: 48, Kind: VAR, Value: b, Parent ID: 49
ID: 50, Kind: VAR, Value: a, Parent ID: 49
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
