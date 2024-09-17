"""Implement unit tests for the `src.abstract_syntax_tree.AbstractSyntaxTree` class."""

from copy import deepcopy

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
      ID: 13, Kind: ASSIGN, Type: int
        ID: 12, Value: 5, Kind: VAR, Type: int
        ID: 15, Kind: ADD, Type: int
          ID: 14, Value: 3, Kind: VAR, Type: int
          ID: 16, Value: 4, Kind: VAR, Type: int
      ID: 21, Kind: ASSIGN, Type: int
        ID: 19, Kind: ELEMENT_ACCESS, Type: int
          ID: 18, Value: 2, Kind: VAR, Type: my_struct
          ID: 20, Value: 0, Kind: CST, Type: int
        ID: 22, Value: 5, Kind: VAR, Type: int
      ID: 24, Kind: RET_SYM, Type: my_struct
        ID: 25, Value: 2, Kind: VAR, Type: my_struct
  ID: 26, Value: some_simple_function, Kind: FUNC_DEF, Type: int
    Value: 3, Kind: VAR_DEF, Type: float
      Name: param_1, Type: float
    Value: 4, Kind: VAR_DEF, Type: int
      Name: param_2, Type: int
    Kind: SEQ
      ID: 29, Kind: RET_SYM, Type: int
        ID: 31, Kind: DIV, Type: float
          ID: 30, Value: 3, Kind: VAR, Type: float
          ID: 32, Value: 4, Kind: VAR, Type: int
  ID: 33, Value: abc, Kind: FUNC_DEF, Type: int
    Value: 3, Kind: VAR_DEF, Type: int
      Name: asda, Type: int
    Value: 4, Kind: VAR_DEF, Type: int
      Name: abcdef, Type: int
    Kind: SEQ
      ID: 36, Value: 5, Kind: VAR_DEF, Type: int
        Name: bla, Type: int
      ID: 41, Kind: ASSIGN, Type: int
        ID: 40, Value: 5, Kind: VAR, Type: int
        ID: 42, Value: 1, Kind: CST, Type: int
      ID: 44, Value: 6, Kind: VAR_DEF, Type: float
        Name: blabla, Type: float
      ID: 49, Kind: ASSIGN, Type: float
        ID: 48, Value: 6, Kind: VAR, Type: float
        ID: 50, Value: 2.0, Kind: CST, Type: float
      ID: 52, Value: 7, Kind: VAR_DEF, Type: short
        Name: xaxaxa, Type: short
      ID: 56, Value: 8, Kind: VAR_DEF, Type: my_struct
        Name: internal_struct_var, Type: my_struct
      ID: 63, Kind: ASSIGN, Type: int
        ID: 61, Kind: ELEMENT_ACCESS, Type: int
          ID: 60, Value: 8, Kind: VAR, Type: my_struct
          ID: 62, Value: 0, Kind: CST, Type: int
        ID: 64, Value: 1, Kind: CST, Type: int
      ID: 67, Kind: ASSIGN, Type: int
        ID: 66, Value: 5, Kind: VAR, Type: int
        ID: 69, Kind: ADD, Type: int
          ID: 68, Value: 5, Kind: VAR, Type: int
          ID: 70, Value: 2, Kind: FUNC_CALL, Type: int
            ID: 71, Value: 6, Kind: VAR, Type: float
            ID: 72, Value: 123, Kind: CST, Type: int
      ID: 72, Value: 3, Kind: FUNC_CALL, Type: int
        ID: 73, Value: 1, Kind: CST, Type: int
        ID: 74, Value: 2, Kind: CST, Type: int
      ID: 76, Kind: RET_SYM, Type: int
        ID: 78, Kind: ADD, Type: float
          ID: 77, Value: 6, Kind: VAR, Type: float
          ID: 79, Value: 5, Kind: VAR, Type: int
  ID: 80, Value: main, Kind: FUNC_DEF, Type: int
    Kind: SEQ
      ID: 83, Value: 3, Kind: VAR_DEF, Type: int
        Name: x, Type: int
      ID: 88, Kind: ASSIGN, Type: int
        ID: 87, Value: 3, Kind: VAR, Type: int
        ID: 89, Value: 3, Kind: FUNC_CALL, Type: int
      ID: 91, Value: 4, Kind: VAR_DEF, Type: int
        Name: array, Type: int (array), Length: 10
      ID: 98, Kind: ASSIGN, Type: int
        ID: 96, Kind: ELEMENT_ACCESS, Type: int
          ID: 95, Value: 4, Kind: VAR, Type: int (array), Length: 10
          ID: 97, Value: 5, Kind: CST, Type: int
        ID: 99, Value: 1, Kind: CST, Type: int
      ID: 101, Value: 5, Kind: VAR_DEF, Type: int
        Name: y, Type: int
      ID: 105, Kind: IFELSE
        ID: 115, Kind: AND, Type: int
          ID: 111, Kind: OR, Type: int
            ID: 109, Kind: EQUAL, Type: int
              ID: 107, Kind: LSHIFT, Type: int
                ID: 106, Value: 3, Kind: VAR, Type: int
                ID: 108, Value: 4, Kind: CST, Type: int
              ID: 110, Value: 1, Kind: CST, Type: int
            ID: 113, Kind: GREATER, Type: int
              ID: 112, Value: 3, Kind: VAR, Type: int
              ID: 114, Value: 1, Kind: CST, Type: int
          ID: 117, Kind: LESS, Type: int
            ID: 116, Value: 3, Kind: VAR, Type: int
            ID: 118, Value: 10, Kind: CST, Type: int
        Kind: SEQ
          ID: 122, Kind: ASSIGN, Type: int
            ID: 121, Value: 5, Kind: VAR, Type: int
            ID: 124, Kind: BITAND, Type: int
              ID: 123, Value: 3, Kind: VAR, Type: int
              ID: 125, Value: 1, Kind: CST, Type: int
        Kind: SEQ
          ID: 129, Kind: ASSIGN, Type: int
            ID: 128, Value: 5, Kind: VAR, Type: int
            ID: 131, Kind: BITOR, Type: int
              ID: 130, Value: 3, Kind: VAR, Type: int
              ID: 132, Value: 1, Kind: CST, Type: int
      ID: 134, Kind: RET_SYM, Type: int
        ID: 140, Kind: RSHIFT, Type: int
          ID: 138, Kind: DIV, Type: int
            ID: 136, Kind: MULT, Type: int
              ID: 135, Value: 3, Kind: VAR, Type: int
              ID: 137, Value: 5, Kind: VAR, Type: int
            ID: 139, Value: 2, Kind: CST, Type: int
          ID: 141, Value: 1, Kind: CST, Type: int
"""

def test_init() -> None:
    """Test the instantiation of AbstractSyntaxTree objects."""

    _source = deepcopy(TOKENIZED_SOURCE_CODE)
    ast = AbstractSyntaxTree(source_code=_source)

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

    _source = deepcopy(TOKENIZED_SOURCE_CODE)
    ast = AbstractSyntaxTree(source_code=_source)
    _ = ast.build()

    ast.print_tree()

    out, _ = capfd.readouterr()
    out = "\n" + out

    expected_tree = EXPECTED_PRINT_TREE
    assert out == expected_tree
