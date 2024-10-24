"""Representation of FUNC_DEF nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.ast_nodes.basic.SEQ import SEQ
from src.ast_nodes.functions.PARAM import PARAM


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
        
        type: str = function_metadata.get("type")
        super().__init__(id, function_name, type)

        self.arguments: list[PARAM] = self._define_vars_from_args(
            arguments=function_metadata.get("arguments")
        )
        self.statements: SEQ = None

    def set_statements(self, statements: SEQ) -> None:
        """
        Set the `statements` attribute.

        Parameters
        ----------
        statements : SEQ
            The statements to be added to object. Must be a `SEQ` -- i.e., the
            root of a subtree with the statements of this function.
        """

        self.statements = statements

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `FUNC_DEF` nodes, obtain the certificates, recursively, starting
        from the `statements` attribute (i.e., a `SEQ` node). The
        `FUNC_DEF` node itself does not have a certificate.

        Returns
        -------
        certificate : list of str
            A list containing the certificate label of this `FUNC_DEF`.
        """

        certificate: list[str] = []

        for argument in self.arguments:
            certificate.extend(argument.get_certificate_label())

        certificate.extend(self.statements.get_certificate_label())

        return certificate

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

        for argument in self.arguments:
            argument.print(indent+1)

        self.statements.print(indent+1)

    @override
    def generate_code(self, register: int) -> tuple[
        int,
        list[dict[str, Union[int, str]]]
    ]:
        """
        Generate the code for this `FUNC_DEF`.

        For this node specialization, generate the code from its `arguments` and
        statements`, recursively. The `FUNC_DEF` node itself does not have an
        associated instruction, nor uses registers.

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
            `instruction`, and node `id`, and `value`.
        """

        code_metadata: list[dict[str, Union[int, str]]] = []

        for argument in self.arguments:
            register, var_def_code = argument.generate_code(
                register=register
            )
            code_metadata.extend(var_def_code)

        register, statements_code = self.statements.generate_code(
            register=register
        )

        code_metadata.extend(statements_code)

        return register, code_metadata

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of this `FUNC_DEF`.

        To achieve this, certificate its `arguments` and `statements`,
        recursively and in order. The `FUNC_DEF` node itself does not have a
        certificate.

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

        for argument in self.arguments:
            prime = argument.certificate(prime)

        return self.statements.certificate(prime)
    
    def _define_vars_from_args(self, arguments: dict[str, dict]) -> list[PARAM]:
        """
        Create `PARAM` nodes to be contain the received arguments.

        Parameters
        ----------
        arguments : dict
            A dict with variable metadata to generate `PARAM` nodes from.

        Returns
        -------
        variables : list[PARAM]
            A list of `PARAM` nodes. Might be empty, if the function does not
            take any parameters.
        """

        variables: list[PARAM] = []

        for argument_name, argument_metadata in arguments.items():
            variable_metadata = {
                "name": argument_name,
                **argument_metadata
            }

            variables.append(
                PARAM(
                    id=None,
                    variable_metadata=variable_metadata
                )
            )

        return variables
    
    def get_function_name(self) -> str:
        """
        Get the name of this function.

        Returns
        -------
        function_name : str
            The name of the function.
        """

        function_name: str = self.value

        return function_name
