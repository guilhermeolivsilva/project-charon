"""Representation of DIV nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from src.ast_nodes.node import Node

from src.ast_nodes.operations.operation import Operation


class DIV(Operation):
    """
    Implement the representation of a division for the AST.

    Parameters
    ----------
    lhs : Node
        The Node representation of the left hand side of the division.
    rhs : Node
        The Node representation of the right hand side of the division.
    """

    @override
    def __init__(self, lhs: Node, rhs: Node, **kwargs) -> None:
        super().__init__(lhs, rhs, **kwargs)

        self.instruction: str = self._compute_instruction("DIV")