"""Representation of SUB nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from src.nodes.base.node import Node

from .base.operation import Operation


class SUB(Operation):
    """
    Implement the representation of a subtraction for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    lhs : Node
        The Node representation of the left hand side of the subtraction.
    rhs : Node
        The Node representation of the right hand side of the subtraction.
    """

    @override
    def __init__(self, id: int, lhs: Node, rhs: Node, **kwargs) -> None:
        super().__init__(id, lhs, rhs, **kwargs)

        self.instruction: str = "ISUB"
        self.symbol: str = "(33)"
