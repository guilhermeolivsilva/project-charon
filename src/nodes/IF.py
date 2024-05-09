"""Representation of IF nodes for the Abstract Syntax Tree."""

from typing import Union
from typing_extensions import override

from .base.conditional import Conditional


class IF(Conditional):
    """
    Implement the representation of a conditional for the AST.

    This class overrides the `traverse` method.

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
    def traverse(self, func: callable, **kwargs) -> None:
        """
        Apply the traversal `func` to the `parenthesis_expression` node, to
        the `IF` node itself, and then to the `if_statement` node.

        Parameters
        ----------
        func : callable
            The function to call during the traversal.
        """

        self.parenthesis_expression.traverse(func, **kwargs)
        func(self, **kwargs)
        self.statement_if_true.traverse(func, **kwargs)

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `Operation`.

        The node itself is aligned with `indent`, and its children are padded
        with an additional left space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)

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

        _last_statement_if_true_instruction = _statement_if_true_code[-1]
        _id_to_jump_if_eval_to_false = _last_statement_if_true_instruction["id"]

        _metadata_if_eval_to_false = {
            "instruction": "JZ",
            "id": _id_to_jump_if_eval_to_false,
            "value": None
        }

        return [
            *_parenthesis_expression_code,
            _metadata_if_eval_to_false,
            *_statement_if_true_code
        ]
