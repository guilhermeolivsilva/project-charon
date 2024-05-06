"""Representation of DO nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from .base.node import Node
from .base.conditional import Conditional


class DO(Conditional):
    """
    Implement the representation of a `DO` loop for the AST.

    This class simply is an interface for the `Conditional` class, renaming
    the `statement_if_true` to `loop`.

    Parameters
    ----------
    id : int
        The ID of the Node.
    parenthesis_expression : Node
        The node representation of the expression to be evaluated.
    loop : Node
        The node representation of code to run while the
        `parenthesis_expression` evaluates to `True`.
    """

    @override
    def __init__(self, id: int, parenthesis_expression: Node, loop: Node) -> None:
        super().__init__(id, parenthesis_expression, loop)
