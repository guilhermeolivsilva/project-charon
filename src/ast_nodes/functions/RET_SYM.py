"""Representation of RET_SYM nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node


class RET_SYM(Node):
    """
    Implement the representation of a function return for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    function_call_metadata : dict
        Dictionary of function call metadata exported by the Lexer.
    """

    @override
    def __init__(self, id: int, returned_value: Node) -> None:
        super().__init__(id)

        self.instruction: str = "RET"
        self.returned_value: Node = returned_value

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `RET_SYM` nodes, obtain the certificates, recursively, from the
        `returned_value` subtree first, and then from the `RET_SYM` node itself.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """

        certificate_label: list[str] = [
            *self.returned_value.get_certificate_label(),
            *super().get_certificate_label(),
        ]

        return certificate_label

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
    def generate_code(self) -> list[dict[str, Union[int, str, None]]]:
        """
        Generate the code associated with this `RET_SYM`.

        For this node specialization, generate code from the `returned_value`
        child node first, and then from the `RET_SYM` itself.

        Returns
        -------
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`, and node `id`, and `value`.
        """

        code_metadata: list[dict] = [
            *self.returned_value.generate_code(),
            *super().generate_code(),
        ]

        return code_metadata

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of the current `RET_SYM`, and set this attribute.

        For `RET_SYM` nodes, certificate the child `returned_value` first, and
        then the `RET_SYM` itself.

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

        prime = self.returned_value.certificate(prime)

        return super().certificate(prime)
