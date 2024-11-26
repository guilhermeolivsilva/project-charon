"""Representation of DO nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.ast_nodes.conditionals.conditional import Conditional


class DO(Conditional):
    """
    Implement the representation of a `DO` loop for the AST.

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
            *self.statement_if_true.get_certificate_label(),
            *self.parenthesis_expression.get_certificate_label(),
            self.certificate_label,
        ]

    @override
    def generate_code(self, register: int) -> tuple[
        int,
        list[dict[str, Union[int, str]]]
    ]:
        """
        Generate the code associated with this `DO`.

        For this node specialization, generate code from the `loop` first,
        then from the `parenthesis_expression`, and add a conditional jump
        to the beginning of the loop for it to run again, if the
        `parenthesis_expression` evaluates to `True`.

        Parameters
        ----------
        register : int
            The number of the register to be used by the code generated by this
            Node.

        Returns
        -------
        register : int
            The number of the next register available.
        do_code : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction` and `value`.
        """

        register, loop_code = self.statement_if_true.generate_code(
            register=register
        )
        register, parenthesis_expression_code = self.parenthesis_expression.generate_code(
            register=register
        )
        conditional_register: int = register - 1

        # The jump target is the amount of instructions to be jumped in order
        # to reenter the loop. It is negative as it will jump to a previous
        # instruction, rather than forward
        instructions_to_jump = 0 - (len(loop_code) + len(parenthesis_expression_code))
        conditional_jump = [
            {
                "instruction": "NOT",
                "metadata": {
                    "value": conditional_register,
                    "register": register
                }
            },
            {
                "instruction": "JZ",
                "metadata": {
                    "conditional_register": register,
                    "jump_size": instructions_to_jump
                }
            }
        ]
        register += 1

        do_code: list[dict[str, Union[int, str]]] = [
            *loop_code,
            *parenthesis_expression_code,
            *conditional_jump
        ]

        return register, do_code

    @override
    def certificate(self) -> None:
        """
        Compute the certificate of the current `DO`, and set this attribute.

        For `DO` nodes, certificate the `parenthesis_expression` and `loop`
        subtrees first, recursively, and then the `DO` node itself.
        """

        # The `statement_if_true` is the actual internal name of the `loop`
        # subtree.
        self.statement_if_true.certificate()
        self.parenthesis_expression.certificate()

        self.certificate_label = f"({self.symbol})"
