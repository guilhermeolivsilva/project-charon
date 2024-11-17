"""Representation of SUB nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from src.ast_nodes.node import Node

from src.ast_nodes.operations.operation import Operation


class SUB(Operation):
    """
    Implement the representation of a subtraction for the AST.

    Parameters
    ----------
    lhs : Node
        The Node representation of the left hand side of the subtraction.
    rhs : Node
        The Node representation of the right hand side of the subtraction.
    """

    @override
    def __init__(self, lhs: Node, rhs: Node, **kwargs) -> None:
        super().__init__(lhs, rhs, **kwargs)

        self.instruction: str = self._compute_instruction("SUB")
