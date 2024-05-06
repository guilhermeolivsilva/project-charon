"""Representation of SUB nodes for the Abstract Syntax Tree."""

from .base.operation import Operation


class SUB(Operation):
    """
    Implement the representation of a subtraction for the AST.

    This class is simply an interface for the `Operation` class.

    Parameters
    ----------
    id : int
        The ID of the Node.
    lhs : Node
        The Node representation of the left hand side of the subtraction.
    rhs : Node
        The Node representation of the right hand side of the subtraction.
    """
