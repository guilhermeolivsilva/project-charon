"""Implement a syntax parser to use with the AST."""

from abstract_syntax_tree import Node


def uses_global_id(func: function) -> function:
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

    def wrapper(cls, *args, **kwargs) -> function:
        """
        Wrap the function to be decorated.

        Returns
        -------
        result : object
            The result of the decorated function.
        """
        result = func(cls, *args, **kwargs)
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
