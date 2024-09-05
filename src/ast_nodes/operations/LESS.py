"""Representation of LESS nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from src.ast_nodes.node import Node

from src.ast_nodes.operations.operation import Operation


class LESS(Operation):
    """
    Implement the representation of a "less than" (<) comparison for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    lhs : Node
        The Node representation of the left hand side of the comparison.
    rhs : Node
        The Node representation of the right hand side of the comparison.
    """

    @override
    def __init__(self, id: int, lhs: Node, rhs: Node, **kwargs) -> None:
        super().__init__(id, lhs, rhs, **kwargs)

        self.instruction: str = self._compute_instruction("LT")
