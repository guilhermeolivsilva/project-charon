"""Implement the Tiny C interpreter."""

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.code_generator import CodeGenerator
from src.lexer import Lexer
from src.virtual_machine import VirtualMachine


def create_virtual_machine(source_code: str) -> VirtualMachine:
    """
    Create a Virtual Machine that runs the input `source_code`.

    Parameters
    ----------
    source_code : str
        The source code to parse and load on the Virtual Machine.

    Returns
    -------
    vm : VirtualMachine
        A Virtual Machine instance loaded with the source code.
    """

    parsed_source = Lexer.parse_source_code(source_code)

    ast = AbstractSyntaxTree(source_code=parsed_source)
    ast.build()

    generator = CodeGenerator()
    generator.generate_code(node=ast.root)

    vm = VirtualMachine(code_collection=generator.code_collection)

    return vm

