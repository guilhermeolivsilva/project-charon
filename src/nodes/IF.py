"""Representation of IF nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.nodes.base.node import Node

from .base.conditional import Conditional


class IF(Conditional):
    """
    Implement the representation of a conditional for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    parenthesis_expression : Node
        The node representation of the expression to be evaluated.
    statement_if_true : Node
        The node representation of code to run if the `parenthesis_expression`
        evaluates to `True`.
    """

    @override
    def __init__(
        self, id: int, parenthesis_expression: Node, statement_if_true: Node
    ) -> None:
        super().__init__(id, parenthesis_expression, statement_if_true)

        self.symbol: str = "(36)"

    @override
    def generate_code(self) -> list[dict[str, Union[int, str, None]]]:
        """
        Generate the code associated with this `IF`.

        For this node specialization, generate code from the
        `parenthesis_expression` first, add a conditional jump to the last
        instruction of the `statement_if_true` subtree -- i.e., to jump to if
        the `parenthesis_expression` evaluates to `False`; in other words, to
        skip the conditional code -- and then from the `statement_if_true`.

        Returns
        -------
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`, and node `id`, and `value`.
        """

        _parenthesis_expression_code = self.parenthesis_expression.generate_code()
        _statement_if_true_code = self.statement_if_true.generate_code()

        _end_of_conditional_block = _statement_if_true_code[-1]
        _end_of_conditional_block_id = _end_of_conditional_block["id"]

        _conditional_jump = {
            "instruction": "JZ",
            "id": _end_of_conditional_block_id,
            "value": None,
        }

        # If `parenthesis_expression` evals to `False`, jump to the instruction
        # with ID `_end_of_conditional_block_id`. If not, execute the
        # `_statement_if_true_code`.
        return [
            *_parenthesis_expression_code,
            _conditional_jump,
            *_statement_if_true_code,
        ]
