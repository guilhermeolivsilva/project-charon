"""Implement unit tests for the `src.cg` module."""

from typing import Union

import pytest

# Just to annotate functions with fixtures.
from pytest_mock.plugin import MockerFixture

from src.code_generator import CodeGenerator
from src.node import Node


def test_init() -> None:
    """Test the instantiation of CodeGenerator objects."""

    cg = CodeGenerator()

    assert cg.code_collection == []

def test_str() -> None:
    """Test the string representation of CodeGenerator objects."""

    cg = CodeGenerator()

    test_nodes = [
        Node(id=1, kind="CST", value=23),
        Node(id=2, kind="VAR", value="a")
    ]

    for node in test_nodes:
        cg.generate_code(node)

    expected_result = "Instruction: IPUSH, Node: (ID: 1, Kind: CST, Value: 23)\n"
    expected_result += "Instruction: IFETCH, Node: (ID: 2, Kind: VAR, Value: a)"

    assert str(cg) == expected_result

def test_generate_code() -> None:
    """
    Test the `CodeGenerator.generate_code` method.
    
    This test is omitted because all of its possibilities are covered by the
    following tests.
    """
    
    ...


def test_parse_simple_node() -> None:
    """
    Test the `CodeGenerator.parse_simple_node` method.
    
    This test is omitted because all of its possibilities are covered by the
    following tests.
    """

    ...


@pytest.mark.parametrize(
    "node, children, expected_result",
    [
        (
            # node
            Node(id=1, kind="CST", value=23),

            # children
            None,

            # expected_result
            [
                ("IPUSH", Node(id=1, kind="CST", value=23))
            ]
        ),
        (
            # node
            Node(id=1, kind="VAR", value="a"),

            # children
            None,

            # expected_result
            [
                ("IFETCH", Node(id=1, kind="VAR", value="a"))
            ]
        ),
        (
            # node
            Node(id=1, kind="ADD"),

            # children
            [
                Node(id=2, kind="CST", value=1),
                Node(id=3, kind="VAR", value="a")
            ],

            # expected_result
            [
                ("IPUSH", Node(id=2, kind="CST", value=1)),
                ("IFETCH", Node(id=3, kind="VAR", value="a")),
                ("IADD", Node(id=1, kind="ADD"))
            ]
        ),
        (
            # node
            Node(id=1, kind="SUB"),

            # children
            [
                Node(id=2, kind="CST", value=1),
                Node(id=3, kind="VAR", value="a")
            ],

            # expected_result
            [
                ("IPUSH", Node(id=2, kind="CST", value=1)),
                ("IFETCH", Node(id=3, kind="VAR", value="a")),
                ("ISUB", Node(id=1, kind="SUB"))
            ]
        ),
        (
            # node
            Node(id=1, kind="LT"),

            # children
            [
                Node(id=2, kind="CST", value=1),
                Node(id=3, kind="VAR", value="a")
            ],

            # expected_result
            [
                ("IPUSH", Node(id=2, kind="CST", value=1)),
                ("IFETCH", Node(id=3, kind="VAR", value="a")),
                ("ILT", Node(id=1, kind="LT"))
            ]
        )
    ]
)
def test_generate_code_simple_node(
    node: Node,
    children: Union[list[Node], None],
    expected_result: list[tuple[str, Node]],
    mocker: MockerFixture
) -> None:
    """
    Test the `CodeGenerator.generate_code` method for simple nodes.

    A simple node is of `VAR`, `CST`, `ADD`, `SUB` or `LT` kind.

    This test also asserts that the `parse_simple_node` method has been called.

    Parameters
    ----------
    node : Node
        The Node of reference.
    expected_result : list of tuples (str, Node)
        A list of tuples of expected string and Node (that represents,
        respectively, an instruction and its reference Node).
    """

    # Add children to the reference node, if any.
    if children:
        for child in children:
            node.add_child(child)

    cg = CodeGenerator()
    cg.parse_simple_node = mocker.spy(cg, "parse_simple_node")
    cg.generate_code(node)

    cg.parse_simple_node.assert_called()
    
    # Must split the expected result and assert each item separately because
    # direct comparisons will fail. The `Node` objects aren't actually the
    # same, but are equal if attribute-wise compared.
    for result, expected in zip(cg.code_collection, expected_result):
        expected_instruction, expected_node = result
        instruction, reference_node = expected
    
        assert instruction == expected_instruction
        assert reference_node == expected_node


