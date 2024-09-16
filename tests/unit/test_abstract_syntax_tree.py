"""Implement unit tests for the `src.abstract_syntax_tree.AbstractSyntaxTree` class."""

from pytest import fixture

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.ast_nodes.basic.PROG import PROG
from tests.unit.common import TOKENIZED_SOURCE_CODE


# Defined here just because of identation
EXPECTED_PRINT_TREE = """
ID: 0, Kind: PROG
  ID: 1, Value: 1, Kind: STRUCT_DEF, Type: my_struct
   Attributes: int, float
  ID: 2, Value: 2, Kind: STRUCT_DEF, Type: test_struct
   Attributes: int, int
  ID: 3, Value: 1, Kind: VAR_DEF, Type: int
    Name: a, Type: int (array), Length: 10
  ID: 4, Value: 2, Kind: VAR_DEF, Type: my_struct
    Name: global_var, Type: my_struct
  ID: 5, Value: function_that_returns_struct, Kind: FUNC_DEF, Type: my_struct
    Value: 3, Kind: VAR_DEF, Type: int
      Name: xyz, Type: int
    Value: 4, Kind: VAR_DEF, Type: int
      Name: aaa, Type: int
    Kind: SEQ
      ID: 8, Value: 5, Kind: VAR_DEF, Type: int
        Name: internal_guy, Type: int
      ID: 12, Kind: RET_SYM
        ID: 13, Kind: EXPR
          ID: 15, Kind: ADD, Type: int
            ID: 14, Value: 3, Kind: VAR, Type: int
            ID: 16, Value: 4, Kind: VAR, Type: int
  ID: 17, Value: some_simple_function, Kind: FUNC_DEF, Type: int
    Value: 3, Kind: VAR_DEF, Type: float
      Name: param_1, Type: float
    Value: 4, Kind: VAR_DEF, Type: int
      Name: param_2, Type: int
    Kind: SEQ
      ID: 20, Kind: RET_SYM
        ID: 21, Kind: EXPR
          ID: 23, Kind: DIV, Type: float
            ID: 22, Value: 3, Kind: VAR, Type: float
            ID: 24, Value: 4, Kind: VAR, Type: int
  ID: 25, Value: abc, Kind: FUNC_DEF, Type: int
    Value: 3, Kind: VAR_DEF, Type: int
      Name: asda, Type: int
    Value: 4, Kind: VAR_DEF, Type: int
      Name: abcdef, Type: int
    Kind: SEQ
      ID: 28, Value: 5, Kind: VAR_DEF, Type: int
        Name: bla, Type: int
      ID: 32, Kind: EXPR
        ID: 34, Kind: ASSIGN, Type: int
          ID: 33, Value: 5, Kind: VAR, Type: int
          ID: 35, Value: 1, Kind: CST, Type: int
      ID: 37, Value: 6, Kind: VAR_DEF, Type: float
        Name: blabla, Type: float
      ID: 41, Kind: EXPR
        ID: 43, Kind: ASSIGN, Type: float
          ID: 42, Value: 6, Kind: VAR, Type: float
          ID: 44, Value: 2.0, Kind: CST, Type: float
      ID: 46, Value: 7, Kind: VAR_DEF, Type: short
        Name: xaxaxa, Type: short
      ID: 50, Value: 8, Kind: VAR_DEF, Type: my_struct
        Name: internal_struct_var, Type: my_struct
      ID: 54, Kind: EXPR
        ID: 58, Kind: ASSIGN, Type: int
          ID: 56, Kind: ELEMENT_ACCESS, Type: int
            ID: 55, Value: 8, Kind: VAR, Type: my_struct
            ID: 57, Value: 0, Kind: CST, Type: int
          ID: 59, Value: 1, Kind: CST, Type: int
      ID: 61, Kind: EXPR
        ID: 63, Kind: ASSIGN, Type: int
          ID: 62, Value: 5, Kind: VAR, Type: int
          ID: 65, Kind: ADD, Type: int
            ID: 64, Value: 5, Kind: VAR, Type: int
            ID: 66, Value: 2, Kind: FUNC_CALL, Type: int
              ID: 67, Value: 6, Kind: VAR, Type: float
              ID: 68, Value: 123, Kind: CST, Type: int
      ID: 68, Value: 3, Kind: FUNC_CALL, Type: int
        ID: 69, Value: 1, Kind: CST, Type: int
        ID: 70, Value: 2, Kind: CST, Type: int
      ID: 72, Kind: RET_SYM
        ID: 73, Kind: EXPR
          ID: 75, Kind: ADD, Type: float
            ID: 74, Value: 6, Kind: VAR, Type: float
            ID: 76, Value: 5, Kind: VAR, Type: int
  ID: 77, Value: main, Kind: FUNC_DEF, Type: int
    Kind: SEQ
      ID: 80, Value: 3, Kind: VAR_DEF, Type: int
        Name: x, Type: int
      ID: 84, Kind: EXPR
        ID: 86, Kind: ASSIGN, Type: int
          ID: 85, Value: 3, Kind: VAR, Type: int
          ID: 87, Value: 3, Kind: FUNC_CALL, Type: int
      ID: 89, Value: 4, Kind: VAR_DEF, Type: int
        Name: array, Type: int (array), Length: 10
      ID: 93, Kind: EXPR
        ID: 97, Kind: ASSIGN, Type: int
          ID: 95, Kind: ELEMENT_ACCESS, Type: int
            ID: 94, Value: 4, Kind: VAR, Type: int (array), Length: 10
            ID: 96, Value: 5, Kind: CST, Type: int
          ID: 98, Value: 1, Kind: CST, Type: int
      ID: 100, Value: 5, Kind: VAR_DEF, Type: int
        Name: y, Type: int
      ID: 104, Kind: IFELSE
        ID: 114, Kind: AND, Type: int
          ID: 110, Kind: OR, Type: int
            ID: 108, Kind: EQUAL, Type: int
              ID: 106, Kind: LSHIFT, Type: int
                ID: 105, Value: 3, Kind: VAR, Type: int
                ID: 107, Value: 4, Kind: CST, Type: int
              ID: 109, Value: 1, Kind: CST, Type: int
            ID: 112, Kind: GREATER, Type: int
              ID: 111, Value: 3, Kind: VAR, Type: int
              ID: 113, Value: 1, Kind: CST, Type: int
          ID: 116, Kind: LESS, Type: int
            ID: 115, Value: 3, Kind: VAR, Type: int
            ID: 117, Value: 10, Kind: CST, Type: int
        Kind: SEQ
          ID: 120, Kind: EXPR
            ID: 122, Kind: ASSIGN, Type: int
              ID: 121, Value: 5, Kind: VAR, Type: int
              ID: 124, Kind: BITAND, Type: int
                ID: 123, Value: 3, Kind: VAR, Type: int
                ID: 125, Value: 1, Kind: CST, Type: int
        Kind: SEQ
          ID: 128, Kind: EXPR
            ID: 130, Kind: ASSIGN, Type: int
              ID: 129, Value: 5, Kind: VAR, Type: int
              ID: 132, Kind: BITOR, Type: int
                ID: 131, Value: 3, Kind: VAR, Type: int
                ID: 133, Value: 1, Kind: CST, Type: int
      ID: 135, Kind: RET_SYM
        ID: 136, Kind: EXPR
          ID: 142, Kind: RSHIFT, Type: int
            ID: 140, Kind: DIV, Type: int
              ID: 138, Kind: MULT, Type: int
                ID: 137, Value: 3, Kind: VAR, Type: int
                ID: 139, Value: 5, Kind: VAR, Type: int
              ID: 141, Value: 2, Kind: CST, Type: int
            ID: 143, Value: 1, Kind: CST, Type: int
"""

def test_init() -> None:
    """Test the instantiation of AbstractSyntaxTree objects."""

    ast = AbstractSyntaxTree(source_code=TOKENIZED_SOURCE_CODE)

    assert ast.node_id_manager == 1
    assert ast.source_code == TOKENIZED_SOURCE_CODE
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

    ast = AbstractSyntaxTree(source_code=TOKENIZED_SOURCE_CODE)
    _ = ast.build()

    ast.print_tree()

    out, _ = capfd.readouterr()
    out = "\n" + out

    expected_tree = EXPECTED_PRINT_TREE
    assert out == expected_tree
