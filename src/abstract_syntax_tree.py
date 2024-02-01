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
    value : int, optional (default = -1)
        The value the Node holds, if any. Defaults to -1.
    """

    def __init__(self, id: int, kind: str, value: int or None = None) -> None:
        self.id: int = id
        self.kind: str = kind
        self.value: int or None = value
        self.parent: Node = None
        self.children: list = []

    def add_child(self, child: "Node") -> None:
        """
        Add a Node to the `self.children` list.

        Parameters
        ----------
        child : Node
            The Node to be added.
        """
        self.children.append(child)

    def add_parent(self, parent: "Node") -> None:
        """
        Set a Node as this object's parent.

        Parameters
        ----------
        parent : Node
            A Node object to be set as the parent of `this`.
        """
        self.parent = parent

    def __str__(self) -> str:
        """
        Implement a string representation of a Node object.

        This method is internally invoked when using `print(node_obj)`.

        Returns
        -------
        _str : str
            The string representation of a Node object.
        """
        _str = f"ID: {self.id}, Kind: {self.kind}, Value: {self.value}"

        if self.parent:
            _str += f", Parent ID: {self.parent.id}"

        return _str


class AbstractSyntaxTree:
    """
    Implement the AST itself.

    The AST is always initialized with a root, with ID 0.
    """

    def __init__(self) -> None:
        self.root: Node = Node(id=0, kind="PROG", value=-1)

    # TODO: assert no IDs are duplicate.
    # TODO: implement a tree traversal method.
