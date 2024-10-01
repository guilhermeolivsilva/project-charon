"""Generate a runner for Charon programs."""

from typing import Union

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.certificators import BackendCertificator, FrontendCertificator
from src.code_generator import CodeGenerator
from src.lexer import Lexer
from src.virtual_machine import VirtualMachine


def create_instance(source_code: str) -> dict[str, Union[VirtualMachine, str]]:
    """
    Create an instance that certificates and runs the input `source_code`.

    Parameters
    ----------
    source_code : str
        The source code to parse and load on the Virtual Machine.

    Returns
    -------
    instance : dict[str, Union[VirtualMachine, str]]
        A dictionary with code metadata and a Virtual Machine loaded with it.
        Fields:
         - vm : VirtualMachine
            The Virtual Machine loaded with the `source_code`.
         - frontend_certificate : str
            The computed certificate of the frontend code.
         - backend_certificate : str
            The computed certificate of the backend code.
    """

    lexer = Lexer(source_code=source_code)
    parsed_source = lexer.parse_source_code()

    ast = AbstractSyntaxTree(source_code=parsed_source)
    ast.build()

    generator = CodeGenerator(root=ast.get_root())
    program = generator.generate_code()

    vm = VirtualMachine(program=program)

    instance = {
        "vm": vm
    }

    return instance
