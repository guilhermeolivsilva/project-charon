"""Representation of CST nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from src.ast_nodes.node import Node
from src.ast_nodes.certificate_mapping import TYPE_SYMBOLS_MAP


class CST(Node):
    """
    Implement the representation of a constant for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    constant_metadata : dict[str, str]
        A dictionary containing metadata (type and value) about this constant.

    Raises
    ------
    TypeError
        Raised if the `type` parameter is not valid. `CONSTANT_TYPES`
        contains the currently supported types.
    """

    @override
    def __init__(self, id: int, constant_metadata: dict[str, str]) -> None:
        value = constant_metadata.get("value")
        type = constant_metadata.get("type")

        if type not in TYPE_SYMBOLS_MAP:
            raise TypeError(f"Constant has invalid type '{type}'")

        _type_symbol: int
        _type_to_enforce: callable

        _type_symbol, _type_to_enforce = TYPE_SYMBOLS_MAP[type].values()
        super().__init__(id, _type_to_enforce(value))

        self.type = type
        self.instruction: str = "PUSH"
        self.symbol: str = f"({self.symbol})^({self.value})^({_type_symbol})"
