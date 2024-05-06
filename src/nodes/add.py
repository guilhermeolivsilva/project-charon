"""Representation of ADD nodes for the Abstract Syntax Tree."""

from .base.operation import Operation


class ADD(Operation):
    """
    Implement the representation of an addition for the AST.

    This class is simply an interface for the `Operation` class.

    Parameters
    ----------
    id : int
        The ID of the Node.
    lhs : Node
        The Node representation of the left hand side of the addition.
    rhs : Node
        The Node representation of the right hand side of the addition.
    """
