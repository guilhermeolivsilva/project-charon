"""Representation of NOT nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.ast_nodes.certificate_mapping import TYPE_SYMBOLS_MAP


class NOT(Node):
    """
    Implement the representation of a negation (logical not) for the AST.

    Parameters
    ----------
    expression : Node
        The Node representation of the term to be negated.
    """

    @override
    def __init__(self, expression: Node, **kwargs) -> None:
        super().__init__()

        self.expression: Node = expression
        self.symbol: str = self._compute_symbol()
        self.instruction: str = "NOT"
        self.type: str = "int"

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `NOT` nodes, obtain the certificates, recursively, from the
        `expression` subtree first, and then from the `NOT` node itself.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `NOT` node.
        """

        return [
            *self.expression.get_certificate_label(),
            self.certificate_label
        ]

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `NOT` node.

        The node itself is aligned with `indent`, and its children are padded
        with an additional left space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)

        self.expression.print(indent + 1)

    @override
    def generate_code(self, register: int) -> tuple[
        int,
        list[dict[str, Union[int, str, None]]]
    ]:
        """
        Generate the code associated with this `Operation`.

        For this node specialization, generate code from the left and right
        hand sides nodes first, and then from the node itself.

        Parameters
        ----------
        register : int
            The number of the register to be used by the code generated by this
            Node.

        Returns
        -------
        register : int
            The number of the next register available.
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`and `value`.
        """

        code_metadata: list[dict[str, Union[int, str, None]]] = []

        register, expression_code = self.expression.generate_code(register=register)
        code_metadata.extend(expression_code)

        expression_register = register - 1

        this_code = {
            "instruction": self.instruction,
            "metadata": {

                "register": register,
                "value": expression_register
            }
        }
        register += 1

        code_metadata.append(this_code)

        return register, code_metadata

    def _compute_symbol(self) -> str:
        """
        Compute the symbol of this `Operation`.

        The symbol is composed by the basic symbol of the operation itself,
        plus the types of its left and right hand sides.

        Returns
        -------
        : str
            The symbol computed with left and right hand sides types.
        """

        expression_type = self.expression.get_type()
        expression_type_symbol = TYPE_SYMBOLS_MAP.get(expression_type).get("type_symbol")

        return f"{self.symbol}^{expression_type_symbol}"
