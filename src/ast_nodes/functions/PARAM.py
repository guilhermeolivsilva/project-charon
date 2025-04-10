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
    def generate_code(
        self, register: int, environment: dict[str, dict[int, str]]
    ) -> tuple[
        list[dict[str, Union[int, str, float]]],
        int,
        dict[int, str]
    ]:
        """
        Generate the code associated with this `PARAM`.

        For this node specialization, update the environment to create a new
        variable, push its address to a `CONSTANT`, and add a `STORE`
        instruction to save the received argument value into the parameter.

        Parameters
        ----------
        register : int
            The number of the register to be used by the code generated by this
            Node.
        environment : dict[int, str]
            The compiler's environment, that maps variables IDs to memory
            addresses and function IDs to instructions indices.

        Returns
        -------
        code : list of dict
            Return a list of dictionaries containing code metadata: the register
            to be used, the related `instruction` and its metadata.
        register : int
            The number of the next register available.
        environment : dict[int, str]
            The updated {var_id: address} environment mapping.
        """

        code: list[dict[str, Union[int, str]]] = []

        # Update the environment with the variable address
        _, _, environment = super().generate_code(
            register=register,
            environment=environment
        )

        allocated_address = environment["variables"][self.value]["address"]

        # Emit a `CONSTANT` instruction with the address of the variable
        var_address_code = {
            "instruction": "CONSTANT",
            "metadata": {"register": register, "value": allocated_address}
        }
        code.append(var_address_code)

        # Store the argument into the parameter's allocated memory.
        _store_instruction = "STOREF" if self.type == "float" else "STORE"
        parameter_store_code = {
            "instruction": _store_instruction,
            "metadata": {"register": register, "value": "arg"},
        }
        code.append(parameter_store_code)

        return code, register + 1, environment
