"""Representation of PROG nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from .base.node import Node


class PROG(Node):
    """
    Implement the representation of the beginning of a program for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    """

    @override
    def __init__(self, id: int) -> None:
        super().__init__(id)

        self.first_statement: Node = None
        self.symbol: str = "(35)"

    def set_first_statement(self, first_statement: Node) -> None:
        """
        Set the first statement of the program.

        Parameters
        ----------
        first_statement : Node
            The node that represents the first statement.
        """

        self.first_statement = first_statement

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `PROG` nodes, first obtain the certificate from the
        `first_statement` subtree, recursively, and then from the `PROG` node
        itself.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """
        
        return [
            *self.first_statement.get_certificate_label(),
            *super().get_certificate_label()
        ]

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `PROG`.

        The node itself is aligned with `indent`, and its children are padded
        with an additional left space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)

        self.first_statement.print(indent + 1)

    @override
    def generate_code(self) -> list[dict[str, Union[int, str, None]]]:
        """
        Generate the code associated with this `PROG`.

        For this node specialization, generate code from the `first_statement`
        (i.e., the program itself) and then add an ending instruction (`HALT`)
        to the code.

        Returns
        -------
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`, and node `id`, and `value`.
        """

        _program_end = {"instruction": "HALT", "id": self.id, "value": None}

        _program_code = self.first_statement.generate_code()

        return [*_program_code, _program_end]

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of `PROG`, and set this attribute.

        For `PROG` nodes, certificate the `first_statement`, recursively, and
        then the `PROG` node itself.

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

        prime = self.first_statement.certificate(prime)

        return super().certificate(prime)
