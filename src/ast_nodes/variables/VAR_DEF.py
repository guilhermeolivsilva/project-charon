"""Representation of VAR_DEF nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.utils import get_variable_size


class VAR_DEF(Node):
    """
    Implement the representation of a variable definition for the AST.

    Parameters
    ----------
    variable_metadata : dict
        Dictionary of variable metadata exported by the Lexer.
    """

    @override
    def __init__(self, variable_metadata: dict) -> None:
        id: int = variable_metadata.get("id")
        type: str = variable_metadata.get("type")

        super().__init__(id, type)

        self.variable_metadata: dict = variable_metadata
        self.instruction: str = "ALLOC"

        prime: int = variable_metadata["prime"]
        self.size: int = get_variable_size(variable_metadata)
        self.symbol: str = f"({self.symbol})" + f"^({prime})" + f"^({self.size})"

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
            var_def_metadata += (
                f" (array), Length: {self.variable_metadata.get('length')}"
            )

        print(f"{'  ' * (indent + 1)}{var_def_metadata}")

    @override
    def generate_code(
        self, register: int
    ) -> tuple[int, list[dict[str, Union[int, str]]]]:
        """
        Generate the code associated with this `VAR_DEF`.

        For this node specialization, the generated code is an `ALLOC`
        instruction. The bytecode contains information about the type, and
        length, if it is an array.

        Parameters
        ----------
        register : int
            The number of the register to be used by the code generated by this
            Node.

        Returns
        -------
        register : int
            The number of the next register available.
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`and `value`.
        """

        code_metadata: list[dict[str, Union[int, str]]] = []

        var_def_code = {
            "instruction": self.instruction,
            "metadata": {"id": self.value, "size": self.size, "register": register},
        }
        register += 1

        code_metadata.append(var_def_code)

        return register, code_metadata
