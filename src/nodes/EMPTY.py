"""Representation of EMPTY nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from .base.node import Node


class EMPTY(Node):
    """
    Implement the representation of an `EMPTY` node for the AST.

    This class does not need to override any methods or properties of the
    base class other than the `symbol`.

    Parameters
    ----------
    id : int
        The ID of the Node.
    """

    @override
    def __init__(self, id: int, value: Union[int, str, None] = None) -> None:
        super().__init__(id, value)

        self.symbol: str = "(37)"
