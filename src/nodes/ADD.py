"""Representation of ADD nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from src.nodes.base.node import Node

from .base.operation import Operation


class ADD(Operation):
    """
    Implement the representation of an addition for the AST.

    This class simply is an interface for the `Operation` class.

    Parameters
    ----------
    id : int
        The ID of the Node.
    lhs : Node
        The Node representation of the left hand side of the addition.
    rhs : Node
        The Node representation of the right hand side of the addition.
    """

    @override
    def __init__(self, id: int, lhs: Node, rhs: Node, **kwargs) -> None:
        super().__init__(id, lhs, rhs, **kwargs)

        self.instruction: str = "IADD"
        self.symbol: str = "(42)"

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `Operation`.

        The node itself is aligned with `indent`, and its children are padded
        with an additional left space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)
