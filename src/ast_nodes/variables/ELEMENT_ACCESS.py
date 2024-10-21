"""Representation of ELEMENT_ACCESS nodes for the Abstract Syntax Tree."""

from typing import Union

from typing_extensions import override

from src.ast_nodes.node import Node
from src.ast_nodes.variables.VAR import VAR
from src.ast_nodes.basic.CST import CST
from src.ast_nodes.certificate_mapping import NODE_SYMBOLS_MAP, TYPE_SYMBOLS_MAP
from src.utils import builtin_types


class ELEMENT_ACCESS(Node):
    """
    Implement the representation of an elemment access node for the AST.

    An element access is used within the context of arrays (indexes), and
    structs (attributes).

    This Node typechecks, and raises a `TypeError` if `variable` does not have a
    `length` attribute -- i.e., is not an array or struct.

    Parameters
    ----------
    id : int
        The ID of the Node.
    variable : str
        The variable whose element is being accessed.
    element : int
        The index of the element being accessed.

    Raises
    ------
    TypeError
        - Raised if `variable` is not an array or a struct.
    """

    @override
    def __init__(
        self,
        id: int,
        variable: VAR,
        element: Union[CST, VAR]
    ) -> None:

        variable_metadata = variable.get_metadata()

        self.is_array = "length" in variable_metadata
        self.is_struct = "attributes" in variable_metadata

        if not (self.is_array or self.is_struct):
            raise TypeError(
                "Trying to access an element from variable that is not an array"
                " nor struct"
            )

        super().__init__(id)

        self.instruction = "ELEMENT_VALUE"
        self.symbol: str = NODE_SYMBOLS_MAP.get("ELEMENT_VALUE")

        self.variable: VAR = variable
        self.element: Union[CST, VAR] = element
        self.type: str = self._compute_element_type()

    @override
    def get_certificate_label(self) -> list[str]:
        """
        Get the contents of `certificate_label`.

        For `ELEMENT_ACCESS` nodes, obtain the certificates, recursively, from
        the `variable` and `element` subtrees first, and then from the
        `ELEMENT_ACCESS` node itself.

        Returns
        -------
        : list of str
            A list containing the certificate label of the `Node`.
        """

        certificate_label: list = [
            *self.variable.get_certificate_label(),
            *self.element.get_certificate_label(),
            *super().get_certificate_label(),
        ]

        return certificate_label

    @override
    def print(self, indent: int = 0) -> None:
        """
        Print the string representation of this `ELEMENT_ACCESS`.

        The node itself is aligned with `indent`, and its children (the
        variable and the element index) are padded with an additional left
        space.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The number of left padding spaces to indent.
        """

        super().print(indent)
        self.variable.print(indent=indent + 1)
        self.element.print(indent=indent + 1)

    @override
    def generate_code(self, register: int) -> tuple[
        int,
        list[dict[str, Union[int, str]]]
    ]:
        """
        Generate the code associated with this `ELEMENT_ACCESS`.

        For this node specialization, generate code from `variable` and
        `element` children nodes first, respectively, and then from the
        `ELEMENT_ACCESS` itself.

        Parameters
        ----------
        register : int
            The number of the register to be used by the code generated by this
            Node. This register will contain the element being accessed.

        Returns
        -------
        register : int
            The number of the next register available.
        code_metadata : list of dict
            Return a list of dictionaries containing code metadata: the related
            `instruction`, and node `id`, and `value`.
        """

        code_metadata: list[dict[str, Union[int, str]]] = []

        register, variable_code = self.variable.generate_code(
            register=register
        )
        code_metadata.extend(variable_code)

        register, element_code = self.element.generate_code(
            register=register
        )
        code_metadata.extend(element_code)
        element_register = register - 1

        element_access_code = {
            "instruction": self.instruction,
            "metadata": {
                "id": self.id,
                "register": register,
                "variable_relative_position": self.variable.get_value()
            }
        }

        # Compute the offset, in bytes, to reach the accessed element
        element_offset: dict = self._compute_element_offset(
            element_register=element_register
        )

        element_access_code["metadata"] = {
            **element_access_code["metadata"],
            **element_offset
        }

        code_metadata.append(element_access_code)

        register += 1

        return register, code_metadata

    @override
    def certificate(self, prime: int) -> int:
        """
        Compute the certificate of the current `ELEMENT_ACCESS`, and set this attribute.

        For `ELEMENT_ACCESS` nodes, certificate `variable` and `element`
        children first, and then the `ELEMENT_ACCESS` itself.

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

        prime = self.variable.certificate(prime)
        prime = self.element.certificate(prime)

        return super().certificate(prime)
    
    def add_context(self, context: dict[str, str]) -> None:
        """
        Add context to this `ELEMENT_ACCESS` node.

        The context indicates whether this variable is being readed or written.

        Parameters
        ----------
        context : dict[str, str]
            A dictionary containing the relative position where it was first
            declared in the original source code, and its type.
        """

        _context: str = context.get("context", "read")
        symbol: str = ""

        if _context == "read":
            self.instruction: str = "ELEMENT_VALUE"
            symbol = NODE_SYMBOLS_MAP.get("ELEMENT_VALUE")

        else:
            self.instruction: str = "ELEMENT_ADDRESS"
            symbol = NODE_SYMBOLS_MAP.get("ELEMENT_ADDRESS")

        self.symbol = f"({symbol})"
    
    def _compute_element_type(self) -> str:
        """
        Compute the type of this `ELEMENT_ACCESS`.

        The type of this Node is the type of the element being accessed as
        declared in its `variable_metadata`.

        Returns
        -------
        : str
            The type of the accessed element.
        """

        variable_metadata = self.variable.get_metadata()
        variable_type: str = variable_metadata["type"]

        # If the type of the struct-like variable is in this mapping, then it is
        # an array.
        if variable_type in TYPE_SYMBOLS_MAP:
            return variable_type
        
        # If not, then it is an "actual" struct. Thus, get the type of the
        # element being accessed.
        struct_attributes = variable_metadata["attributes"]
        accessed_attribute_index: int = self.element.get_value()
        accessed_attribute_name: str = list(struct_attributes)[accessed_attribute_index]
        accessed_attribute_type: str = struct_attributes[accessed_attribute_name]["type"]

        return accessed_attribute_type

    def _compute_element_offset(self, element_register: int) -> dict:
        """
        Compute the number of bytes to offset in order to reach the accessed element.

        This method handles 3 possible cases:

        - A: the `variable` is an array, and the `element` is a constant (i.e.,
        statically indexed).
        - B: the `variable` is an array, but the `element` is a variable (i.e.,
        dinamically indexed).
        - C: the `variable` is a struct, and the `element` is, necessarily, a
        constant.

        Parameters
        ----------
        element_register : int
            The number of the register that contains the value of the `element`.
            Will only be used in case B.

        Returns
        -------
        element_offset : dict
            A dictionary containing further metadata about how to access the
            intended `element` from `variable`.
        """

        element_offset: dict = {}

        if self.is_array:
            variable_type_size: int = builtin_types.get(self.variable.get_type())

            # Case A
            if isinstance(self.element, CST):
                index: int = self.element.get_value()

                offset_size: int = variable_type_size * index

                element_offset["offset_size"] = offset_size
                element_offset["offset_mode"] = "static"

            # Case B
            else:
                element_offset["offset_mode"] = "dynamic"
                element_offset["element_register"] = element_register
                element_offset["variable_type_size"] = variable_type_size
        
        # Case C
        else:
            variable_metadata: dict = self.variable.get_metadata()
            variable_attributes: dict = variable_metadata.get("attributes")

            offset_size: int = 0

            # Iterate over the attributes and sum the offset, in bytes, until
            # the `element` is found

            for attribute_metadata in variable_attributes.values():
                attribute_position: int = attribute_metadata.get("attr_pointer")

                if attribute_position == self.element.get_value():
                    break

                attribute_type: str = attribute_metadata.get("type")
                attribute_size: int = builtin_types.get(attribute_type)

                offset_size += attribute_size

            element_offset["offset_size"] = offset_size
            element_offset["offset_mode"] = "static"

        return element_offset
