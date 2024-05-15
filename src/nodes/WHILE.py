"""Representation of WHILE nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from .base.node import Node
from .base.conditional import Conditional


class WHILE(Conditional):
    """
    Implement the representation of a `WHILE` loop for the AST.

    This class simply is an interface for the `Conditional` class, renaming
    the `statement_if_true` to `loop`.

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

        self.symbol: str = "(38)"

    @override
    def generate_code(self) -> list[dict[str, Union[int, str, None]]]:
        """
        Generate the code associated with this `WHILE`.

        For this node specialization, generate code from the
        `parenthesis_expression` first, add a conditional jump to the last
        instruction of the `loop` subtree -- i.e., to jump to if the
        `parenthesis_expression` evaluates to `False`; in other words, to
        skip the conditional code -- and then from the `loop`. After the `loop`
        instructions, add an unconditional jump to the `parenthesis_expression`
        for it to be reevaluated.

        Returns
        -------
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`, and node `id`, and `value`.
        """

        _parenthesis_expression_code = self.parenthesis_expression.generate_code()
        _loop_code = self.statement_if_true.generate_code()

        # Conditional jump to leave the loop if the `parenthesis_expression`
        # evaluates to `False`
        _conditional_jump = {"instruction": "JZ", "id": self.id, "value": None}

        # Dummy instruction (i.e., `EMPTY`) just outside the loop. This is the
        # target of the `_conditional_jump` for it to leave the loop.
        _dummy_instruction_metadata = {
            "instruction": "EMPTY",
            "id": self.id,
            "value": None,
        }

        # Unconditional jump at the end of the `_loop_code` so the
        # `parenthesis_expression` can be reevaluated
        _beginning_of_parenthesis_expression = _parenthesis_expression_code[0]
        _beginning_of_parenthesis_expression_id = _beginning_of_parenthesis_expression[
            "id"
        ]

        _unconditional_jump = {
            "instruction": "JMP",
            "id": _beginning_of_parenthesis_expression_id,
            "value": None,
        }

        return [
            *_parenthesis_expression_code,
            _conditional_jump,
            *_loop_code,
            _unconditional_jump,
            _dummy_instruction_metadata,
        ]

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of the current `WHILE`, and set this attribute.

        For `WHILE` nodes, certificate the `parenthesis_expression` and `loop`
        subtrees first, recursively, and then the `WHILE` node itself.

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

        return super().certificate(prime)
