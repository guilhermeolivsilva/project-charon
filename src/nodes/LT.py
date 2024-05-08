"""Representation of LT nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from .base.operation import Operation


class LT(Operation):
    """
    Implement the representation of a "less than" comparison for the AST.

    This class simply is an interface for the `Operation` class.

    Parameters
    ----------
    id : int
        The ID of the Node.
    lhs : Node
        The Node representation of the left hand side of the comparison.
    rhs : Node
        The Node representation of the right hand side of the comparison.
    """

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `Operation`.

        The node itself is aligned with `indent`, and its children are padded
        with an additional left space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)
