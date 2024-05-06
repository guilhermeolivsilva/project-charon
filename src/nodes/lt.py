"""Representation of LT nodes for the Abstract Syntax Tree."""

from .operation import Operation


class LT(Operation):
    """
    Implement the representation of a "less than" comparison for the AST.

    This class is simply an interface for the `Operation` class.

    Parameters
    ----------
    id : int
        The ID of the Node.
    lhs : Node
        The Node representation of the left hand side of the comparison.
    rhs : Node
        The Node representation of the right hand side of the comparison.
    """

    ...
