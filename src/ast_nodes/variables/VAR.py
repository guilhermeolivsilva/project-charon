"""Representation of VAR nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.utils import get_certificate_symbol


class VAR(Node):
    """
    Implement the representation of a variable for the AST.

    Parameters
    ----------
    variable_metadata : dict[str, str]
        A dictionary containing the unique ID generated when it was first
        declared in the original source code, and its type.
    """

    @override
    def __init__(self, variable_metadata: dict[str, str]) -> None:
        id = variable_metadata.get("id")
        super().__init__(id)

        self.variable_metadata: dict[str, str] = variable_metadata
        self.id: int = id
        self.type = self.variable_metadata.get("type")

        # Handle the `instruction` and `symbol`. This defaults to the `read`
        # case, but can be changed by the AST as it is built
        self.add_context(context={"context": "read"})

    @override
    def __str__(self) -> str:
        new_str: str = super().__str__()

        array_length: Union[int, None] = self.variable_metadata.get("length")
        if array_length:
            new_str += f" (array), Length: {array_length}"

        return new_str

    @override
    def generate_code(
        self, register: int, environment: dict[str, dict[int, str]]
    ) -> tuple[
        list[dict[str, Union[int, str, float]]],
        int,
        dict[int, str]
    ]:
        """
        Generate the code associated with this `VAR`.

        For this node specialization, the code metadata contains the instruction
        (i.e., whether the context requires the variable's value or address),
        together with the variable identifier (`self.value`).

        Parameters
        ----------
        register : int
            The number of the register to be used by the code generated by this
            Node.
        environment : dict[int, str]
            The compiler's environment, that maps variables IDs to memory
            addresses and function IDs to instructions indices.

        Returns
        -------
        code : list of dict
            Return a list of dictionaries containing code metadata: the register
            to be used, the related `instruction` and its metadata.
        register : int
            The number of the next register available.
        environment : dict[int, str]
            The updated {var_id: address} environment mapping.
        """

        operation: str = self.context.get("context", "read")
        var_address = environment["variables"][self.id]["address"]

        code = [
            {
                "instruction": "CONSTANT",
                "metadata": {"register": register, "value": var_address}
            },
            {
                "instruction": "ADD",
                "metadata": {
                    "register": register + 1,
                    "lhs_register": register,
                    "rhs_register": "zero"
                },
            }
        ]

        register += 2

        if operation == "read":
            code.append({
                "instruction": "LOAD",
                "metadata": {"register": register, "value": register - 1}
            })

            register += 1

        return code, register, environment

    def get_metadata(self) -> dict[str, str]:
        """
        Get the metadata of this `VAR`.

        Returns
        -------
        : dict[str, str]
            The variable metadata.
        """

        return self.variable_metadata

    def add_context(self, context: dict[str, str]) -> None:
        """
        Add context to this `VAR` node.

        The context indicates whether this variable is being readed or written.

        Parameters
        ----------
        context : dict[str, str]
            The context of this variable use.

        Notes
        -----
        This method also changes the `symbol` attribute according to the
        instruction being used.
        """

        # Update the context
        self.context = context

        operation: str = context.get("context", "read")

        if operation == "read":
            symbol: str = get_certificate_symbol("VAR_VALUE")

        else:
            symbol: str = get_certificate_symbol("VAR_ADDRESS")

        # Add ^1 because it means memory offset + 1. As this is a regular
        # variable – and not an array nor struct –, the offset is always 0.
        self.symbol: str = (
            f"({symbol})" + f"^({self.variable_metadata['prime']})" + "^(2)" + "^(1)"
        )
