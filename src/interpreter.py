"""Implement the Tiny C interpreter."""

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

    lexer = Lexer(source_code)
    parsed_source = lexer.parse_source_code()

    ast = AbstractSyntaxTree(source_code=parsed_source)
    ast.build()

    generator = CodeGenerator()
    generator.generate_code(node=ast.root)

    vm = VirtualMachine(code_collection=generator.code_collection)

    frontend_certificator = FrontendCertificator(ast=ast)
    frontend_certificator.certificate()

    backend_certificator = BackendCertificator(
        code_collection=generator.code_collection
    )
    backend_certificator.certificate()

    instance = {
        "vm": vm,
        "frontend_certificate": frontend_certificator.get_certificate(),
        "backend_certificate": backend_certificator.get_certificate()
    }

    return instance
