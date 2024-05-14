"""Representation of EXPR nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from .base.node import Node


class EXPR(Node):
    """
    Implement the representation of an expression for the AST.

    This class overrides the constructor and `traverse` methods.

    Parameters
    ----------
    id : int
        The ID of the Node.
    child_expression : Node
        The node representation of the child expression.
    """

    @override
    def __init__(self, id: int, child_expression: Node) -> None:
        super().__init__(id)

        self.child_expression: Node = child_expression

        self.instruction: str = "IPOP"
        self.symbol: str = "(31)"

    @override
    def traverse(self, func: callable, **kwargs) -> None:
        """
        Apply the traversal `func` to the child expression node, and then
        to the `EXPR` node itself.

        Parameters
        ----------
        func : callable
            The function to call during the traversal.
        """

        self.child_expression.traverse(func, **kwargs)
        func(self, **kwargs)

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
    def generate_code(self) -> list[dict[str, Union[int, str, None]]]:
        """
        Generate the code associated with this `EXPR`.

        For this node specialization, generate code from its `child_expression`
        first, and then from the node itself.

        Returns
        -------
        code_metadata : list of dict
            Return a dictionary of code metadata: the related `instruction`,
            and node `id`, and `value`.
        """

        code_metadata = [
            *self.child_expression.generate_code(),
            *super().generate_code()
        ]

        return code_metadata

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
