"""Representation of EXPR nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node


class EXPR(Node):
    """
    Implement the representation of an expression for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    child_expression : Node
        The node representation of the child expression.
    """

    @override
    def __init__(self, id: int, child_expression: Node) -> None:
        super().__init__(id, uses_register=False)

        self.child_expression: Node = child_expression

        self.instruction: str = "POP"

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `EXPR` nodes, first obtain the certificate from the `child_expression`
        subtree, recursively, and then from the `EXPR` node itself.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """

        return [
            *self.child_expression.get_certificate_label(),
            *super().get_certificate_label(),
        ]

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `EXPR`.

        The node itself is aligned with `indent`, and its children are padded
        with an additional left space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)

        self.child_expression.print(indent + 1)

    @override
    def generate_code(self, register: int) -> tuple[
        int,
        list[dict[str, Union[int, str, None]]]
    ]:
        """
        Generate the code associated with this `EXPR`.

        For this node specialization, generate code from its `child_expression`
        first, and then from the node itself.
        
        Notice that the register may only be incremented by the
        `child_expression.generate_code` method. This Node does not increment
        the `register`, as it only adds a `POP` to the instructions list.

        Parameters
        ----------
        register : int
            The number of the register to be used by the code generated by this
            Node.

        Returns
        -------
        code_metadata : list of dict
            Return a dictionary of code metadata: the related `instruction`,
            and node `id`, and `value`.
        """

        register, child_expression_code = self.child_expression.generate_code(register=register)
        _, this_code = super().generate_code(register=register)

        code_metadata = [
            *child_expression_code,
            *this_code
        ]

        return register, code_metadata

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of the current `EXPR`, and set this attribute.

        For `EXPR` nodes, certificate the `child_expression`, recursively, and
        then the `EXPR` node itself.

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

        prime = self.child_expression.certificate(prime)

        return super().certificate(prime)
