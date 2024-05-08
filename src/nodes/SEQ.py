"""Representation of SEQ nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from .base.node import Node


class SEQ(Node):
    """
    Implement the representation of a sequence of statements for the AST.

    This class overrides the constructor and `traverse` methods.

    Parameters
    ----------
    id : int
        The ID of the Node.
    """

    @override
    def __init__(self, id: int) -> None:
        super().__init__(id)

        self.children: list[Node] = []

    def add_child(self, child: Node) -> None:
        """
        Add a child Node to the `self.children` list.

        Parameters
        ----------
        child : Node
            The child to be added to the list.
        """

        self.children.append(child)

    @override
    def traverse(self, func: callable, **kwargs) -> None:
        """
        Apply the traversal `func` to the `SEQ` node itself, and then
        to each of its children.

        Parameters
        ----------
        func : callable
            The function to call during the traversal.
        """

        func(self, **kwargs)

        for child in self.children:
            child.traverse(func, **kwargs)

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `Conditional`.

        The node itself is aligned with `indent`, and its children are padded
        with an additional left space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)

        for child in self.children:
            child.print(indent + 1)
