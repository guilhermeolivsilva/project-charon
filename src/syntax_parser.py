"""Implement a syntax parser to use with the AST."""

from .abstract_syntax_tree import Node


def uses_global_id(func: callable) -> callable:
    """
    Decorate a function to enable it to access the `global_id_manager`.

    The decorated function will increment the `global_id_manager` by 1 after
    being called.

    Parameters
    ----------
    func : function
        The function to be decorated.

    Returns
    -------
    wrapper : function
        The decorated function.
    """

    def wrapper(cls, *args, **kwargs) -> callable:
        """
        Wrap the function to be decorated.

        Returns
        -------
        result : object
            The result of the decorated function.
        """
        try:
            result = func(cls, *args, **kwargs)
        except Exception:
            print(
                "Could not run decorated function.",
                "The ID counter was not affected."
            )
        else:
            cls.global_id_manager += 1

        return result

    return wrapper


class SyntaxParser:
    """Syntax Parser that translates input text to AST nodes."""

    def __init__(self) -> None:
        self._global_id_manager: int = 1

    @property
    def global_id_manager(self) -> int:
        return self._global_id_manager

    @global_id_manager.setter
    def global_id_manager(self, value: int) -> None:
        self._global_id_manager = value

    @uses_global_id
    def term(self, symbol: str, value: int) -> Node:
        """
        Generate a `term` for the AST.

        Terms are either a variable, a constant, or a paranthesis expression.

        Parameters
        ----------
        symbol : str
            The symbol to parse. If not "ID" or "INT", creates a
            `parenthesis_expression`.
        value : int
            The value to be stored in the Node.

        Returns
        -------
        term_node : Node
            The new `term` generated Node.
        """

        symbol_map = {
            "ID": Node(id=self.global_id_manager, kind="VAR", value=value),
            "INT": Node(id=self.global_id_manager, kind="CST", value=value),
        }

        try:
            term_node = symbol_map[symbol]
        except KeyError:
            term_node = self.parenthesis_expression()

        return term_node

    @uses_global_id
    def sum(self, symbol: str, lhs: Node, rhs: Node) -> Node:
        """
        Generate a `sum` for the AST.

        A `sum` is a triplet of Nodes consisting of the left and right hand
        side terms, and the `sum_node` itself – it might be either an addition
        or a subtraction.

        Parameters
        ----------
        symbol : str
            The symbol to parse. If not "ID" or "INT", creates a
            `parenthesis_expression`.
        lhs : Node
            The Node that represents the left hand side term of the operation.
        rhs : Node
            The Node that represents the right hand side term of the operation.

        Returns
        -------
        sum_node : Node
            The new `sum` generated Node.
        """
        symbol_map = {
            "PLUS": Node(id=self.global_id_manager, kind="ADD", value=-1),
            "MINUS": Node(id=self.global_id_manager, kind="SUB", value=-1),
        }

        sum_node = symbol_map[symbol]

        lhs.add_parent(sum_node)
        rhs.add_parent(sum_node)

        sum_node.add_child(lhs)
        sum_node.add_child(rhs)

        return sum_node
    
    @uses_global_id
    def comparison(self, lhs: Node, rhs: Node) -> Node:
        """
        Generate a `comparison` for the AST.

        A `comparison` is a triplet of Nodes consisting of the left and right
        hand side terms, and the `comparison` itself.

        TinyC currently only supports the "less than" (`<`) comparison.

        Parameters
        ----------
        lhs : Node
            The Node that represents the left hand side term of the operation.
        rhs : Node
            The Node that represents the right hand side term of the operation.

        Returns
        -------
        comparison_node : Node
            The new `comparison` generated Node.
        """
        comparison_node = Node(id=self.global_id_manager, kind="LT", value=-1)

        lhs.add_parent(comparison_node)
        rhs.add_parent(comparison_node)

        comparison_node.add_child(lhs)
        comparison_node.add_child(rhs)

        return comparison_node

    @uses_global_id
    def parenthesis_expression(self) -> Node:
        raise NotImplementedError()
