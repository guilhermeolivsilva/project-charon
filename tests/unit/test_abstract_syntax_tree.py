"""Implement unit tests for the `src.abstract_syntax_tree.AbstractSyntaxTree` class."""

from copy import deepcopy

from pytest import fixture

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.ast_nodes.basic.PROG import PROG
from tests.unit.common import TOKENIZED_SOURCE_CODE


# Defined here just because of identation
EXPECTED_PRINT_TREE = """
Kind: PROG
  Value: 1, Kind: STRUCT_DEF, Type: my_struct
   Attributes: int, float
  Value: 2, Kind: STRUCT_DEF, Type: test_struct
   Attributes: int, int
  Value: 1, Kind: VAR_DEF, Type: int
    Name: a, Type: int (array), Length: 10
  Value: 2, Kind: VAR_DEF, Type: my_struct
    Name: global_var, Type: my_struct
  Value: function_that_returns_struct, Kind: FUNC_DEF, Type: my_struct
    Value: 3, Kind: PARAM, Type: int
      Name: xyz, Type: int
    Value: 4, Kind: PARAM, Type: int
      Name: aaa, Type: int
    Kind: SEQ
      Value: 5, Kind: VAR_DEF, Type: int
        Name: internal_guy, Type: int
      Kind: ASSIGN, Type: int
        Value: 5, Kind: VAR, Type: int
        Kind: ADD, Type: int
          Value: 3, Kind: VAR, Type: int
          Value: 4, Kind: VAR, Type: int
      Kind: ASSIGN, Type: int
        Kind: ELEMENT_ACCESS, Type: int
          Value: 2, Kind: VAR, Type: my_struct
          Value: 0, Kind: CST, Type: int
        Value: 5, Kind: VAR, Type: int
      Kind: RET_SYM, Type: my_struct
        Value: 2, Kind: VAR, Type: my_struct
  Value: some_simple_function, Kind: FUNC_DEF, Type: int
    Value: 6, Kind: PARAM, Type: float
      Name: param_1, Type: float
    Value: 7, Kind: PARAM, Type: int
      Name: param_2, Type: int
    Kind: SEQ
      Kind: RET_SYM, Type: int
        Kind: DIV, Type: float
          Value: 6, Kind: VAR, Type: float
          Value: 7, Kind: VAR, Type: int
  Value: abc, Kind: FUNC_DEF, Type: int
    Value: 8, Kind: PARAM, Type: int
      Name: asda, Type: int
    Value: 9, Kind: PARAM, Type: int
      Name: abcdef, Type: int
    Kind: SEQ
      Value: 10, Kind: VAR_DEF, Type: int
        Name: bla, Type: int
      Kind: ASSIGN, Type: int
        Value: 10, Kind: VAR, Type: int
        Value: 1, Kind: CST, Type: int
      Value: 11, Kind: VAR_DEF, Type: float
        Name: blabla, Type: float
      Kind: ASSIGN, Type: float
        Value: 11, Kind: VAR, Type: float
        Value: 2.0, Kind: CST, Type: float
      Value: 12, Kind: VAR_DEF, Type: short
        Name: xaxaxa, Type: short
      Value: 13, Kind: VAR_DEF, Type: my_struct
        Name: internal_struct_var, Type: my_struct
      Kind: ASSIGN, Type: int
        Kind: ELEMENT_ACCESS, Type: int
          Value: 13, Kind: VAR, Type: my_struct
          Value: 0, Kind: CST, Type: int
        Value: 1, Kind: CST, Type: int
      Kind: ASSIGN, Type: int
        Value: 10, Kind: VAR, Type: int
        Kind: ADD, Type: int
          Value: 10, Kind: VAR, Type: int
          Value: 2, Kind: FUNC_CALL, Type: int
            Kind: ARG
              Value: 11, Kind: VAR, Type: float
            Kind: ARG
              Value: 123, Kind: CST, Type: int
      Kind: RET_SYM, Type: int
        Kind: ADD, Type: float
          Value: 11, Kind: VAR, Type: float
          Value: 10, Kind: VAR, Type: int
  Value: main, Kind: FUNC_DEF, Type: int
    Kind: SEQ
      Value: 14, Kind: VAR_DEF, Type: int
        Name: x, Type: int
      Kind: ASSIGN, Type: int
        Value: 14, Kind: VAR, Type: int
        Value: 3, Kind: FUNC_CALL, Type: int
          Kind: ARG
            Value: 1, Kind: CST, Type: int
          Kind: ARG
            Value: 2, Kind: CST, Type: int
      Value: 15, Kind: VAR_DEF, Type: int
        Name: array, Type: int (array), Length: 10
      Kind: ASSIGN, Type: int
        Kind: ELEMENT_ACCESS, Type: int
          Value: 15, Kind: VAR, Type: int (array), Length: 10
          Value: 5, Kind: CST, Type: int
        Value: 1, Kind: CST, Type: int
      Value: 16, Kind: VAR_DEF, Type: int
        Name: y, Type: int
      Kind: IFELSE
        Kind: AND, Type: int
          Kind: OR, Type: int
            Kind: EQUAL, Type: int
              Kind: LSHIFT, Type: int
                Value: 14, Kind: VAR, Type: int
                Value: 4, Kind: CST, Type: int
              Value: 1, Kind: CST, Type: int
            Kind: GREATER, Type: int
              Value: 14, Kind: VAR, Type: int
              Value: 1, Kind: CST, Type: int
          Kind: LESS, Type: int
            Value: 14, Kind: VAR, Type: int
            Value: 10, Kind: CST, Type: int
        Kind: SEQ
          Kind: ASSIGN, Type: int
            Value: 16, Kind: VAR, Type: int
            Kind: BITAND, Type: int
              Value: 14, Kind: VAR, Type: int
              Value: 1, Kind: CST, Type: int
        Kind: SEQ
          Kind: ASSIGN, Type: int
            Value: 16, Kind: VAR, Type: int
            Kind: BITOR, Type: int
              Value: 14, Kind: VAR, Type: int
              Value: 1, Kind: CST, Type: int
      Kind: RET_SYM, Type: int
        Kind: RSHIFT, Type: int
          Kind: DIV, Type: int
            Kind: MULT, Type: int
              Value: 14, Kind: VAR, Type: int
              Value: 16, Kind: VAR, Type: int
            Value: 2, Kind: CST, Type: int
          Value: 1, Kind: CST, Type: int
"""

def test_init() -> None:
    """Test the instantiation of AbstractSyntaxTree objects."""

    _source = deepcopy(TOKENIZED_SOURCE_CODE)
    ast = AbstractSyntaxTree(source_code=_source)

    assert ast.source_code == TOKENIZED_SOURCE_CODE
    assert ast.current_symbol is None
    assert ast.current_value == {}
    assert ast.root == PROG()


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
