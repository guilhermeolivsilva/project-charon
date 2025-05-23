"""Representation of WHILE nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.ast_nodes.conditionals.conditional import Conditional
from src.utils import SYMBOLS_MAP


class WHILE(Conditional):
    """
    Implement the representation of a `WHILE` loop for the AST.

    This class simply is an interface for the `Conditional` class, renaming
    the `statement_if_true` to `loop`.

    Parameters
    ----------
    parenthesis_expression : Node
        The node representation of the expression to be evaluated.
    loop : Node
        The node representation of code to run while the
        `parenthesis_expression` evaluates to `True`.
    """

    @override
    def __init__(self, parenthesis_expression: Node, loop: Node) -> None:
        super().__init__(parenthesis_expression, loop)

        self.boundary_symbol = SYMBOLS_MAP["WHILE_END"]

    @override
    def generate_code(
        self, register: int, environment: dict[str, dict[int, str]]
    ) -> tuple[
        list[dict[str, Union[int, str, float]]],
        int,
        dict[int, str]
    ]:
        """
        Generate the code associated with this `WHILE`.

        For this node specialization, generate code from the
        `parenthesis_expression` first, add a conditional jump to the last
        instruction of the `loop` subtree -- i.e., to jump to if the
        `parenthesis_expression` evaluates to `False`; in other words, to
        skip the conditional code -- and then from the `loop`. After the `loop`
        instructions, add an unconditional jump to the `parenthesis_expression`
        for it to be reevaluated.

        Parameters
        ----------
        register : int
            The number of the register to be used by the code generated by this
            Node.
        environment : dict[int, str]
            The compiler's environment, that maps variables IDs to memory
            addresses and function IDs to instructions indices.

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
            loop_code,
            register,
            environment
        ) = self.statement_if_true.generate_code(
            register=register,
            environment=environment
        )

        # Conditional jump to leave the loop if the `parenthesis_expression`
        # evaluates to `False` (add 2 to land right after the unconditional
        # jump added later on)
        instructions_to_jump_over_loop = len(loop_code) + 2
        conditional_jump = {
            "instruction": "JZ",
            "metadata": {
                "conditional_register": conditional_register,
                "jump_size": instructions_to_jump_over_loop,
            },
        }

        # Unconditional jump to go back to the `parenthesis_expression`
        # evaluation
        instructions_to_jump_back_to_expression = 0 - (
            len(parenthesis_expression_code) + len(loop_code) + 1
        )
        unconditional_jump = {
            "instruction": "JZ",
            "metadata": {
                "conditional_register": "zero",
                "jump_size": instructions_to_jump_back_to_expression,
            },
        }

        while_code: list[dict[str, Union[int, str]]] = [
            *parenthesis_expression_code,
            conditional_jump,
            *loop_code,
            unconditional_jump,
        ]

        return while_code, register, environment
