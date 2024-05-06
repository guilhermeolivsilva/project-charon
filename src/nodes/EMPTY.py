"""Representation of EMPTY nodes for the Abstract Syntax Tree."""

from .base.node import Node


class EMPTY(Node):
    """
    Implement the representation of an `EMPTY` node for the AST.

    This class does not need to override any methods or properties of the
    base class.

    Parameters
    ----------
    id : int
        The ID of the Node.
    """
