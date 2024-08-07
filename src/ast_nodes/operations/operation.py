"""Representation of operation nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node


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
    """

    @override
    def __init__(self, id: int, lhs: Node, rhs: Node, **kwargs) -> None:
        super().__init__(id)

        self.lhs: Node = lhs
        self.rhs: Node = rhs

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
