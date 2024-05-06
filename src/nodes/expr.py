"""Representation of EXPR nodes for the Abstract Syntax Tree."""

from typing_extensions import override
from .node import Node


class EXPR(Node):
    """
    Implement the representation of an expression for the AST.

    This class overrides the constructor and `traverse` methods.

    Parameters
    ----------
    id : int
        The ID of the Node.
    child_expression : Node
        The node representation of the child expression.
    """

    @override
    def __init__(self, id: int, child_expression: Node) -> None:
        super().__init__(id)

        self.child_expression: Node = child_expression

    @override
    def traverse(self, func: callable, **kwargs) -> None:
        """
        Apply the traversal `func` to the child expression node, and then
        to the `EXPR` node itself.

        Parameters
        ----------
        func : callable
            The function to call during the traversal.
        """

        self.child_expression.traverse(func, **kwargs)
        func(self, **kwargs)
