"""Representation of CST nodes for the Abstract Syntax Tree."""

from typing import Union
from typing_extensions import override
from .node import Node



class CST(Node):
    """
    Implement the representation of a constant for the AST.

    This class does not need to override any methods or properties of the
    base class.
    """

    @override
    def __init__(self, id: int, value: Union[int, None] = None) -> None:
        if value is not None and not isinstance(value, int):
            raise TypeError("CST value must be an integer or None.")

        super().__init__(id, value)
