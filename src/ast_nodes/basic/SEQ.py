"""Representation of SEQ nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node


class SEQ(Node):
    """
    Implement the representation of a sequence of statements for the AST.

    The node doesn't have any semantics itself, `instruction`, or has a
    certificate. Its only purpose is to help structuring the AST.
    """

    @override
    def __init__(self, **kwargs) -> None:
        super().__init__(uses_register=False)

        self.children: list[Node] = []

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

        For `SEQ` nodes, obtain the certificate from the `children` subtrees,
        recursively. The `SEQ` node itself does not have a certificate.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """

        certificate_label: list[str] = []

        for child in self.children:
            certificate_label.extend(child.get_certificate_label())

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
    def generate_code(self, register: int) -> tuple[
        int,
        list[dict[str, Union[int, str, None]]]
    ]:
        """
        Generate the code associated with this `SEQ`.

        For this node specialization, return a list with the children's code,
        generated in the same order as they appear in the `children` attribute.
        The `SEQ` node itself does not generate code, for it has no associated
        `instruction`.

        Returns
        -------
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction` and `value`.
        """

        code_metadata: list[dict[str, Union[int, str, None]]] = []

        for child in self.children:
            register, child_code = child.generate_code(register=register)
            code_metadata.extend(child_code)

        return register, code_metadata

    def certificate(self) -> None:
        """
        Compute the certificate of the current `SEQ`, and set this attribute.

        For `SEQ` nodes, certificate the child nodes in the same order as they
        appear in the `children` list. The `SEQ` node itself is not certified.
        """

        for child in self.children:
            child.certificate()
