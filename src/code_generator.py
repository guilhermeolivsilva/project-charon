"""Implement a code generator for the virtual machine."""

from src.node import Node


class CodeGenerator:
    """
    Code Generator that generates instructions for the virtual machine from
    Abstract Syntax Tree (AST) Nodes.
    """

    instructions = [
        "IFETCH",
        "IPUSH",
        "ISTORE",
        "IPOP",
        "IADD",
        "ISUB",
        "ILT",
        "HALT",
        "JZ",
        "JMP",
        "JNZ"
        "EMPTY",
    ]

    def __init__(self) -> None:
        self.code_collection: list[tuple[str, Node]] = []

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
            The initial Node from the AST. (i.e., its `root`.)
        """

        instruction_map = {
            "VAR": (self.parse_simple_node, {"instruction": "IFETCH"}),
            "CST": (self.parse_simple_node, {"instruction": "IPUSH"}),
            "ADD": (self.parse_simple_node, {"instruction": "IADD"}),
            "SUB": (self.parse_simple_node, {"instruction": "ISUB"}),
            "LT": (self.parse_simple_node, {"instruction": "ILT"}),
            "EXPR": (
                self.parse_simple_node,
                {"instruction": "IPOP", "children_first": True},
            ),
            "PROG": (
                self.parse_simple_node,
                {"instruction": "HALT", "children_first": True},
            ),
            "EMPTY": (self.parse_simple_node, {"instruction": "EMPTY"}),
            "SET": (self.parse_set_node, {}),
            "IF": (self.parse_if_node, {}),
            "IFELSE": (self.parse_if_else_node, {}),
            "WHILE": (self.parse_while_node, {}),
            "DO": (self.parse_do_while_node, {}),
            "SEQ": (self.parse_sequence, {})
        }

        handler, kwargs = instruction_map[node.kind]

        handler(node=node, **kwargs)

    def parse_simple_node(
        self, node: Node, instruction: str, children_first: bool = True, **kwargs
    ) -> None:
        """
        Generate code from a simple Node.

        A simple Node's kind is either `VAR`, `CST`, `ADD`, `SUB` or `LT`.

        Parameters
        ----------
        node : Node
            The Node object to parse.
        instruction : str
            The instruction to add to the `code_collection`.
        children_first : bool, optional (default=True)
            If enabled, generates code from children Nodes before adding the
            `instruction` to the `code_collection`. Defaults to `True`.
        """

        if not children_first:
            self.code_collection.append((instruction, node))

        for child in node.children:
            self.generate_code(child)

        if children_first:
            self.code_collection.append((instruction, node))

    def parse_set_node(self, node: Node, **kwargs) -> None:
        """
        Generate code from a `SET` kind Node.

        Parameters
        ----------
        node : Node
            The `SET` Node to parse.
        """

        # Making the Code Generator compatible with AST pruning.
        if node.value is not None:
            lhs = Node(id=node.id, kind="VAR", value=node.value)
            lhs.set_certificate_label(node.certificate_label)
            rhs = node.children[0]
        else:
            lhs, rhs = node.children

        self.generate_code(rhs)

        self.code_collection.append(("ISTORE", lhs))

    def parse_if_node(self, node: Node, **kwargs) -> None:
        """
        Generate code from an `IF` kind Node.

        Parameters
        ----------
        node : Node
            The `IF` Node to parse.
        """

        expr, if_statement = node.children

        self.generate_code(expr)

        last_if_command = if_statement.children[-1]
        self.code_collection.append(("JZ", last_if_command))

        self.generate_code(if_statement)

    def parse_if_else_node(self, node: Node, **kwargs) -> None:
        """
        Generate code from an `IFELSE` kind Node.

        Parameters
        ----------
        node : Node
            The `IFELSE` Node to parse.
        """

        expr, if_statement, else_statement = node.children

        self.generate_code(expr)

        first_else_command = else_statement
        self.code_collection.append(("JZ", first_else_command))

        self.generate_code(if_statement)

        last_else_command = else_statement.children[-1]
        self.code_collection.append(("JMP", last_else_command))
        self.generate_code(else_statement)

    def parse_while_node(self, node: Node, **kwargs) -> None:
        """
        Generate code from a `WHILE` Node.

        Parameters
        ----------
        node : Node
            The `WHILE` Node to parse.
        """

        expr, statement = node.children

        self.generate_code(expr)

        dummy_node = Node(id=node.id, kind="EMPTY")
        self.code_collection.append(("JZ", dummy_node))

        self.generate_code(statement)

        first_expression_node = expr.children[0]
        self.code_collection.append(("JMP", first_expression_node))
        self.code_collection.append(("EMPTY", dummy_node))

    def parse_do_while_node(self, node: Node, **kwargs) -> None:
        """
        Generate code from a `DOWHILE` Node.

        Parameters
        ----------
        node : Node
            The `DOWHILE` Node to parse.
        """

        statement, expr = node.children

        self.generate_code(statement)
        self.generate_code(expr)

        first_statement_node = statement.children[0]

        self.code_collection.append(("JNZ", first_statement_node))

    def parse_sequence(self, node: Node, **kwargs) -> None:
        """
        Generate code from a sequence of commands.

        Parameters
        ----------
        node : Node
            The Node object to parse.
        """

        dummy_node = Node(id=node.id, kind="SEQ")
        self.code_collection.append(("EMPTY", dummy_node))

        for child in node.children:
            self.generate_code(child)
