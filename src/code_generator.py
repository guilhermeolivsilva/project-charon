"""Implement a code generator for the virtual machine."""

from typing import Union

from src.nodes.base.node import Node


class CodeGenerator:
    """
    Code Generator that generates instructions for the virtual machine from
    Abstract Syntax Tree (AST) Nodes.
    """

    def __init__(self) -> None:
        self.code_collection: list[dict[str, Union[int, str, None]]] = []

    def __str__(self) -> str:
        """
        Implement a string representation of a CodeGenerator object.

        This method is internally invoked when using `print(codegen_obj)`.

        Returns
        -------
        _str : str
            The string representation of a CodeGenerator object.
        """

        return "\n".join(
            f"Instruction: {metadata['instruction']}, ID: {metadata['id']}, Value: {metadata['value']}"
            for metadata in self.code_collection
        )

    def generate_code(self, node: Node) -> None:
        """
        Generate code from a Node in the Abstract Syntax Tree.

        Parameters
        ----------
        node : Node
            The initial Node from the AST. (i.e., its `root`.)
        """

        # Ignore elements with `None` instruction
        self.code_collection = [
            code_metadata
            for code_metadata in node.generate_code()
            if code_metadata["instruction"] is not None
        ]
