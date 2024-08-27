"""Representation of PROG nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node


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

        self.instruction: str = "HALT"
        self.children: list[Node] = []

    def add_child(self, child: Node) -> None:
        """
        Add a child Node to the `self.children` list.

        Parameters
        ----------
        child : Node
            The child to be added to the list.
        """

        self.children.append(child)

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `PROG` nodes, first obtain the certificate from each `child`
        subtree, recursively, and then from the `PROG` node itself.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """

        certificate_label: list[str] = []

        for child in self.children:
            certificate_label.extend(child.get_certificate_label())

        certificate_label.extend(super().get_certificate_label())

        return certificate_label

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

        for child in self.children:
            child.print(indent + 1)

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

        code_metadata: list[dict[str, Union[int, str, None]]] = []

        for child in self.children:
            code_metadata.extend(child.generate_code())

        code_metadata.append({
            "instruction": self.instruction,
            "id": self.id,
            "value": None
        })

        return code_metadata

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

        for child in self.children:
            prime = child.certificate(prime)

        return super().certificate(prime)
