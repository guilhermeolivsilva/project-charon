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
            "INT": Node(id=self.global_id_manager, kind="CST", value=value)
        }
        
        try:
            term_node = symbol_map[symbol]
        except KeyError:
            term_node = self.parenthesis_expression()

        return term_node

    @uses_global_id
    def parenthesis_expression(self) -> Node:
        raise NotImplementedError()