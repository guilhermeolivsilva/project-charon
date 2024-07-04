"""Representation of VAR nodes for the Abstract Syntax Tree."""

from string import ascii_lowercase
from typing_extensions import override

from src.ast_nodes.node import Node


class VAR(Node):
    """
    Implement the representation of a variable for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    value : str
        The variable to attribute to. Must be a single, lower case character.
    """

    @override
    def __init__(self, id: int, value: str) -> None:
        value_is_str = isinstance(value, str)
        value_is_ascii_lowercase = value in ascii_lowercase
        value_is_single_letter = len(value) == 1

        typecheck = value_is_str and value_is_ascii_lowercase and value_is_single_letter

        if not typecheck:
            raise TypeError("VAR value must be a valid variable name ([a-z]).")

        super().__init__(id, value)

        self.instruction: str = "IFETCH"
        self.symbol: str = f"{self.symbol}^{self.value}"
