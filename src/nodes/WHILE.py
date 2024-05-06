"""Representation of WHILE nodes for the Abstract Syntax Tree."""

from .base.loop import Loop


class WHILE(Loop):
    """
    Implement the representation of a `WHILE` loop for the AST.

    This class simply is an interface for the `Loop` class.

    Parameters
    ----------
    id : int
        The ID of the Node.
    parenthesis_expression : Node
        The node representation of the expression to be evaluated.
    loop : Node
        The node representation of code to run if the `parenthesis_expression`
        evaluates to `True`.
    """
