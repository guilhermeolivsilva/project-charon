"""Base class for AST Nodes classes (e.g., VAR, CST etc.)."""

from abc import abstractmethod
from typing import Union


class Node:
    """
    Implement a Node for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    value : int or None, optional (default = None)
        The value the Node holds, if any. Defaults to None.
    """

    def __init__(self, id: int, value: Union[int, str, None] = None) -> None:
        self.id: int = id
        self.value: Union[int, str, None] = value
        self.certificate_label: str = None

    def __eq__(self, other: "Node") -> bool:
        """
        Implement the equality comparison between Nodes.

        Parameters
        ----------
        other : Node
            The right hand side Node of the comparison.

        Returns
        -------
        is_equal : bool
            `True` if all the attributes are equal, `False` otherwise.
        """

        is_equal = (
            self.id == other.id
            and self.value == other.value
            and type(self) is type(other)
        )

        return is_equal
    
    def __str__(self) -> str:
        """
        Implement a string representation of a Node object.

        This method is internally invoked when using `print(node_obj)`.

        Returns
        -------
        _str : str
            The string representation of a Node object.
        """
        _str = f"ID: {self.id}, Value: {self.value}, Kind: {type(self).__name__}"

        if self.certificate_label is not None:
            _str += f", Certificate Label: {self.certificate_label}"

        return _str
    
    def set_certificate_label(self, certificate_label: str) -> None:
        """
        Set the `certificate_label` of the Node.

        Parameters
        ----------
        certificate_label : str
            The new `certificate_label` to set.
        """

        self.certificate_label = certificate_label

    def traverse(self, func: callable, **kwargs) -> None:
        """
        Traverse the node and apply a `func` to its children.

        This implementation should only be used for atomic nodes (i.e.,
        `CST`, `VAR` and `EMPTY`). Other nodes should implement their own
        traversal methods, as there are children to handle.

        Parameters
        ----------
        func : callable
            The function to call during the traversal.
        """

        func(self, **kwargs)
