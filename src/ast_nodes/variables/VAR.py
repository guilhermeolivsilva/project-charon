"""Representation of VAR nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from src.ast_nodes.node import Node


class VAR(Node):
    """
    Implement the representation of a variable for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    pseudonymous : str
        The pseudonymous of the variable, that reflects the relative position
        where it was first declared in the original source code.
    """

    @override
    def __init__(self, id: int, pseudonymous: str) -> None:
        # Clip the `%` sign from the pseudonymous computed by the Lexer,
        # and cast it to `int`.
        _relative_position: int = int(pseudonymous[1:])

        super().__init__(id, _relative_position)

        self.instruction: str = "FETCH"
        self.symbol: str = f"({self.symbol})^({self.value})"
        self.relative_position: int = _relative_position
