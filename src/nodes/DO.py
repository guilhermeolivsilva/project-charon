"""Representation of DO nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.utils import next_prime

from .base.node import Node
from .base.conditional import Conditional


class DO(Conditional):
    """
    Implement the representation of a `DO` loop for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    parenthesis_expression : Node
        The node representation of the expression to be evaluated.
    loop : Node
        The node representation of code to run while the
        `parenthesis_expression` evaluates to `True`.
    """

    @override
    def __init__(self, id: int, parenthesis_expression: Node, loop: Node) -> None:
        super().__init__(id, parenthesis_expression, loop)

        self.symbol: str = "(39)"

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `WHILE` nodes, first obtain the `certificate_label` from the
        `parenthesis_expression` and loop (`statement_if_true`) subtrees,
        recursively, and then from the `WHILE` node itself.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """
        
        return [
            *self.parenthesis_expression.get_certificate_label(),
            *self.statement_if_true.get_certificate_label(),
            self.certificate_label
        ]

    @override
    def generate_code(self) -> list[dict[str, Union[int, str, None]]]:
        """
        Generate the code associated with this `DO`.

        For this node specialization, generate code from the `loop` first,
        then from the `parenthesis_expression`, and add a conditional jump
        to the beginning of the loop for it to run again, if the
        `parenthesis_expression` evaluates to `True`.

        Returns
        -------
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`, and node `id`, and `value`.
        """

        _loop_code = self.statement_if_true.generate_code()
        _parenthesis_expression_code = self.parenthesis_expression.generate_code()

        # Conditional jump to reenter the loop if the `parenthesis_expression`
        # evaluates to `True`
        _beginning_of_loop = _loop_code[0]
        _beginning_of_loop_id = _beginning_of_loop["id"]
        _conditional_jump = {
            "instruction": "JNZ",
            "id": _beginning_of_loop_id,
            "value": None,
        }

        return [*_loop_code, *_parenthesis_expression_code, _conditional_jump]

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of the current `DO`, and set this attribute.

        For `DO` nodes, certificate the `parenthesis_expression` and `loop`
        subtrees first, recursively, and then the `DO` node itself.

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

        prime = self.parenthesis_expression.certificate(prime)

        # The `statement_if_true` is the actual internal name of the `loop`
        # subtree.
        prime = self.statement_if_true.certificate(prime)

        self.set_certificate_label(certificate_label=f"{prime}^{self.symbol}")

        return next_prime(prime)
