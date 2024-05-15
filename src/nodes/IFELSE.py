"""Representation of IFELSE nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from .base.conditional import Conditional
from .base.node import Node


class IFELSE(Conditional):
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
    statement_if_false : Node
        The node representation of code to run if the `parenthesis_expression`
        evaluates to `False`.
    """

    @override
    def __init__(
        self,
        id: int,
        parenthesis_expression: Node,
        statement_if_true: Node,
        statement_if_false: Node,
    ) -> None:
        super().__init__(id, parenthesis_expression, statement_if_true)

        self.statement_if_false: Node = statement_if_false
        self.symbol: str = "(37)"

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `IFELSE` nodes, first call the `Conditional.get_certificate_label`
        method, and compose it with the `certificate_label` obtained recursively
        from the `statement_if_false` subtree.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """

        return [
            *super().get_certificate_label(),
            *self.statement_if_false.get_certificate_label(),
        ]

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

        self.statement_if_false.print(indent + 1)

    @override
    def generate_code(self) -> list[dict[str, Union[int, str, None]]]:
        """
        Generate the code associated with this `IFELSE`.

        For this node specialization, generate code from the
        `parenthesis_expression` first, add a conditional jump to the first
        instruction of the `statement_if_false` subtree -- i.e., to jump to if
        the `parenthesis_expression` evaluates to `False` --, then generate
        code from the `statement_if_true`, add an unconditional jump to the
        last instruction of teh `statement_if_false` subtree, and then finally
        generate code from `statement_if_false`.

        Returns
        -------
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`, and node `id`, and `value`.
        """

        _parenthesis_expression_code = self.parenthesis_expression.generate_code()
        _statement_if_true_code = self.statement_if_true.generate_code()
        _statement_if_false_code = self.statement_if_false.generate_code()

        _beginning_of_else_block = _statement_if_false_code[0]
        _beginning_of_else_block_id = _beginning_of_else_block["id"]
        _conditional_jump = {
            "instruction": "JZ",
            "id": _beginning_of_else_block_id,
            "value": None,
        }

        _end_of_else_block = _statement_if_false_code[-1]
        _end_of_else_block_id = _end_of_else_block["id"]
        _unconditional_jump = {
            "instruction": "JMP",
            "id": _end_of_else_block_id,
            "value": None,
        }

        # If `parenthesis_expression` evals to `False`, jump to the instruction
        # with ID `_beginning_of_else_block_id`. If not, execute the
        # `_statement_if_true_code`. However, add an unconditional jump right
        # after the `_statement_if_true_code` in order to skip the
        # `_statement_if_false_code`.
        return [
            *_parenthesis_expression_code,
            _conditional_jump,
            *_statement_if_true_code,
            _unconditional_jump,
            *_statement_if_false_code,
        ]

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of the current `IFELSE`, and set this attribute.

        For `IFELSE` nodes, certificate the `parenthesis_expression`,
        recursively, and the `IFELSE` itself, and then the children
        `statement` nodes -- also recursively -- in order (i.e., the
        `statement_if_true` and then the `statement_if_false` subtrees).

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

        prime = super().certificate(prime)

        return self.statement_if_false.certificate(prime)
