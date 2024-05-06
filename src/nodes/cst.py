"""Representation of CST nodes for the Abstract Syntax Tree."""

from typing_extensions import override
from .base.node import Node



class CST(Node):
    """
    Implement the representation of a constant for the AST.

    This class does not need to override any methods or properties of the
    base class other than the constructor for type checking.
    """

    @override
    def __init__(self, id: int, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("CST value must be an integer.")

        super().__init__(id, value)
