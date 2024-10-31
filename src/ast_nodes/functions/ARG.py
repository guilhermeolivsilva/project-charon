"""Representation of ARG nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.basic.CST import CST
from src.ast_nodes.node import Node
from src.ast_nodes.variables.VAR import VAR


class ARG(Node):
    """
    Implement the representation of a function argument for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    argument_value : Union[CST, VAR]
        The node representation of this argument.
    """

    @override
    def __init__(self, id: int, argument_value: Union[CST, VAR]) -> None:
        super().__init__(id)

        self.argument_value: Union[CST, VAR] = argument_value

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `ARG` nodes, obtain the certificates, from the `argument_value` node
        first, and then from the `ARG` node itself.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """

        return [
            *self.argument_value.get_certificate_label(),
            *super().get_certificate_label()
        ]

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `ARG`.

        The node itself is aligned with `indent`, and `argument_value` is padded
        with an additional left space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)

        self.argument_value.print(indent=indent + 1)

    @override
    def generate_code(self, register: int) -> tuple[
        int,
        list[dict[str, Union[int, str, None]]]
    ]:
        """
        Generate the code associated with this `ARG`.

        For this node specialization, generate code from the `argument_value`
        node first, and then generate a `STORE` instruction to save the
        `argument_value` in the `arg` register.

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
            `instruction`, and node `id`, and `value`.
        """

        code_metadata: list[dict] = []

        register, argument_value_code = self.argument_value.generate_code(
            register=register
        )
        code_metadata.extend(argument_value_code)

        # ARG must point to the same register that contains the `argument_value`
        argument_value_register = argument_value_code[-1]["metadata"]["register"]
        argument_store_code = {
            "instruction": "MOV",
            "metadata": {
                "lhs_register": "arg",
                "rhs_register": argument_value_register,
                "type": self.type
            }
        }
        code_metadata.append(argument_store_code)

        return register, code_metadata

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of the this `ARG`, and set this attribute.

        For `ARG` nodes, certificate the `argument_value` node first, and then
        the `ARG` itself.

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

        prime = self.argument_value.certificate(prime)

        return super().certificate(prime)
