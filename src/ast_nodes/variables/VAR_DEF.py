"""Representation of VAR_DEF nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from src.ast_nodes.node import Node


class VAR_DEF(Node):
    """
    Implement the representation of a variable definition for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    variable_metadata : dict
        Dictionary of variable metadata exported by the Lexer.
    """

    @override
    def __init__(self, id: int, variable_metadata: dict) -> None:
        # Clip the `%` sign from the pseudonymous computed by the Lexer,
        # and cast it to `int`.
        _pseudonymous: str = variable_metadata.get("pseudonymous")
        _relative_position: int = int(_pseudonymous[1:])

        super().__init__(id, _relative_position)

        self.instruction: str = "ALLOC"
        self.type_certificate = variable_metadata.get("type_certificate")
        self.length = variable_metadata.get("length", 1)

        self.symbol: str = (
            f"({self.symbol})^"
            + f"({_relative_position})^"
            + f"({self.type_certificate})^"
            + f"({self.length})"
        )
