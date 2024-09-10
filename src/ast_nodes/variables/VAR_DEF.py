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
        relative_position: int = variable_metadata.get("relative_position")
        super().__init__(id, relative_position)

        self.variable_metadata: dict = variable_metadata
        self.instruction: str = "ALLOC"

        _length = self.variable_metadata.get("length", 1)

        # The `type_certificate` is a placeholder! The `frontend` certificator
        # is responsible for filling it later.
        self.symbol: str = (
            f"({self.symbol})^"
            + f"({relative_position})^"
            + "({type_certificate})^"
            + f"({_length})"
        )

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `VAR_DEF`.

        The node itself is aligned with `indent`, and the information about its
        attributes is padded with an additional left space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)

        var_def_metadata: str = f"Name: {self.variable_metadata.get('name')}, "
        var_def_metadata += f"Type: {self.variable_metadata.get('type')}"

        if self.variable_metadata.get("length"):
            var_def_metadata += f" (array), Length: {self.variable_metadata.get('length')}"

        print(f"{'  ' * (indent + 1)}{var_def_metadata}")
