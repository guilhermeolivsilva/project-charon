"""Representation of conditionals for the Abstract Syntax Tree."""

from typing_extensions import override

from .node import Node


class Conditional(Node):
    """
    Implement the representation of conditionals for the AST.

    This class overrides the constructor and `traverse` methods.

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
    def traverse(self, func: callable, **kwargs) -> None:
        """
        Apply the traversal `func` to the `parenthesis_expression` node, to
        the `statement_if_true` node, and then to the parent node itself.

        Parameters
        ----------
        func : callable
            The function to call during the traversal.
        """

        self.parenthesis_expression.traverse(func, **kwargs)
        self.statement_if_true.traverse(func, **kwargs)
        func(self, **kwargs)
