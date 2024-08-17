"""Representation of STRUCT_DEF nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from src.ast_nodes.node import Node


class STRUCT_DEF(Node):
    """
    Implement the representation of a struct definition for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    struct_metadata : dict
        Dictionary of struct metadata exported by the Lexer.
    """

    @override
    def __init__(
        self,
        id: int,
        struct_metadata: dict[str, dict[str, dict]]
    ) -> None:
        # Clip the `%` sign from the pseudonymous computed by the Lexer,
        # and cast it to `int`.
        _pseudonymous: str = struct_metadata.get("pseudonymous")
        _relative_position: int = int(_pseudonymous[8:])

        super().__init__(id, _relative_position)

        _attribute_types: str = "^".join(
            f'({attribute.get("type_pseudonymous")})'
            for attribute in struct_metadata.get("attributes").values()
        )

        self.struct_metadata = struct_metadata
        self.symbol: str = f"({self.symbol})^{_attribute_types}"
        
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

        _attribute_types = ", ".join(
            attribute.get("type")
            for attribute in self.struct_metadata.get("attributes").values()
        )

        print(" " * (indent + 1) + f"Attributes: {_attribute_types}")

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of this `STRUCT_DEF`.

        For `STRUCT_DEF` nodes, the certificate is simply the `symbol` set
        during the object initialization.

        This method does not manipulate the `prime` parameter, as the notion of
        relative position of this `STRUCT_DEF` in the code is already obtained
        from the `struct_metadata`. Thus, it returns the same given `prime`.
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

        self.certificate_label = self.symbol

        return prime

    @override
    def generate_code(self) -> list:
        """
        Generate the code associated with this `EXPR`.

        For this node specialization, there is no code to be generated -- the
        struct definition is just an abstraction.

        Returns
        -------
        code_metadata : list
            An empty list.
        """

        return []
