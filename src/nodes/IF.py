"""Representation of IF nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from .base.conditional import Conditional


class IF(Conditional):
    """
    Implement the representation of a conditional for the AST.

    This class overrides the `traverse` method.

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
    def traverse(self, func: callable, **kwargs) -> None:
        """
        Apply the traversal `func` to the `parenthesis_expression` node, to
        the `IF` node itself, and then to the `if_statement` node.

        Parameters
        ----------
        func : callable
            The function to call during the traversal.
        """

        self.parenthesis_expression.traverse(func, **kwargs)
        func(self, **kwargs)
        self.statement_if_true.traverse(func, **kwargs)
