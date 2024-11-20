"""Representation of VAR nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.certificate_mapping import NODE_SYMBOLS_MAP
from src.ast_nodes.node import Node


class VAR(Node):
    """
    Implement the representation of a variable for the AST.

    Parameters
    ----------
    variable_metadata : dict[str, str]
        A dictionary containing the ID where it was first
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
    def generate_code(self, register: int) -> tuple[
        int,
        list[dict[str, Union[int, str]]]
    ]:
        """
        Generate the code associated with this `VAR`.

        For this node specialization, the code metadata contains the instruction
        (i.e., whether the context requires the variable's value or address),
        together with the variable identifier (`self.value`).
        
        It also contains `offset_size` and `offset_register` fields: this is due
        to the design of the `ADDRESS` and `LOAD` instructions in the virtual
        machine.

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
            Return a dictionary of code metadata: the related `instruction` and
            `value`.
        """

        code_metadata = {
            "instruction": self.instruction,
            "metadata": {

                "register": register,
                "value": self.value,
                "type": self.type
            }
        }

        return register + 1, [code_metadata]

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
        """

        context: str = context.get("context", "read")

        if context == "read":
            self.instruction: str = "LOAD"
            symbol: str = NODE_SYMBOLS_MAP.get("VAR_VALUE")

        else:
            self.instruction: str = "ADDRESS"
            symbol: str = NODE_SYMBOLS_MAP.get("VAR_ADDRESS")

        self.symbol: str = f"({symbol})^({self.variable_metadata['prime']})"
