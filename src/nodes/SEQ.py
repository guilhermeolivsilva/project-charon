"""Representation of SEQ nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from .base.node import Node


class SEQ(Node):
    """
    Implement the representation of a sequence of statements for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    """

    @override
    def __init__(self, id: int) -> None:
        super().__init__(id)

        self.children: list[Node] = []
        self.symbol: str = "(27)"

    def add_child(self, child: Node) -> None:
        """
        Add a child Node to the `self.children` list.

        Parameters
        ----------
        child : Node
            The child to be added to the list.
        """

        self.children.append(child)

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `SEQ` nodes, obtain the certificate from the `SEQ` node itself
        first, and then from the `children` subtrees, recursively.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """
        
        certificate_label: list[str] = super().get_certificate_label()

        for child in self.children:
            certificate_label.append(*child.get_certificate_label())

        return certificate_label

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

        super().print(indent)

        for child in self.children:
            child.print(indent + 1)

    @override
    def generate_code(self) -> list[dict[str, Union[int, str, None]]]:
        """
        Generate the code associated with this `SEQ`.

        For this node specialization, return a dummy instruction and the code
        regarding the `children`.

        Returns
        -------
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`, and node `id`, and `value`.
        """

        _dummy_instruction = {"instruction": "EMPTY", "id": self.id, "value": None}

        # Flatten the code of the children in a single, one dimensional list of
        # code metadata (dicts), as each child.generate_code call returns a
        # list of dicts.
        _children_code = [
            code_metadata
            for child in self.children
            for code_metadata in child.generate_code()
        ]

        return [_dummy_instruction, *_children_code]

    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of the current `SEQ`, and set this attribute.

        For `SEQ` nodes, certificate the `SEQ` node itself first, and then its
        children in the same order as they appear in the `children` list.

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

        prime = super().certificate(prime)

        for child in self.children:
            prime = child.certificate(prime)

        return prime
