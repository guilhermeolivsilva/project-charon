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

        self.variable_metadata: dict[str, str] = variable_metadata
        self.relative_position: int = relative_position
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
            symbol: str = NODE_SYMBOLS_MAP.get("VAR_READ")

        else:
            self.instruction: str = "ADDRESS"
            symbol: str = NODE_SYMBOLS_MAP.get("VAR_WRITE")

        self.symbol: str = f"({symbol})^({self.variable_metadata['prime']})"
