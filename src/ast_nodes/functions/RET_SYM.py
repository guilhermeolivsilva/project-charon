"""Representation of RET_SYM nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.utils import next_prime, type_cast


class RET_SYM(Node):
    """
    Implement the representation of a function return for the AST.

    Parameters
    ----------
    function_call_metadata : dict
        Dictionary of function call metadata exported by the Lexer.
    type : str
        The type of the function this `RET_SYM` belongs to.
    """

    @override
    def __init__(self, returned_value: Node, type: str) -> None:
        super().__init__(uses_register=False)

        self.returned_value: Node = returned_value
        self.type: str = type

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `RET_SYM`.

        The node itself is aligned with `indent`, and the `returned_value` child
        is padded with an additional left space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)

        self.returned_value.print(indent + 1)

    @override
    def generate_code(self, register: int) -> tuple[
        int,
        list[dict[str, Union[int, str, None]]]
    ]:
        """
        Generate the code associated with this `RET_SYM`.

        For this node specialization, generate code from the `returned_value`
        child node first, and then from the `RET_SYM` itself.

        Notice that, if `RET_SYM.type` is different from `returned_value.type`,
        type cast instructions will be added to the generated code.

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

        register, returned_value_code = self.returned_value.generate_code(
            register=register
        )
        code_metadata.extend(returned_value_code)

        # Add a type cast to enforce the returned value to have the same type
        # as the function it is located in.
        returned_value_type = self.returned_value.get_type()
        function_return_type = self.get_type()

        if returned_value_type != function_return_type:
            register, returned_value_typecast = type_cast(
                original_type=returned_value_type,
                target_type=function_return_type,
                register=register
            )
            code_metadata.extend(returned_value_typecast)

        returned_value_code_register = register - 1

        # The code for the return operation itself is, essentially, a pair of
        # MOV (move data between registers) + JR (jump to register) pair.
        return_symbol_code = [
            {
                "instruction": "MOV",
                "metadata": {
                    "register": "ret_value",
                    "value": returned_value_code_register
                }
            },
            {
                "instruction": "JR",
                "metadata": {
                    "register": "ret_address"
                }
            }
        ]

        code_metadata.extend(return_symbol_code)

        return register, code_metadata

    @override
    def certificate(self, positional_prime: int) -> int:
        """
        Compute the certificate of the current `RET_SYM`, and set this attribute.

        For `RET_SYM` nodes, certificate the child `returned_value` first, and
        then the `RET_SYM` itself.

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

        positional_prime = self.returned_value.certificate(positional_prime)
        _returned_value_certificate = self.returned_value.get_certificate_label().pop()

        self.certificate_label = (
            f"{positional_prime}^"
            + f"(({self.symbol})^({_returned_value_certificate}))"
        )

        return next_prime(positional_prime)
