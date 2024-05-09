"""Representation of SET nodes for the Abstract Syntax Tree."""

from string import ascii_lowercase
from typing import Union
from typing_extensions import override

from .base.node import Node
from .base.operation import Operation


class SET(Operation):
    """
    Implement the representation of a attribution operation for the AST.

    This class overrides the constructor and `traverse` methods.

    Parameters
    ----------
    id : int
        The ID of the Node.
    lhs : Node
        The node representation of the variable to attribute to.
    rhs : Node
        The node representation of the expression to be attributed to `lhs`.
    """

    @override
    def __init__(self, id: int, lhs: Node, rhs: Node) -> None:
        super().__init__(id, lhs=None, rhs=rhs)

        self.value: Union[str, int, None] = lhs.value

        self.instruction: str = "ISTORE"

    @override
    def traverse(self, func: callable, **kwargs) -> None:
        """
        Apply the traversal `func` to the child expression node, and then
        to the `SET` node itself.

        Parameters
        ----------
        func : callable
            The function to call during the traversal.
        """

        self.rhs.traverse(func, **kwargs)
        func(self, **kwargs)

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

        print("  " * indent + str(self))

        self.rhs.print(indent + 1)

    @override
    def generate_code(self) -> list[dict[str, Union[int, str, None]]]:
        """
        Generate the code associated with this `SET`.

        For this node specialization, generate code from the `rhs` first, and
        then from the node itself.

        Returns
        -------
        code_metadata : list of dict
            Return a dictionary of code metadata: the related `instruction`,
            and node `id`, and `value`.
        """

        _this_metadata = {
            "instruction": self.instruction,
            "id": self.id,
            "value": self.value
        }

        code_metadata = [
            *self.rhs.generate_code(),
            _this_metadata
        ]

        return code_metadata
