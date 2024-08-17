"""Representation of SCOPE nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node


class SCOPE(Node):
    """
    Implement the representation of a `SCOPE` node for the AST.

    A `SCOPE` is an abstraction of the boundaries of a scope: `global`, `main`,
    or user defined functions. The node itself only has children to help
    structuring the scope, but doesn't have any semantics itself, `instruction`,
    or has a certificate.

    Parameters
    ----------
    scope_name : str
        The name of the scope.
    """

    @override
    def __init__(self, scope_name: str, value: Union[int, str, None] = None) -> None:
        super().__init__(scope_name, value)

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

        For `SCOPE` nodes, obtain the certificates, recursively, from the
        `children` nodes. The `SCOPE` node itself does not have a certificate.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """

        certificate_label: list[str] = []

        for child in self.children:
            certificate_label.extend(child.get_certificate_label())

        return certificate_label

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `SCOPE`.

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
        Generate the code for this `SCOPE`.

        For this node specialization, generate the code from its `children`,
        recursively and in order. The `SCOPE` node itself does not have an
        associated instruction.

        Returns
        -------
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`, and node `id`, and `value`.
        """

        code_metadata: list[dict[str, Union[int, str, None]]] = []

        for child in self.children:
            code_metadata.extend(child.generate_code())

        return code_metadata

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of this `SCOPE`.

        To achieve this, certificate its `children`, recursively and in order.
        The `SCOPE` node itself does not have a certificate.

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

        return prime
