"""Representation of SET nodes for the Abstract Syntax Tree."""

from string import ascii_lowercase
from typing_extensions import override

from .base.node import Node


class SET(Node):
    """
    Implement the representation of a attribution operation for the AST.

    This class overrides the constructor and `traverse` methods.

    Parameters
    ----------
    id : int
        The ID of the Node.
    value : str
        The variable to attribute to. Must be a single, lower case character.
    child_expression : Node
        The node representation of the child expression.
    """

    @override
    def __init__(self, id: int, value: str, child_expression: Node) -> None:
        if not isinstance(value, str) or value not in ascii_lowercase:
            err_msg = "Left hand side element of SET operation must be a"
            err_msg += " string that represents a variable ([a-z] interval)."
            raise TypeError(err_msg)

        super().__init__(id, value)

        self.child_expression: Node = child_expression

    @override
    def traverse(self, func: callable, **kwargs) -> None:
        """
        Apply the traversal `func` to the child expression node, and then
        to the `SET` node itself.

        Parameters
        ----------
        func : callable
            The function to call during the traversal.
        """

        self.child_expression.traverse(func, **kwargs)
        func(self, **kwargs)
