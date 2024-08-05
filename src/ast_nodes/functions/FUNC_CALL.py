"""Representation of FUNC_CALL nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.ast_nodes.basic.CST import CST
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
        # Clip the `#` sign from the pseudonymous computed by the Lexer,
        # and cast it to `int`.
        pseudonymous = function_call_metadata.get("function")
        _relative_position: int = int(pseudonymous[1:])

        super().__init__(id, _relative_position)

        self.instruction: str = "CALL"
        self.function_call_metadata = function_call_metadata
        self.parameters = self._build_children_nodes()

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `FUNC_CALL` nodes, obtain the certificates, recursively, from each
        `parameter` subtree first, and then from the `FUNC_CALL` node itself.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """

        certificate_label: list = []

        for parameter in self.parameters:
            certificate_label.append(*parameter.get_certificate_label())

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

        for parameter in self.parameters:
            parameter.print(indent=indent + 1)

    @override
    def generate_code(self) -> list[dict[str, Union[int, str, None]]]:
        """
        Generate the code associated with this `FUNC_CALL`.

        For this node specialization, generate code from `parameter` children
        nodes first, and then from the `FUNC_CALL` itself.

        Returns
        -------
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`, and node `id`, and `value`.
        """

        code_metadata: list[dict] = []

        for parameter in self.parameters:
            code_metadata.append(*parameter.generate_code())

        code_metadata.append(*super().generate_code())

        return code_metadata

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of the current `FUNC_CALL`, and set this attribute.

        For `FUNC_CALL` nodes, certificate each `parameter` child first, and
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

        for parameter in self.parameters:
            prime = parameter.certificate(prime)

        return super().certificate(prime)

    def _build_children_nodes(self) -> list[Node]:
        parameters = self.function_call_metadata.get("parameters")

        children_nodes: list[Node] = []
        current_id = self.id

        for parameter in parameters:
            _type = parameter.get("type")
            _value = parameter.get("value")

            if _type == "variable":
                new_node = VAR(
                    id=current_id + 1,
                    pseudonymous=_value
                )

            else:
                new_node = CST(
                    id=current_id + 1,
                    value=_value,
                    type=_type
                )

            current_id += 1
            children_nodes.append(new_node)

        return children_nodes
