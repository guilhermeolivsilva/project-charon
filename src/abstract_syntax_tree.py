"""Implement the Abstract Syntax Tree (AST)."""

from src.node import Node


class AbstractSyntaxTree:
    """
    Implement the AST itself.

    The AST is always initialized with a root, with ID 0.
    """

    def __init__(self) -> None:
        self.root: Node = Node(id=0, kind="PROG")

    # TODO: assert no IDs are duplicate.
    # TODO: implement a tree traversal method.
