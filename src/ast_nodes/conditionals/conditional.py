"""Representation of conditionals for the Abstract Syntax Tree."""

from typing_extensions import override

from src.ast_nodes.node import Node
from src.utils import SYMBOLS_MAP


class Conditional(Node):
    """
    Implement the representation of conditionals for the AST.

    Parameters
    ----------
    parenthesis_expression : Node
        The node representation of the expression to be evaluated.
    statement_if_true : Node
        The node representation of code to run if the `parenthesis_expression`
        evaluates to `True`.
    """

    @override
    def __init__(self, parenthesis_expression: Node, statement_if_true: Node) -> None:
        super().__init__(uses_register=False)

        self.parenthesis_expression: Node = parenthesis_expression
        self.statement_if_true: Node = statement_if_true

        # This will be set by the `certificate` method
        self.conditional_expression_boundary = None
        self.boundary_certificate = None

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `Conditional` nodes, obtain the certificates, recursively, from the
        `parenthesis_expression` subtree first, then from the `Conditional`
        node itself, and, finally, from the `statement_if_true` subtree.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """

        return [
            self.conditional_expression_boundary,
            *self.parenthesis_expression.get_certificate_label(),
            *super().get_certificate_label(),
            *self.statement_if_true.get_certificate_label(),
            self.boundary_certificate
        ]

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
    def certificate(
        self,
        certificator_env: dict[int, list[int]]
    ) -> dict[int, list[int]]:
        """
        Compute the certificate of the current `Conditional`, and set this attribute.

        For `Conditional` nodes, certificate the `parenthesis_expression`,
        recursively, and the `Conditional` itself, and then the children
        `statement` nodes -- also recursively.

        Parameters
        ----------
        certificator_env : dict[int, list[int]]
            The certificators's environment, that maps variables IDs to
            encodings of their types.

        Returns
        -------
        certificator_env : dict[int, list[int]]
            The updated certificator's environment, with any additional
            information about the variable's types it might have captured.
        """

        # Add the symbol to delimit the condition expression
        _conditional_expression_boundary_symbol = SYMBOLS_MAP["COND"]
        self.conditional_expression_boundary = (
            f"{_conditional_expression_boundary_symbol}"
        )

        certificator_env = self.parenthesis_expression.certificate(certificator_env)
        certificator_env = super().certificate(certificator_env)
        certificator_env = self.statement_if_true.certificate(certificator_env)

        self.boundary_certificate = f"{self.boundary_symbol}"

        return certificator_env
