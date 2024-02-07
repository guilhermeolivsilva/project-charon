"""Implement unit tests for the classes defined in `abstract_suntax_tree`."""

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

    assert str(node) == f"ID: {node_id}, Kind: {node_kind}, Value: {node_value}"


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
