"""Representation of ASSIGN nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.utils import next_prime

from src.ast_nodes.node import Node
from src.ast_nodes.operations.operation import Operation


class ASSIGN(Operation):
    """
    Implement the representation of a attribution operation for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    lhs : Node
        The node representation of the variable to attribute to.
    rhs : Node
        The node representation of the expression to be attributed to `lhs`.
    """

    @override
    def __init__(self, id: int, lhs: Node, rhs: Node) -> None:
        super().__init__(id, lhs=lhs, rhs=rhs)

        self.instruction: str = "STORE"
