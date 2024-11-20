"""Representation of ASSIGN nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.ast_nodes.variables.VAR import VAR
from src.ast_nodes.variables.ELEMENT_ACCESS import ELEMENT_ACCESS
from src.ast_nodes.operations.operation import Operation


class ASSIGN(Operation):
    """
    Implement the representation of a attribution operation for the AST.

    Parameters
    ----------
    lhs : Node
        The node representation of the variable to attribute to.
    rhs : Node
        The node representation of the expression to be attributed to `lhs`.

    Raises
    ------
    TypeError
        Raised if the `lhs` parameter is not a `VAR` or `ELEMENT_ACCESS` nodes.
    """

    @override
    def __init__(self, lhs: Node, rhs: Node) -> None:
        if not isinstance(lhs, (VAR, ELEMENT_ACCESS)):
            raise TypeError(
                "Left-hand side of ASSIGN operation is not a Variable."
            )

        super().__init__(lhs=lhs, rhs=rhs, type=lhs.type)

        self.instruction: str = "STORE"

    @override
    def generate_code(self, register: int) -> tuple[
        int,
        list[dict[str, Union[int, str, None]]]
    ]:
        """
        Generate the code associated with this `ASSIGN` operation.

        For this node specialization, generate code from the left and right
        hand sides nodes first, and then from the node itself.

        The `ASSIGN` operation does not need a register for itself. Thus, after
        generating the code, we "undo" the "register allocation" and decrement
        the `register` value to be returned.

        Not pretty. But works.

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

        register, operation_code = super().generate_code(register=register)
        assign_code = operation_code.pop()

        # Simply "undo" the `register` and `type` fields of the `assign` instruction :)
        del assign_code["metadata"]["register"]
        register -= 1

        # Rerrange the binary operation metadata to unary operation
        assign_code_metadata = assign_code.pop("metadata")
        assign_code_metadata["register"] = assign_code_metadata.pop("lhs_register")
        assign_code_metadata["value"] = assign_code_metadata.pop("rhs_register")

        assign_code["metadata"] = assign_code_metadata

        operation_code.append(assign_code)

        return register, operation_code
