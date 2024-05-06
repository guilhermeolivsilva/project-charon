"""Representation of SUB nodes for the Abstract Syntax Tree."""

from typing_extensions import override
from .node import Node


class SUB(Node):
    """
    Implement the representation of a subtraction for the AST.

    This class overrides the constructor and `traverse` methods.

    Parameters
    ----------
    id : int
        The ID of the Node.
    lhs : Node
        The Node representation of the left hand side of the subtraction.
    rhs : Node
        The Node representation of the right hand side of the subtraction.
    """

    @override
    def __init__(self, id: int, lhs: Node, rhs: Node, **kwargs) -> None:
        super().__init__(id)

        self.lhs: Node = lhs
        self.rhs: Node = rhs

    @override
    def traverse(self, func: callable, **kwargs) -> None:
        """
        Apply the traversal `func` to the left and right hand nodes of the
        subtraction, and then to the `SUB` node itself.

        Parameters
        ----------
        func : callable
            The function to call during the traversal.
        """

        self.lhs.traverse(func, **kwargs)
        self.rhs.traverse(func, **kwargs)
        func(self, **kwargs)
