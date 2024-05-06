"""Representation of operation nodes for the Abstract Syntax Tree."""

from typing_extensions import override
from .node import Node


class Operation(Node):
    """
    Implement the representation of an operation for the AST.

    An operation is either the addition (`ADD`), subtraction (`SUB`), or
    comparison (`LT`) of two nodes.

    This class overrides the constructor and `traverse` methods.

    Parameters
    ----------
    id : int
        The ID of the Node.
    lhs : Node
        The Node representation of the left hand side of the operation.
    rhs : Node
        The Node representation of the right hand side of the operation.
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
        addition, and then to the parent node itself.

        Parameters
        ----------
        func : callable
            The function to call during the traversal.
        """

        self.lhs.traverse(func, **kwargs)
        self.rhs.traverse(func, **kwargs)
        func(self, **kwargs)
