"""Representation of DO nodes for the Abstract Syntax Tree."""

from typing import Union
from typing_extensions import override

from .base.node import Node
from .base.conditional import Conditional


class DO(Conditional):
    """
    Implement the representation of a `DO` loop for the AST.

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
            "value": None
        }

        return [
            *_loop_code,
            *_parenthesis_expression_code,
            _conditional_jump
        ]
