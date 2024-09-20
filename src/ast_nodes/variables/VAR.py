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
        A dictionary containing the relative position where it was first
        declared in the original source code, and its type.
    """

    @override
    def __init__(self, id: int, variable_metadata: dict[str, str]) -> None:
        relative_position = variable_metadata.get("relative_position")
        super().__init__(id, relative_position)

        self.instruction: str = "LOAD"
        self.symbol: str = f"({self.symbol})^({self.value})"
        self.relative_position: int = relative_position
        self.variable_metadata: dict[str, str] = variable_metadata
        self.type = self.variable_metadata.get("type")

    @override
    def __str__(self) -> str:
        new_str: str = super().__str__()

        array_length: Union[int, None] = self.variable_metadata.get("length")
        if array_length:
            new_str += f" (array), Length: {array_length}"

        return new_str

    def get_metadata(self) -> dict[str, str]:
        """
        Get the metadata of this `VAR`.

        Returns
        -------
        : dict[str, str]
            The variable metadata.
        """

        return self.variable_metadata
