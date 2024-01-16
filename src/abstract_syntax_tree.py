"""Implement the Abstract Syntax Tree (AST)."""


class Node:
    """
    Implement a Node for the AST.

    Parameters
    ----------
    id : int
        The ID of the Node.
    kind : str
        The Node kind. Must be VAR, CST, ADD, SUB, LT, SET, IF1, IF2, WHILE,
        DO, EMPTY, SEQ, EXPR, or PROG.
    value : int, optional (default = 0)
        The value the Node holds, if any. Defaults to zero.
    """
    def __init__(self, id: int, kind: str, value: int = 0) -> None:
        self.id: int = id
        self.kind: str = kind
        self.value: int = value
        self.parent: Node = None
        self.children: list = []


class AbstractSyntaxTree:
    """
    Implement the AST itself.

    The AST is always initialized with a root, with ID 0.
    """
    def __init__(self) -> None:
        self.root: Node = Node(id=0, kind="PROG", value=0)

    # TODO: assert no IDs are duplicate.
    # TODO: implement a tree traversal method.