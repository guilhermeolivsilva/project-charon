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

        self.variable_metadata: dict = variable_metadata
        self.instruction: str = "ALLOC"

        _type_certificate = self.variable_metadata.get("type_certificate")
        _length = self.variable_metadata.get("length", 1)

        self.symbol: str = (
            f"({self.symbol})^"
            + f"({_relative_position})^"
            + f"({_type_certificate})^"
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

        var_def_metadata: str = ""
        var_def_metadata += f"Name: {self.variable_metadata.get('name')}, "
        var_def_metadata += f"Type: {self.variable_metadata.get('type')}"

        if self.variable_metadata.get("length"):
            var_def_metadata += f" (array), Length: {self.variable_metadata.get('length')}"

        print(f"{' ' * (indent + 1)} {var_def_metadata}")
