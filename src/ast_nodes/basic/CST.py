"""Representation of CST nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from src.ast_nodes.node import Node


class CST(Node):
    """
    Implement the representation of a constant for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    value : int
        The value of the constant.
    """

    @override
    def __init__(self, id: int, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("CST value must be an integer.")

        super().__init__(id, value)

        self.instruction: str = "IPUSH"
        self.symbol: str = f"(29^{self.value})"
