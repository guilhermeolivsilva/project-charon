"""Representation of VAR nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node


class VAR(Node):
    """
    Implement the representation of a variable for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    variable_metadata : dict[str, str]
        A dictionary containing the pseudonymous of the variable, that reflects
        the relative position where it was first declared in the original source
        code.
    """

    @override
    def __init__(self, id: int, variable_metadata: dict[str, str]) -> None:
        # Clip the `%` sign from the pseudonymous computed by the Lexer,
        # and cast it to `int`.
        pseudonymous = variable_metadata.get("pseudonymous")
        _relative_position: int = int(pseudonymous[1:])

        super().__init__(id, _relative_position)

        self.instruction: str = "FETCH"
        self.symbol: str = f"({self.symbol})^({self.value})"
        self.relative_position: int = _relative_position
        self.variable_metadata: dict[str, str] = variable_metadata
        self.type = self.variable_metadata.get("type")

    @override
    def __str__(self) -> str:
        new_str: str = super().__str__() + f", Type: {self.type}"

        array_length: Union[int, None] = self.variable_metadata.get("length")
        if array_length:
            new_str += f" (array), Length: {array_length}"

        return new_str
