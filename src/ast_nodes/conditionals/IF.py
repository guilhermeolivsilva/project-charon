"""Representation of IF nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.ast_nodes.conditionals.conditional import Conditional


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

    @override
    def generate_code(self, register: int) -> tuple[
        int,
        list[dict[str, Union[int, str]]]
    ]:
        """
        Generate the code associated with this `IF`.

        For this node specialization, generate code from the
        `parenthesis_expression` first, add a conditional jump to the last
        instruction of the `statement_if_true` subtree -- i.e., to jump to if
        the `parenthesis_expression` evaluates to `False`; in other words, to
        skip the conditional code -- and then from the `statement_if_true`.

        Parameters
        ----------
        register : int
            The number of the register to be used by the code generated by this
            Node.

        Returns
        -------
        register : int
            The number of the next register available.
        if_code : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`, and node `id`, and `value`.
        """

        register, parenthesis_expression_code = self.parenthesis_expression.generate_code(
            register=register
        )
        register, statement_if_true_code = self.statement_if_true.generate_code(
            register=register
        )

        _end_of_conditional_block = statement_if_true_code[-1]
        _end_of_conditional_block_id = _end_of_conditional_block.get("metadata").get("id")

        # The jump target is the amount of instructions in the
        # `statement_if_true` block (add 1 to land right after the last
        # instruction)
        instructions_to_jump = len(statement_if_true_code) + 1
        conditional_jump = {
            "instruction": "JZ",
            "metadata": {
                "instructions_to_jump": instructions_to_jump
            }
        }

        # If `parenthesis_expression` evals to `False`, jump to the instruction
        # with ID `_end_of_conditional_block_id`. If not, execute the
        # `_statement_if_true_code`.
        if_code: list[dict[str, Union[int, str]]] = [
            *parenthesis_expression_code,
            conditional_jump,
            *statement_if_true_code,
        ]

        return register, if_code
