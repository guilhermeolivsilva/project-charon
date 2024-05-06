"""Representation of VAR nodes for the Abstract Syntax Tree."""

from string import ascii_lowercase
from typing_extensions import override
from .base.node import Node


class VAR(Node):
    """
    Implement the representation of a variable for the AST.

    This class does not need to override any methods or properties of the
    base class other than the constructor for type checking.
    """

    @override
    def __init__(self, id: int, value: str) -> None:
        if not isinstance(value, str) and value not in ascii_lowercase:
            raise TypeError("VAR value must be a valid variable name ([a-z]).")

        super().__init__(id, value)
