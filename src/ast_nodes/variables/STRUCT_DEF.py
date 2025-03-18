"""Representation of STRUCT_DEF nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.utils import TYPE_SYMBOLS_MAP


class STRUCT_DEF(Node):
    """
    Implement the representation of a struct definition for the AST.

    Parameters
    ----------
    struct_metadata : dict
        Dictionary of struct metadata exported by the Lexer.
    """

    @override
    def __init__(self, struct_metadata: dict[str, dict[str, dict]]) -> None:
        id: int = struct_metadata.get("id")
        _type: str = struct_metadata.get("type")

        super().__init__(id, type=_type)

        self.active: bool = struct_metadata.get("active")
        self.struct_metadata = struct_metadata

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `STRUCT_DEF`.

        The node itself is aligned with `indent`, and the information about its
        attributes is padded with an additional left space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)

        _attribute_types = ", ".join(self.get_attribute_types())

        print(f"{' ' * (indent + 1)} Attributes: {_attribute_types}")

    @override
    def certificate(self, positional_prime: int) -> int:
        """
        Compute the certificate of this `STRUCT_DEF`.

        For `STRUCT_DEF` nodes, the certificate is simply the `symbol` set
        during the object initialization.

        Parameters
        ----------
        positional_prime : int
            A prime number that denotes the relative position of this node in
            the source code.

        Returns
        -------
        : int
            The very same received prime -- this node has no certificate itself.
        """

        return positional_prime

    @override
    def generate_code(
        self, register: int, environment: dict[int, str]
    ) -> tuple[
        list[dict[str, Union[int, str, float]]],
        int,
        dict[int, str]
    ]:
        """
        Generate the code associated with this `STRUCT_DEF`.

        For this node specialization, there is no code to be generated -- the
        struct definition is just an abstraction. Still, it takes a `register`
        as parameter, but returns it without incrementing it.

        Parameters
        ----------
        register : int
            The number of the register to be used by the code generated by this
            Node.
        environment : dict[int, str]
            The compiler's environment, that maps variables IDs to memory
            addresses.

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

        return [], register, environment

    def get_symbol(self) -> str:
        """
        Get the `symbol` attribute from this `STRUCT_DEF`.

        Returns
        -------
        : str
            The `symbol` attribute.
        """

        return self.symbol

    def get_attribute_types(self) -> list[str]:
        """
        Get the types of the attributes of this struct.

        The types are returned in the same order as they have been declared in
        the struct definition.

        Returns
        -------
        attribute_types : list[str]
            A list containing the attributes types.
        """

        attribute_types: list[str] = [
            attribute.get("type")
            for attribute in self.struct_metadata.get("attributes").values()
        ]

        return attribute_types

    def is_active(self) -> bool:
        """
        Tell whether this struct definition is `active` or not.

        A struct is `active` if at least one variable of its type has been
        defined in the source code.

        Returns
        -------
        active : bool
            Wheter the struct is active or not.
        """

        return self.active
