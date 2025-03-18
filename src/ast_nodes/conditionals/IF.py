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
    parenthesis_expression : Node
        The node representation of the expression to be evaluated.
    statement_if_true : Node
        The node representation of code to run if the `parenthesis_expression`
        evaluates to `True`.
    """

    @override
    def __init__(self, parenthesis_expression: Node, statement_if_true: Node) -> None:
        super().__init__(parenthesis_expression, statement_if_true)

    @override
    def generate_code(
        self, register: int, environment: dict[int, str]
    ) -> tuple[
        list[dict[str, Union[int, str, float]]],
        int,
        dict[int, str]
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
        environment : dict[int, str]
            The compiler's environment, that maps variables IDs to memory
            addresses.

        Returns
        -------
        code : list of dict
            Return a list of dictionaries containing code metadata: the register
            to be used, the related `instruction` and its metadata.
        register : int
            The number of the next register available.
        environment : dict[int, str]
            The updated {var_id: address} environment mapping.
        """

        (
            parenthesis_expression_code,
            register,
            environment
        ) = self.parenthesis_expression.generate_code(
            register=register,
            environment=environment
        )
        conditional_register: int = register - 1

        (
            statement_if_true_code,
            register,
            environment
        ) = self.statement_if_true.generate_code(
            register=register,
            environment=environment
        )

        # The jump target is the amount of instructions in the
        # `statement_if_true` block (add 1 to land right after the last
        # instruction)
        instructions_to_jump = len(statement_if_true_code) + 1
        conditional_jump = {
            "instruction": "JZ",
            "metadata": {
                "conditional_register": conditional_register,
                "jump_size": instructions_to_jump,
            },
        }

        # If `parenthesis_expression` evals to `False`, jump a number of
        # `instructions_to_jump`. If not, execute the `_statement_if_true_code`.
        if_code: list[dict[str, Union[int, str]]] = [
            *parenthesis_expression_code,
            conditional_jump,
            *statement_if_true_code,
        ]

        return if_code, register, environment
