"""Representation of IFELSE nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from .base.node import Node


class IFELSE(Node):
    """
    Implement the representation of a conditional for the AST.

    This class overrides the constructor and `traverse` methods.

    Parameters
    ----------
    id : int
        The ID of the Node.
    parenthesis_expression : Node
        The node representation of the expression to be evaluated.
    if_statement : Node
        The node representation of code to run if the `parenthesis_expression`
        evaluates to `True`.
    else_statement : Node
        The node representation of code to run if the `parenthesis_expression`
        evaluates to `False`.
    """

    @override
    def __init__(
        self, id: int,
        parenthesis_expression: Node,
        if_statement: Node,
        else_statement: Node
    ) -> None:
        super().__init__(id)

        self.parenthesis_expression: Node = parenthesis_expression
        self.if_statement = if_statement
        self.else_statement = else_statement

    @override
    def traverse(self, func: callable, **kwargs) -> None:
        """
        Apply the traversal `func` to the `parenthesis_expression` node, to
        the `IF` node itself, to the `if_statement` node, and the to the
        `else_statement` node.

        Parameters
        ----------
        func : callable
            The function to call during the traversal.
        """

        self.parenthesis_expression.traverse(func, **kwargs)
        func(self, **kwargs)
        self.if_statement.traverse(func, **kwargs)
        self.else_statement.traverse(func, **kwargs)
