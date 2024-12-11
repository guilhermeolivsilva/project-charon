"""Representation of operation nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.utils import next_prime, type_cast, TYPE_SYMBOLS_MAP


class Operation(Node):
    """
    Implement the representation of an operation for the AST.

    Parameters
    ----------
    lhs : Node
        The Node representation of the left hand side of the operation.
    rhs : Node
        The Node representation of the right hand side of the operation.
    supports_float : bool (optional, default = True)
        Whether the operation supports floating point numbers.
    """

    @override
    def __init__(
        self,
        lhs: Node,
        rhs: Node,
        supports_float: bool = True,
        type: str = None,
        **kwargs
    ) -> None:
        super().__init__()

        self.lhs: Node = lhs
        self.rhs: Node = rhs
        self.supports_float: bool = supports_float

        if type is not None:
            self.type = type
        else:
            self.type: str = self._compute_operation_type()

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
    def generate_code(self, register: int) -> tuple[
        int,
        list[dict[str, Union[int, str, None]]]
    ]:
        """
        Generate the code associated with this `Operation`.

        For this node specialization, generate code from the left and right
        hand sides nodes first, and then from the node itself.

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

        code_metadata: list[dict[str, Union[int, str, None]]] = []

        register, lhs_code = self.lhs.generate_code(register=register)
        code_metadata.extend(lhs_code)

        if self.lhs.get_type() != self.get_type():
            register, lhs_typecast = type_cast(
                original_type=self.lhs.get_type(),
                target_type=self.get_type(),
                register=register
            )
            code_metadata.extend(lhs_typecast)

        lhs_register = register - 1

        register, rhs_code = self.rhs.generate_code(register=register)
        code_metadata.extend(rhs_code)

        if self.rhs.get_type() != self.get_type():
            register, rhs_typecast = type_cast(
                original_type=self.rhs.get_type(),
                target_type=self.get_type(),
                register=register
            )
            code_metadata.extend(rhs_typecast)

        rhs_register = register - 1

        this_code = {
            "instruction": self.instruction,
            "metadata": {
                "register": register,
                "lhs_register": lhs_register,
                "rhs_register": rhs_register
            }
        }
        register += 1

        code_metadata.append(this_code)

        return register, code_metadata

    @override
    def certificate(self, positional_prime: int) -> int:
        """
        Compute the certificate of the current `Operation`, and set this attribute.

        For `Operation` nodes, certificate the `lhs` and `rhs` children first,
        and then the `Operation` itself.

        Parameters
        ----------
        positional_prime : int
            A prime number that denotes the relative position of this node in
            the source code.

        Returns
        -------
        : int
            The prime that comes immediately after `positional_prime`.
        """

        operation_certificate_label = f"({self.symbol})"

        positional_prime = self.lhs.certificate(positional_prime)
        positional_prime = self.rhs.certificate(positional_prime)

        lhs_certificate_label = self.lhs.get_certificate_label().pop()
        operation_certificate_label += f"^({lhs_certificate_label})"

        rhs_certificate_label = self.rhs.get_certificate_label().pop()
        operation_certificate_label += f"^({rhs_certificate_label})"

        self.certificate_label = (
            f"{positional_prime}^"
            + f"({operation_certificate_label})"
        )

        return next_prime(positional_prime)
    
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
