from .abstract_syntax_tree import Node
from .syntax_parser import SyntaxParser


class CodeGenerator:
    def __init__(self) -> None:
        self.parser: SyntaxParser = SyntaxParser()
        self.code_collection: list = []

    def __str__(self) -> str:
        return "\n".join(
            f"Instruction: {instruction}, Node: ({node})"
            for instruction, node in self.code_collection
        )

    def generate_code(self, node: Node) -> None:
        instruction_map = {
            "VAR": (
                self.parse_simple_node,
                {"instruction": "IFETCH"}
            ),
            "CST": (
                self.parse_simple_node,
                {"instruction": "IPUSH"}
            ),
            "ADD": (
                self.parse_simple_node,
                {"instruction": "IADD"}
            ),
            "SUB": (
                self.parse_simple_node,
                {"instruction": "ISUB"}
            ),
            "LT": (
                self.parse_simple_node,
                {"instruction": "ILT"}
            )
        }

        handler, kwargs = instruction_map[node.kind]

        handler(node=node, **kwargs)

    def parse_simple_node(self, node: Node, instruction: str) -> None:
        for child in node.children:
            self.generate_code(child)

        self.code_collection.append((instruction, node))
