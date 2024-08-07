"""Representation of CST nodes for the Abstract Syntax Tree."""

from typing_extensions import override
from typing import Union

from src.ast_nodes.node import Node


CONSTANT_TYPES = {
    "int": {
        "enforce": int,
        "exponent": 2
    },
    "float": {
        "enforce": float,
        "exponent": 3
    },
    "long": {
        "enforce": int,
        "exponent": 4
    }
}

class CST(Node):
    """
    Implement the representation of a constant for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    value : int or float
        The value of the constant.
    type : str
        The type of the constant.

    Raises
    ------
    TypeError
        Raised if the `type` parameter is not valid. `CONSTANT_TYPES`
        contains the currently supported types.
    """

    @override
    def __init__(self, id: int, value: Union[int, float], type: str) -> None:
        if type not in CONSTANT_TYPES:
            raise TypeError(f"Constant has invalid type '{type}'")

        _type_to_enforce: callable
        _exponent: int
        _type_to_enforce, _exponent = CONSTANT_TYPES[type].values()
        super().__init__(id, _type_to_enforce(value))

        self.type = type
        self.instruction: str = "PUSH"

        _exponent: int = CONSTANT_TYPES[type]["exponent"]
        self.symbol: str = (
            f"({self.symbol})^({self.value})^({_exponent})"
        )

    @override
    def __str__(self) -> str:
        return super().__str__() + f", Type: {self.type}"
