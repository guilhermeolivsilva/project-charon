"""Representation of operation nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.ast_nodes.certificate_mapping import TYPE_SYMBOLS_MAP


class Operation(Node):
    """
    Implement the representation of an operation for the AST.

    An operation is either the addition (`ADD`), subtraction (`SUB`),
    comparison (`LT`), or attribution (`SET`) of two nodes.

    Parameters
    ----------
    id : int
        The ID of the Node.
    lhs : Node
        The Node representation of the left hand side of the operation.
    rhs : Node
        The Node representation of the right hand side of the operation.
    supports_float : bool (optional, default = True)
        Whether the operation supports floating point numbers.
    """

    @override
    def __init__(self, id: int, lhs: Node, rhs: Node, supports_float: bool = True, **kwargs) -> None:
        super().__init__(id)

        self.lhs: Node = lhs
        self.rhs: Node = rhs
        self.supports_float: bool = supports_float

        self.type: str = self._compute_operation_type()
        self.symbol: str = self._compute_symbol()

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `Operation` nodes, obtain the certificates, recursively, from the
        `lhs` and `rhs` subtrees first, and then from the `Operation` node
        itself.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """

        return [
            *self.lhs.get_certificate_label(),
            *self.rhs.get_certificate_label(),
            *super().get_certificate_label(),
        ]

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `Operation`.

        The node itself is aligned with `indent`, and its children are padded
        with an additional left space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)

        self.lhs.print(indent + 1)
        self.rhs.print(indent + 1)

    @override
    def generate_code(self) -> list[dict[str, Union[int, str, None]]]:
        """
        Generate the code associated with this `Operation`.

        For this node specialization, generate code from the left and right
        hand sides nodes first, and then from the node itself.

        Returns
        -------
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`, and node `id`, and `value`.
        """

        code_metadata = [
            *self.lhs.generate_code(),
            *self.rhs.generate_code(),
            *super().generate_code(),
        ]

        return code_metadata

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of the current `Operation`, and set this attribute.

        For `Operation` nodes, certificate the `lhs` and `rhs` children first,
        and then the `Operation` itself.

        Parameters
        ----------
        prime : int
            A prime number that represents the relative position of the `Node`
            in the AST.

        Returns
        -------
        : int
            A prime number that comes after the given `prime`.
        """

        prime = self.lhs.certificate(prime)
        prime = self.rhs.certificate(prime)

        return super().certificate(prime)
    
    def _compute_operation_type(self) -> str:
        """
        Compute the type this `Operation` will return.

        The type is set to be the least restrictive between the `lhs` and `rhs`
        children Nodes -- i.e., if `lhs` is `float`, and `rhs` is `int`, return
        `float`.

        This method also type checks: if the node does not support floating
        point numbers, but its type is `float`, it will raise a TypeError.

        Returns
        -------
        operation_type : str
            The type of this Operation.

        Raises
        ------
        TypeError
            - Raised if the `type` is detected to be `float`, but
            `supports_float` is set to `False`.
        """

        operation_type: str = ""

        lhs_type = self.lhs.get_type()
        lhs_type_symbol = TYPE_SYMBOLS_MAP.get(lhs_type).get("type_symbol")

        rhs_type = self.rhs.get_type()
        rhs_type_symbol = TYPE_SYMBOLS_MAP.get(rhs_type).get("type_symbol")

        if lhs_type_symbol > rhs_type_symbol:
            operation_type = lhs_type
        else:
            operation_type = rhs_type

        if operation_type == "float" and not self.supports_float:
            raise TypeError(
                f"{type(self).__name__} does not support floating point "
                "numbers. Check the parameters."
            )
        
        return operation_type

    def _compute_symbol(self) -> str:
        """
        Compute the symbol of this `Operation`.

        The symbol is composed by the basic symbol of the operation itself,
        plus the types of its left and right hand sides.

        Returns
        -------
        : str
            The symbol computed with left and right hand sides types.
        """

        lhs_type = self.lhs.get_type()
        lhs_type_symbol = TYPE_SYMBOLS_MAP.get(lhs_type).get("type_symbol")

        rhs_type = self.rhs.get_type()
        rhs_type_symbol = TYPE_SYMBOLS_MAP.get(rhs_type).get("type_symbol")

        return f"{self.symbol}^{lhs_type_symbol}^{rhs_type_symbol}"
    
    def _compute_instruction(self, base_instruction: str) -> str:
        """
        Compute `instruction` attribute to be used by an Operation node.

        Parameters
        ----------
        base_instruction : str
            The base instruction. It will receive an `F` as preffix if the
            Operation supports floating point numbers and is of `float` type.

        Returns
        -------
        instruction : str
            The instruction to be used by the Operation node.
        """

        instruction: str = ""

        if self.type == "float":
            instruction = f"F{base_instruction}"
        else:
            instruction = base_instruction

        return instruction