"""Representation of conditionals for the Abstract Syntax Tree."""

from typing_extensions import override

from .node import Node


class Conditional(Node):
    """
    Implement the representation of conditionals for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    parenthesis_expression : Node
        The node representation of the expression to be evaluated.
    statement_if_true : Node
        The node representation of code to run if the `parenthesis_expression`
        evaluates to `True`.
    """

    @override
    def __init__(
        self, id: int, parenthesis_expression: Node, statement_if_true: Node
    ) -> None:
        super().__init__(id)

        self.parenthesis_expression: Node = parenthesis_expression
        self.statement_if_true: Node = statement_if_true

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `Conditional`.

        The node itself is aligned with `indent`, and its children are padded
        with an additional left space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)

        self.parenthesis_expression.print(indent + 1)
        self.statement_if_true.print(indent + 1)

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of the current `Conditional`, and set this attribute.

        For `Conditional` nodes, certificate the `parenthesis_expression`,
        recursively, and the `Conditional` itself, and then the children
        `statement` nodes -- also recursively.

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

        prime = self.parenthesis_expression.certificate(prime)

        prime = super().certificate(prime)

        return self.statement_if_true.certificate(prime)
