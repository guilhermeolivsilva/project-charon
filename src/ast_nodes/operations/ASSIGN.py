"""Representation of ASSIGN nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.utils import next_prime

from src.ast_nodes.node import Node
from src.ast_nodes.operations.operation import Operation


class ASSIGN(Operation):
    """
    Implement the representation of a attribution operation for the AST.

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
        super().__init__(id, lhs=lhs, rhs=rhs)

        self.instruction: str = "STORE"

    @override
    def generate_code(self) -> list[dict[str, Union[int, str, None]]]:
        """
        Generate the code associated with this `ASSIGN`.

        For this node specialization, generate code from the `lhs` and `rhs`
        subtrees first, and then from the node itself.

        Returns
        -------
        code_metadata : list of dict
            Return a dictionary of code metadata: the related `instruction`,
            and node `id`, and `value`.
        """

        _this_metadata = {
            "instruction": self.instruction,
            "id": self.id,
            "value": self.value,
        }

        code_metadata = [
            *self.lhs.generate_code(),
            *self.rhs.generate_code(),
            _this_metadata
        ]

        return code_metadata

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of the current `ASSIGN`, and set this attribute.

        For `ASSIGN` nodes, certificate the `lhs` and `rhs` subtrees first.
        Then, certificate the `ASSIGN` itself with `symbol ^ variable
        declaration relative position`.

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

        prime = self.lhs.certificate(prime)
        prime = self.rhs.certificate(prime)

        self.set_certificate_label(certificate_label=f"{prime}^{self.symbol}")

        return next_prime(prime)
