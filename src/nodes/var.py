"""Representation of VAR nodes for the Abstract Syntax Tree."""

from typing import Union
from typing_extensions import override
from .node import Node


class VAR(Node):
    """
    Implement the representation of a variable for the AST.

    This class does not need to override any methods or properties of the
    base class.
    """

    @override
    def __init__(self, id: int, value: Union[str, None] = None) -> None:
        if value is not None and not isinstance(value, str):
            raise TypeError("VAR value must be a string or None.")

        super().__init__(id, value)
