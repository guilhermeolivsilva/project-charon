"""Representation of SET nodes for the Abstract Syntax Tree."""

from string import ascii_lowercase
from typing_extensions import override
from .node import Node


class SET(Node):
    """
    Implement the representation of a attribution operation for the AST.

    This class does not need to override any methods or properties of the
    base class other than the constructor for type checking.
    """

    @override
    def __init__(self, id: int, value: str, child_expression: Node) -> None:
        if not isinstance(value, str) or value not in ascii_lowercase:
            err_msg = "Left hand side element of SET operation must be a"
            err_msg += " string that represents a variable ([a-z] interval)."
            raise TypeError(err_msg)

        super().__init__(id, value)

        self.child_expression = child_expression
