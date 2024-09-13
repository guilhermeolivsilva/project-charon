"""Implement a code generator for the virtual machine."""

from src.ast_nodes.basic.PROG import PROG


class CodeGenerator:
    """
    Code Generator that generates instructions for the virtual machine from
    Abstract Syntax Tree (AST) Nodes.

    This class also keeps track of the structs defined in the source code that
    have been instantiated -- structs that have been defined, but not
    instantiated, are ignored.

    Parameters
    ----------
    root : PROG
        The root of an Abstract Syntax Tree generated by the 
        `src.abstract_syntax_tree.AbstractSyntaxTree`. class
    """

    def __init__(self, root: PROG) -> None:
        self.root: PROG = root
        self.code: dict[str, dict] = {
            "structs": {},
            "global_vars": {},
            "functions": {}
        }

    def __str__(self) -> str:
        """
        Implement a string representation of a CodeGenerator object.

        This method is intended to be used with `print(codegen_obj)`.

        Returns
        -------
        _str : str
            The string representation of a CodeGenerator object.
        """

        ...

    def generate_code(self) -> dict[str, dict]:
        """
        Generate code from a the root of an Abstract Syntax Tree.

        The generated code will also be stored in the `self.code` attribute. 
        
        Returns
        -------
        code : dict[str, dict]
            A dictionary with bytecodes and struct metadata generated from some
            Abstract Syntax Tree representation of a program.
        """

        ...

    def parse_struct_definitions(self) -> None:
        """
        Parse struct definitions and add it to the generated code.

        For structs, we only keep track of the types used by the struct, and
        the the order they appear in.
        """

        ...

    def parse_global_variables(self) -> None:
        """
        Generate code for global variables and add it to the generated code.
        """

        ...

    def parse_functions(self) -> None:
        """
        Generate code for each function and add it to the generated code.
        """

        ...

    def get_code(self) -> dict[str, dict]:
        """
        Get the generated code.
        
        Returns
        -------
        code : dict[str, dict]
            The generated code.
        """

        return self.code
