"""Implement a code generator for the virtual machine."""

from .abstract_syntax_tree import Node
from .syntax_parser import SyntaxParser


class CodeGenerator:
    """
    Code Generator that generates instructions for the virtual machine from
    Abstract Syntax Tree (AST) Nodes.
    """

    def __init__(self) -> None:
        self.parser: SyntaxParser = SyntaxParser()
        self.code_collection: list = []

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
            f"Instruction: {instruction}, Node: ({node})"
            for instruction, node in self.code_collection
        )

    def generate_code(self, node: Node) -> None:
        """
        Generate code from a Node in the Abstract Syntax Tree.

        Parameters
        ----------
        node : Node
            A Node from the AST.
        """

        instruction_map = {
            "VAR": (self.parse_simple_node, {"instruction": "IFETCH"}),
            "CST": (self.parse_simple_node, {"instruction": "IPUSH"}),
            "ADD": (self.parse_simple_node, {"instruction": "IADD"}),
            "SUB": (self.parse_simple_node, {"instruction": "ISUB"}),
            "LT": (self.parse_simple_node, {"instruction": "ILT"}),
            "SET": (self.parse_set_node, {}),
            "IF": (self.parse_if_node, {}),
            "IFELSE": (self.parse_if_node, {"is_if_else": True}),
        }

        handler, kwargs = instruction_map[node.kind]

        handler(node=node, **kwargs)

    def parse_simple_node(self, node: Node, instruction: str) -> None:
        """
        Generate code from a simple Node.

        A simple Node's kind is either `VAR`, `CST`, `ADD`, `SUB` or `LT`.

        Parameters
        ----------
        node : Node
            The Node object to parse.
        instruction : str
            The instruction to add to the `code_collection`.
        """

        for child in node.children:
            self.generate_code(child)

        self.code_collection.append((instruction, node))

    def parse_set_node(self, node: Node, **kwargs) -> None:
        """
        Generate code from a `SET` kind Node.

        Parameters
        ----------
        node : Node
            The `SET` Node to parse.
        """

        lhs, rhs = node.children
        self.generate_code(rhs)

        self.code_collection.append(("ISTORE", lhs))

    def parse_if_node(self, node: Node, is_if_else: bool = False, **kwargs) -> None:
        """
        Generate code from an `IF` or `IFELSE` kind Node.

        Parameters
        ----------
        node : Node
            The `IF` or `IFELSE` Node to parse.
        is_if_else : bool, optional (default = False)
            A flag that indicates whether it is an `IF` or `IFELSE` Node. Set
            it to `True` if it is `IFELSE`. Defaults to `False`.
        """

        if is_if_else:
            expr, if_statement, else_statement = node.children
        else:
            expr, if_statement = node.children

        self.generate_code(expr)
        self.code_collection.append(("JZ", expr))

        self.generate_code(if_statement)
        self.code_collection.append(("JMP", if_statement))

        if is_if_else:
            self.generate_code(else_statement)