"""Representation of ELEMENT_ACCESS nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.ast_nodes.variables.VAR import VAR
from src.ast_nodes.basic.CST import CST


class ELEMENT_ACCESS(Node):
    """
    Implement the representation of an elemment access node for the AST.

    An element access is used within the context of arrays (indexes), and
    structs (attributes).

    Parameters
    ----------
    id : int
        The ID of the Node.
    variable : str
        The variable whose element is being accessed.
    element : int
        The index of the element being accessed.
    """

    @override
    def __init__(self, id: int, variable: str, element: int) -> None:
        super().__init__(id)

        self.instruction = "ELEMENT_PTR"

        self.variable = VAR(
            id=id + 1,
            pseudonymous=variable
        )
        self.element = CST(
            id=id + 2,
            value=element,
            type="int"
        )

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `ELEMENT_ACCESS` nodes, obtain the certificates, recursively, from
        the `variable` and `element` subtrees first, and then from the
        `ELEMENT_ACCESS` node itself.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """

        certificate_label: list = [
            *self.variable.get_certificate_label(),
            *self.element.get_certificate_label(),
            *super().get_certificate_label()
        ]

        return certificate_label

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `ELEMENT_ACCESS`.

        The node itself is aligned with `indent`, and its children (the
        variable and the element index) are padded with an additional left
        space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)
        self.variable.print(indent=indent + 1)
        self.element.print(indent=indent + 1)

    @override
    def generate_code(self) -> list[dict[str, Union[int, str, None]]]:
        """
        Generate the code associated with this `ELEMENT_ACCESS`.

        For this node specialization, generate code from `variable` and
        `element` children nodes first, respectively, and then from the
        `ELEMENT_ACCESS` itself.

        Returns
        -------
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`, and node `id`, and `value`.
        """

        code_metadata: list[dict] = [
            *self.variable.generate_code(),
            *self.element.generate_code(),
            *super().generate_code()
        ]

        return code_metadata

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of the current `ELEMENT_ACCESS`, and set this attribute.

        For `ELEMENT_ACCESS` nodes, certificate `variable` and `element`
        children first, and then the `ELEMENT_ACCESS` itself.

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

        prime = self.variable.certificate(prime)
        prime = self.element.certificate(prime)

        return super().certificate(prime)
