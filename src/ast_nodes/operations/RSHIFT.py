"""Representation of RSHIFT nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from src.ast_nodes.node import Node

from src.ast_nodes.operations.operation import Operation


class RSHIFT(Operation):
    """
    Implement the representation of a right shift operation (>>) for the AST.

    Parameters
    ----------
    lhs : Node
        The Node representation of the left hand side of the operation.
    rhs : Node
        The Node representation of the right hand side of the operation.
    """

    @override
    def __init__(self, lhs: Node, rhs: Node, **kwargs) -> None:
        super().__init__(lhs, rhs, supports_float=False, **kwargs)

        self.instruction: str = "RSHIFT"
