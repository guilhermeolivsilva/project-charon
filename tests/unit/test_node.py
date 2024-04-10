"""Implement unit tests for the `src.node.Node` class."""

from src.node import Node


def test_init():
    """Test the instantiation of Node objects."""

    node_id = 1
    node_kind = "TEST"

    node = Node(
        id=node_id,
        kind=node_kind
    )

    assert node.id == node_id
    assert node.kind == node_kind
    assert node.value is None
    assert node.parent is None
    assert node.children == []


def test_eq():
    """Test the equality operator between Node objects."""

    args_a = {
        "id": 1,
        "kind": "TEST",
        "value": 23
    }

    args_b = {
        "id": 2,
        "kind": "TEST",
        "value": 35
    }

    lhs = Node(**args_a)
    rhs_a = Node(**args_a)
    rhs_b = Node(**args_b)

    assert lhs == rhs_a
    assert lhs != rhs_b


def test_str():
    """Test the string representation of Node objects."""

    node_id = 1
    node_kind = "TEST"
    node_value = 1

    node = Node(
        id=node_id,
        kind=node_kind,
        value=node_value
    )

    assert str(node) == f"ID: {node_id}, Value: {node_value}, Kind: {node_kind}"


def test_add_child():
    """Test the `Node.add_child` method."""

    parent_node = Node(id=1, kind="TEST")
    child_node = Node(id=2, kind="TEST")

    parent_node.add_child(child_node)

    assert child_node in parent_node.children


def test_add_parent():
    """Test the `Node.add_parent` method."""

    parent_node = Node(id=1, kind="TEST")
    child_node = Node(id=2, kind="TEST")

    child_node.add_parent(parent_node)

    assert parent_node == child_node.parent
