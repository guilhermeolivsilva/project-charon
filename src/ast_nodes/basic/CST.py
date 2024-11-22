"""Representation of CST nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from src.ast_nodes.node import Node
from src.ast_nodes.certificate_mapping import TYPE_SYMBOLS_MAP


class CST(Node):
    """
    Implement the representation of a constant for the AST.

    Parameters
    ----------
    constant_metadata : dict[str, str]
        A dictionary containing metadata (type and value) about this constant.

    Raises
    ------
    TypeError
        Raised if the `type` parameter is not valid. `CONSTANT_TYPES`
        contains the currently supported types.
    """

    @override
    def __init__(self, constant_metadata: dict[str, str]) -> None:
        value: int = constant_metadata.get("value")
        type: str = constant_metadata.get("type")

        if type not in TYPE_SYMBOLS_MAP:
            raise TypeError(f"Constant has invalid type '{type}'")

        _type_to_enforce: callable
        _, _type_to_enforce = TYPE_SYMBOLS_MAP[type].values()
        super().__init__(_type_to_enforce(value))

        self.type = type
        self.instruction: str = "CONSTANT"

        # We apply this linear transformation so we get rid of zeroes
        value_exponent = value + 1 if value >= 0 else value
        self.symbol: str = f"({self.symbol})^({value_exponent}))"
