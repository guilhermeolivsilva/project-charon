"""Representation of FUNC_CALL nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.basic.CST import CST
from src.ast_nodes.functions.ARG import ARG
from src.ast_nodes.node import Node
from src.ast_nodes.variables.VAR import VAR


class FUNC_CALL(Node):
    """
    Implement the representation of a function call for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    function_call_metadata : dict
        Dictionary of function call metadata exported by the Lexer.
    """

    @override
    def __init__(self, id: int, function_call_metadata: dict) -> None:
        function_id: int = function_call_metadata["called_function_metadata"]["relative_position"]
        super().__init__(id, function_id)

        _function_type: str = function_call_metadata["called_function_metadata"]["type"]

        self.function_call_metadata: dict = function_call_metadata
        self.arguments: list[ARG] = self._build_children_nodes()
        self.type: str = _function_type

        _prime: int = self.function_call_metadata["called_function_metadata"]["prime"]
        self.symbol: str = f"({self.symbol})^({_prime})"

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `FUNC_CALL` nodes, obtain the certificates, recursively, from each
        `argument` subtree first, and then from the `FUNC_CALL` node itself.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """

        certificate_label: list = []

        for argument in self.arguments:
            certificate_label.extend(argument.get_certificate_label())

        certificate_label.append(*super().get_certificate_label())

        return certificate_label

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `FUNC_CALL`.

        The node itself is aligned with `indent`, and its children are padded
        with an additional left space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)

        for argument in self.arguments:
            argument.print(indent=indent + 1)

    @override
    def generate_code(self, register: int) -> tuple[
        int,
        list[dict[str, Union[int, str, None]]]
    ]:
        """
        Generate the code associated with this `FUNC_CALL`.

        For this node specialization, generate code from `argument` children
        nodes first, and then from the `FUNC_CALL` itself.

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

        code_metadata: list[dict] = []
        arguments_registers: list[int] = []

        for argument in self.arguments:
            register, argument_code = argument.generate_code(register=register)

            # Keep track of the registers containing the arguments values
            arguments_registers.append(
                argument_code[0].get("metadata").get("register")
            )

            code_metadata.extend(argument_code)

        # The code for the function call itself is actually very simple! Just
        # jump-and-link (JAL), to keep track of the return address, and copy
        # the `returned_value_register` to `register`.
        func_call_code: list[dict[str, dict]] = [
            {
                "instruction": "JAL",
                "metadata": {"value": self.value}
            },
            {
                "instruction": "MOV",
                "metadata": {
                    "lhs_register": register,
                    "rhs_register": "ret_value",
                    "type": self.type
                }
            }
        ]
        register += 1

        code_metadata.extend(func_call_code)

        return register, code_metadata

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of the current `FUNC_CALL`, and set this attribute.

        For `FUNC_CALL` nodes, certificate each `argument` child first, and
        then the `FUNC_CALL` itself.

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

        return super().certificate(prime)

    def _build_children_nodes(self) -> list[Node]:
        arguments = self.function_call_metadata["arguments"]
        parameters_types: list[str] = [
            param["type"] for param in (
                self.function_call_metadata["called_function_metadata"]
                                           ["parameters"]
                                           .values()
            )
        ]

        children_nodes: list[Node] = []
        current_id = self.id

        for idx, argument_metadata in enumerate(arguments):
            _is_variable = argument_metadata["variable"]
            _parameter_type = parameters_types[idx]

            if _is_variable:
                argument_value = VAR(
                    id=current_id + 1,
                    variable_metadata=argument_metadata
                )

            else:
                argument_value = CST(
                    id=current_id + 1,
                    constant_metadata=argument_metadata
                )

            new_node = ARG(
                id=None,
                argument_value=argument_value,
                parameter_type=_parameter_type
            )

            current_id += 1
            children_nodes.append(new_node)

        return children_nodes
