"""Implement unit tests for the `src.abstract_syntax_tree.AbstractSyntaxTree` class."""

from copy import deepcopy

from pytest import fixture

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.ast_nodes.basic.PROG import PROG
from tests.unit.common import TOKENIZED_SOURCE_CODE


# Defined here just because of identation
EXPECTED_PRINT_TREE = """
Kind: PROG
  Kind: STRUCT_DEF, Value: 1, Type: my_struct
   Attributes: int, float
  Kind: STRUCT_DEF, Value: 2, Type: test_struct
   Attributes: int, int
  Kind: VAR_DEF, Value: 1, Type: int
    Name: a, Type: int (array), Length: 10
  Kind: VAR_DEF, Value: 2, Type: my_struct
    Name: global_var, Type: my_struct
  Kind: FUNC_DEF, Value: function_that_returns_struct, Type: my_struct
    Kind: PARAM, Value: 3, Type: int
      Name: xyz, Type: int
    Kind: PARAM, Value: 4, Type: int
      Name: aaa, Type: int
    Kind: SEQ
      Kind: VAR_DEF, Value: 5, Type: int
        Name: internal_guy, Type: int
      Kind: ASSIGN, Type: int
        Kind: VAR, Value: 5, Type: int
        Kind: ADD, Type: int
          Kind: VAR, Value: 3, Type: int
          Kind: VAR, Value: 4, Type: int
      Kind: ASSIGN, Type: int
        Kind: ELEMENT_ACCESS, Type: int
          Kind: VAR, Value: 2, Type: my_struct
          Kind: CST, Value: 0, Type: int
        Kind: VAR, Value: 5, Type: int
      Kind: RET_SYM, Type: my_struct
        Kind: VAR, Value: 2, Type: my_struct
  Kind: FUNC_DEF, Value: some_simple_function, Type: int
    Kind: PARAM, Value: 6, Type: float
      Name: param_1, Type: float
    Kind: PARAM, Value: 7, Type: int
      Name: param_2, Type: int
    Kind: SEQ
      Kind: RET_SYM, Type: int
        Kind: DIV, Type: float
          Kind: VAR, Value: 6, Type: float
          Kind: VAR, Value: 7, Type: int
  Kind: FUNC_DEF, Value: abc, Type: int
    Kind: PARAM, Value: 8, Type: int
      Name: asda, Type: int
    Kind: PARAM, Value: 9, Type: int
      Name: abcdef, Type: int
    Kind: SEQ
      Kind: VAR_DEF, Value: 10, Type: int
        Name: bla, Type: int
      Kind: ASSIGN, Type: int
        Kind: VAR, Value: 10, Type: int
        Kind: CST, Value: 1, Type: int
      Kind: VAR_DEF, Value: 11, Type: float
        Name: blabla, Type: float
      Kind: ASSIGN, Type: float
        Kind: VAR, Value: 11, Type: float
        Kind: CST, Value: 2.0, Type: float
      Kind: VAR_DEF, Value: 12, Type: short
        Name: xaxaxa, Type: short
      Kind: VAR_DEF, Value: 13, Type: my_struct
        Name: internal_struct_var, Type: my_struct
      Kind: ASSIGN, Type: int
        Kind: ELEMENT_ACCESS, Type: int
          Kind: VAR, Value: 13, Type: my_struct
          Kind: CST, Value: 0, Type: int
        Kind: CST, Value: 1, Type: int
      Kind: ASSIGN, Type: int
        Kind: VAR, Value: 10, Type: int
        Kind: ADD, Type: int
          Kind: VAR, Value: 10, Type: int
          Kind: FUNC_CALL, Value: 2, Type: int
            Kind: ARG
              Kind: VAR, Value: 11, Type: float
            Kind: ARG
              Kind: CST, Value: 123, Type: int
      Kind: RET_SYM, Type: int
        Kind: ADD, Type: float
          Kind: VAR, Value: 11, Type: float
          Kind: VAR, Value: 10, Type: int
  Kind: FUNC_DEF, Value: main, Type: int
    Kind: SEQ
      Kind: VAR_DEF, Value: 14, Type: int
        Name: x, Type: int
      Kind: ASSIGN, Type: int
        Kind: VAR, Value: 14, Type: int
        Kind: FUNC_CALL, Value: 3, Type: int
          Kind: ARG
            Kind: CST, Value: 1, Type: int
          Kind: ARG
            Kind: CST, Value: 2, Type: int
      Kind: VAR_DEF, Value: 15, Type: int
        Name: array, Type: int (array), Length: 10
      Kind: ASSIGN, Type: int
        Kind: ELEMENT_ACCESS, Type: int
          Kind: VAR, Value: 15, Type: int (array), Length: 10
          Kind: CST, Value: 5, Type: int
        Kind: CST, Value: 1, Type: int
      Kind: VAR_DEF, Value: 16, Type: int
        Name: y, Type: int
      Kind: IFELSE
        Kind: AND, Type: int
          Kind: OR, Type: int
            Kind: EQUAL, Type: int
              Kind: LSHIFT, Type: int
                Kind: VAR, Value: 14, Type: int
                Kind: CST, Value: 4, Type: int
              Kind: CST, Value: 1, Type: int
            Kind: GREATER, Type: int
              Kind: VAR, Value: 14, Type: int
              Kind: CST, Value: 1, Type: int
          Kind: LESS, Type: int
            Kind: VAR, Value: 14, Type: int
            Kind: CST, Value: 10, Type: int
        Kind: SEQ
          Kind: ASSIGN, Type: int
            Kind: VAR, Value: 16, Type: int
            Kind: BITAND, Type: int
              Kind: VAR, Value: 14, Type: int
              Kind: CST, Value: 1, Type: int
        Kind: SEQ
          Kind: ASSIGN, Type: int
            Kind: VAR, Value: 16, Type: int
            Kind: BITOR, Type: int
              Kind: VAR, Value: 14, Type: int
              Kind: CST, Value: 1, Type: int
      Kind: RET_SYM, Type: int
        Kind: RSHIFT, Type: int
          Kind: DIV, Type: int
            Kind: MULT, Type: int
              Kind: VAR, Value: 14, Type: int
              Kind: VAR, Value: 16, Type: int
            Kind: CST, Value: 2, Type: int
          Kind: CST, Value: 1, Type: int
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
