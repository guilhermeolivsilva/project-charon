"""Representation of IFELSE nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from .base.conditional import Conditional
from .base.node import Node


class IFELSE(Conditional):
    """
    Implement the representation of a conditional for the AST.

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
    statement_if_false : Node
        The node representation of code to run if the `parenthesis_expression`
        evaluates to `False`.
    """

    @override
    def __init__(
        self,
        id: int,
        parenthesis_expression: Node,
        statement_if_true: Node,
        statement_if_false: Node,
    ) -> None:
        super().__init__(id, parenthesis_expression, statement_if_true)

        self.statement_if_false: Node = statement_if_false

    @override
    def traverse(self, func: callable, **kwargs) -> None:
        """
        Apply the traversal `func` to the `parenthesis_expression` node, to
        the `IF` node itself, to the `statement_if_true` node, and the to the
        `statement_if_false` node.

        Parameters
        ----------
        func : callable
            The function to call during the traversal.
        """

        self.parenthesis_expression.traverse(func, **kwargs)
        func(self, **kwargs)
        self.statement_if_true.traverse(func, **kwargs)
        self.statement_if_false.traverse(func, **kwargs)

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

        self.statement_if_false.print(indent + 1)
