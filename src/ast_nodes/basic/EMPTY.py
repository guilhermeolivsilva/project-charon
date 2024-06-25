"""Representation of EMPTY nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node


class EMPTY(Node):
    """
    Implement the representation of an `EMPTY` node for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    """

    @override
    def __init__(self, id: int, value: Union[int, str, None] = None) -> None:
        super().__init__(id, value)

        self.symbol: str = "(27)"
