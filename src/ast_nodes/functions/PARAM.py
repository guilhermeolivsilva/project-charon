"""Representation of PARAM nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.variables.VAR_DEF import VAR_DEF


class PARAM(VAR_DEF):
    """
    Implement the representation of a function parameter for the AST.

    This is pretty much the same as a VAR_DEF. It just has a different name to
    make the AST easier to read, and generates a `STORE` instruction in order to
    save received argument into the parameter's memory location.

    Parameters
    ----------
    variable_metadata : dict
        Dictionary of parameter metadata exported by the Lexer.
    """

    @override
    def __init__(self, variable_metadata: dict) -> None:
        super().__init__(variable_metadata)

    @override
    def generate_code(self, register: int) -> tuple[
        int,
        list[dict[str, Union[int, str]]]
    ]:
        """
        Generate the code associated with this `PARAM`.

        For this node specialization, generate an instruction to allocate memory
        (`ALLOC`) for this parameter, and an instruction `STORE` to save the
        received argument value into the parameter.

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

        code_metadata: list[dict[str, Union[int, str]]] = []

        # First instruction: memory allocation
        register, parameter_allocation_code = super().generate_code(register)
        code_metadata.extend(parameter_allocation_code)

        # Second instruction: store the argument into the parameter's allocated
        # memory.
        parameter_address_register = register - 1
        parameter_store_code = {
            "instruction": "STORE",
            "metadata": {
                "register": parameter_address_register,
                "value": "arg",
                "type": self.type
            }
        }
        code_metadata.append(parameter_store_code)

        return register, code_metadata

