"""Base class for AST Nodes classes (e.g., VAR, CST etc.)."""

from typing import Union

from src.utils import next_prime


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

        # Each `Node` specialization must set its own `instruction` and
        # `symbol`.
        self.instruction: str = None
        self.symbol: str = None

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

    def get_certificate_label(self) -> str:
        """
        Get the contents of `certificate_label`.

        Returns
        -------
        : str
            The certificate label of the `Node`.
        """

        return self.certificate_label

    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of `self`.

        The printed text is indented according with the optional `indent`
        paremeter.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        print("  " * indent + str(self))

    def generate_code(self) -> list[dict[str, Union[int, str, None]]]:
        """
        Generate the code associated with this `Node`.

        The generated code consists of a dictionary containing the relevant
        `Node` data for the code to run -- namely, the `instruction`, the `id`,
        and the `value`.

        Notice that some `Nodes` may rewrite this method in order to deal
        with special attributes -- such as the `Operation` nodes, that must
        handle its children nodes.

        Returns
        -------
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`, and node `id`, and `value`.

        Notes
        -----
        This method returns a `list` rather than only the `code_metadata` in
        order to standardize the return type as some subclasses might have to
        generate code using not only the node itself, but its children, too.
        """

        code_metadata = {
            "instruction": self.instruction,
            "id": self.id,
            "value": self.value
        }

        return [code_metadata]
    
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of the current `Node`, and set this attribute.

        This method returns an integer, that corresponds to a prime number that
        comes after the given `prime` (immediately after or not) in
        order to allow recursively certificate the nodes of a subtree of the
        AST.

        Parameters
        ----------
        prime : int
            A prime number that represents the relative position of the `Node`
            in the AST.

        Returns
        -------
        : int
            A prime number that comes after the given `prime`.
        """

        self.set_certificate_label(
            certificate_label=f"{prime}^{self.symbol}"
        )

        return next_prime(prime)