def test_generate_code_set_node(mocker: MockerFixture) -> None:
    """Test the `CodeGenerator.generate_code` method for `SET` nodes."""

    cg = CodeGenerator()
    cg.parse_set_node = mocker.spy(cg, "parse_set_node")

    node = Node(id=1, kind="SET")
    lhs = Node(id=2, kind="VAR", value="a")
    rhs = Node(id=3, kind="VAR", value="b")
    node.add_child(lhs)
    node.add_child(rhs)

    cg.generate_code(node)

    cg.parse_set_node.assert_called()

    expected_result = [
        ("IFETCH", rhs),
        ("ISTORE", lhs)
    ]

    # In this case, we can check the equality directly because the expected
    # result uses the exact same `Node` objects.
    assert cg.code_collection == expected_result


def test_generate_code_if_node(mocker: MockerFixture) -> None:
    """Test the `CodeGenerator.generate_code` method for `IF` nodes."""

    cg = CodeGenerator()
    cg.parse_if_node = mocker.spy(cg, "parse_if_node")

    node = Node(id=1, kind="IF")

    expr = Node(id=2, kind="LT")
    expr_lhs = Node(id=3, kind="VAR", value="a")
    expr.add_child(expr_lhs)
    expr_rhs = Node(id=4, kind="CST", value=1)
    expr.add_child(expr_rhs)
    node.add_child(expr)

    if_statement = Node(id=5, kind="SET")
    if_statement_lhs = Node(id=6, kind="VAR", value="b")
    if_statement.add_child(if_statement_lhs)
    if_statement_rhs = Node(id=7, kind="CST", value=2)
    if_statement.add_child(if_statement_rhs)
    node.add_child(if_statement)

    cg.generate_code(node)

    cg.parse_if_node.assert_called()

    expected_result = [
        ('IFETCH', expr_lhs),
        ('IPUSH', expr_rhs),
        ('ILT', expr),
        ('JZ', if_statement_rhs),
        ('IPUSH', if_statement_rhs),
        ('ISTORE', if_statement_lhs)
    ]

    # In this case, we can check the equality directly because the expected
    # result uses the exact same `Node` objects.
    assert cg.code_collection == expected_result


def test_generate_code_ifelse_node(mocker: MockerFixture) -> None:
    """Test the `CodeGenerator.generate_code` method for `IFELSE` nodes."""

    cg = CodeGenerator()
    cg.parse_if_else_node = mocker.spy(cg, "parse_if_else_node")

    node = Node(id=1, kind="IFELSE")

    expr = Node(id=2, kind="LT")
    expr_lhs = Node(id=3, kind="VAR", value="a")
    expr.add_child(expr_lhs)
    expr_rhs = Node(id=4, kind="CST", value=1)
    expr.add_child(expr_rhs)

    if_statement = Node(id=5, kind="SET")
    if_statement_lhs = Node(id=6, kind="VAR", value="b")
    if_statement.add_child(if_statement_lhs)
    if_statement_rhs = Node(id=7, kind="CST", value=2)
    if_statement.add_child(if_statement_rhs)

    else_statement = Node(id=8, kind="SET")
    else_statement_lhs = Node(id=9, kind="VAR", value="b")
    else_statement.add_child(else_statement_lhs)
    else_statement_rhs = Node(id=10, kind="CST", value=10)
    else_statement.add_child(else_statement_rhs)

    node.add_child(expr)
    node.add_child(if_statement)
    node.add_child(else_statement)

    cg.generate_code(node)

    expected_result = [
        ('IFETCH', expr_lhs),
        ('IPUSH', expr_rhs),
        ('ILT', expr),
        ('JZ', else_statement_lhs),
        ('IPUSH', if_statement_rhs),
        ('ISTORE', if_statement_lhs),
        ('JMP', else_statement_rhs),
        ('IPUSH', else_statement_rhs),
        ('ISTORE', else_statement_lhs)
    ]

    # In this case, we can check the equality directly because the expected
    # result uses the exact same `Node` objects.
    assert cg.code_collection == expected_result
