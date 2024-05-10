"""Implement unit tests for the `src.cg` module."""

from typing import Union

import pytest

from src.code_generator import CodeGenerator
from src.nodes import *


def test_init() -> None:
    """Test the instantiation of CodeGenerator objects."""

    cg = CodeGenerator()

    assert cg.code_collection == []

def test_str() -> None:
    """Test the string representation of CodeGenerator objects."""

    cg = CodeGenerator()

    first_statement = SEQ(id=1)
    first_statement.add_child(
        ADD(
            id=2,
            lhs=CST(id=3, value=1),
            rhs=VAR(id=4, value="a")
        )
    )

    program = PROG(id=0)
    program.set_first_statement(first_statement)

    cg.generate_code(program)

    expected_result = "Instruction: EMPTY, ID: 1, Value: None\n"
    expected_result += "Instruction: IPUSH, ID: 3, Value: 1\n"
    expected_result += "Instruction: IFETCH, ID: 4, Value: a\n"
    expected_result += "Instruction: IADD, ID: 2, Value: None\n"
    expected_result += "Instruction: HALT, ID: 0, Value: None"

    assert str(cg) == expected_result

def test_generate_code() -> None:
    """
    Test the `CodeGenerator.generate_code` method.
    
    This test is omitted because all of its possibilities are covered by the
    following tests.
    """
    
    ...
