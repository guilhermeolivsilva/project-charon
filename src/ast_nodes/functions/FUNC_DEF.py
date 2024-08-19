"""Representation of FUNC_DEF nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.ast_nodes.basic.SEQ import SEQ


class FUNC_DEF(Node):
    """
    Implement the representation of a `FUNC_DEF` node for the AST.

    A `FUNC_DEF` is an abstraction of a function definition: it tracks its
    return type, parameters (and its types), and statements.
    
    The node itself only has children to help structuring the function
    definition, but doesn't have any semantics itself, `instruction`, or has a
    certificate.

    Parameters
    ----------
    function_name : str
        The name of the function.
    variable_metadata : dict
        Dictionary of variable metadata exported by the Lexer.
    """

    @override
    def __init__(
        self,
        id: int,
        function_name: str,
        function_metadata: dict[str, Union[str, dict]]
    ) -> None:
        super().__init__(function_name)

        self.pseudonymous: str = function_metadata.get("pseudonymous")
        self.type: str = function_metadata.get("type")
        self.arguments: dict = function_metadata.get("arguments")
        self.statements = SEQ(id=id)

    def add_statement(self, statement: Node) -> None:
        """
        Add a statement Node to the `self.SEQ.children` list.

        Parameters
        ----------
        statement : Node
            The statement to be added to the list.
        """

        self.statements.add_child(statement)

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `FUNC_DEF` nodes, obtain the certificates, recursively, starting
        from the `statements` attribute (i.e., a `SEQ` node). The
        `FUNC_DEF` node itself does not have a certificate.

        Returns
        -------
        : list of str
            A list containing the certificate label of this `FUNC_DEF`.
        """

        return self.statements.get_certificate_label()

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `FUNC_DEF`.

        The node itself is aligned with `indent`, and its children are padded
        with an additional left space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)

        self.statements.print(indent+1)

    @override
    def generate_code(self) -> list[dict[str, Union[int, str, None]]]:
        """
        Generate the code for this `FUNC_DEF`.

        For this node specialization, generate the code from its `statements`,
        recursively. The `FUNC_DEF` node itself does not have an associated
        instruction.

        Returns
        -------
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`, and node `id`, and `value`.
        """

        return self.statements.generate_code()

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of this `FUNC_DEF`.

        To achieve this, certificate its `statements`, recursively and in order.
        The `FUNC_DEF` node itself does not have a certificate.

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

        return self.statements.certificate(prime)
