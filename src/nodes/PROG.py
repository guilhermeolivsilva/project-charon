"""Representation of PROG nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from .base.node import Node


class PROG(Node):
    """
    Implement the representation of the beginning of a program for the AST.

    This class overrides the constructor and `traverse` methods.

    Parameters
    ----------
    id : int
        The ID of the Node.
    """

    @override
    def __init__(self, id: int) -> None:
        super().__init__(id)

        self.first_statement: Node = None

    def set_first_statement(self, first_statement: Node) -> None:
        """
        Set the first statement of the program.

        Parameters
        ----------
        first_statement : Node
            The node that represents the first statement.        
        """

        self.first_statement = first_statement

    def traverse(self, func: callable, **kwargs) -> None:
        """
        Apply the traversal `func` to the first statement node, and then
        to the `PROG` node itself.

        Parameters
        ----------
        func : callable
            The function to call during the traversal.
        """

        self.first_statement.traverse(func, **kwargs)
        func(self, **kwargs)
