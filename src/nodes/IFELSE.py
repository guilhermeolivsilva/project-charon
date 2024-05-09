"""Representation of IFELSE nodes for the Abstract Syntax Tree."""

from typing import Union
from typing_extensions import override

from .base.conditional import Conditional
from .base.node import Node


class IFELSE(Conditional):
    """
    Implement the representation of a conditional for the AST.

    This class overrides the constructor and `traverse` methods.

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

    @override
    def traverse(self, func: callable, **kwargs) -> None:
        """
        Apply the traversal `func` to the `parenthesis_expression` node, to
        the `IF` node itself, to the `statement_if_true` node, and the to the
        `statement_if_false` node.

        Parameters
        ----------
        func : callable
            The function to call during the traversal.
        """

        self.parenthesis_expression.traverse(func, **kwargs)
        func(self, **kwargs)
        self.statement_if_true.traverse(func, **kwargs)
        self.statement_if_false.traverse(func, **kwargs)

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

        _first_instruction_of_else_block = _statement_if_false_code[0]
        _first_instruction_of_else_block_id = _first_instruction_of_else_block["id"]
        _conditional_jump = {
            "instruction": "JZ",
            "id": _first_instruction_of_else_block_id,
            "value": None
        }

        _last_instruction_of_else_block = _statement_if_false_code[-1]
        _last_instruction_of_else_block_id = _last_instruction_of_else_block["id"]
        _unconditional_jump = {
            "instruction": "JMP",
            "id": _last_instruction_of_else_block_id,
            "value": None
        }

        # If `parenthesis_expression` evals to `False`, jump to the instruction
        # with ID `_first_instruction_of_else_block_id`. If not, execute
        # the `_statement_if_true_code`. However, add an unconditional jump
        # right after the `_statement_if_true_code` in order to skip the
        # `_statemente_if_false_code`.
        return [
            *_parenthesis_expression_code,
            _conditional_jump,
            *_statement_if_true_code,
            _unconditional_jump,
            *_statement_if_false_code
        ]
