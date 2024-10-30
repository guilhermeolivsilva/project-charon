"""Representation of PARAM nodes for the Abstract Syntax Tree."""

from typing_extensions import override

from src.ast_nodes.variables.VAR_DEF import VAR_DEF


class PARAM(VAR_DEF):
    """
    Implement the representation of a function parameter for the AST.

    As this is, essentially, a variable definition, it inherits from `VAR_DEF`
    and ovewrites the `instruction`.

    Parameters
    ----------
    id : int
        The ID of the Node.
    variable_metadata : dict
        Dictionary of parameter metadata exported by the Lexer.
    """

    @override
    def __init__(self, id: int, variable_metadata: dict) -> None:
        super().__init__(id, variable_metadata)

        self.instruction: str = "PARAM"
