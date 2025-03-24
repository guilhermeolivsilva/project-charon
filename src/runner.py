"""Generate a runner for Charon programs."""

from copy import deepcopy

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.certificators import BackendCertificator, FrontendCertificator
from src.code_generator import CodeGenerator
from src.lexer import Lexer
from src.virtual_machine import VirtualMachine


class Charon:
    """
    This class represents an instance of a program in [C]haron.

    An instance is composed by the parsed source (i.e., the output from the
    `Lexer`), the Abstract Syntax Tree, a Virtual Machine, and the frontend and
    backend certificators.

    The goal of this class is to centralize all of this generated metadata in a
    single object.

    Parameters
    ----------
    parsed_source : dict[str, dict]
        The source code after being tokenized and parsed by the Lexer.
    ast : AbstractSyntaxTree
        The Abstract Syntax Tree of this progrma.
    program : dict[str, dict]
        The compiled program, to be executed by the Virtual Machine.
    vm : VirtualMachine
        An instance of `VirtualMachine` loaded with the `program`.
    frontend_certificator : FrontendCertificator
        An instance of `FrontendCertificator` loaded with the `ast`.
    backend_certificator : BackendCertificator
        An instance of `BackendCertificator` loaded with the `program`.
    """

    def __init__(
        self,
        parsed_source: dict[str, dict],
        ast: AbstractSyntaxTree,
        code_generator: CodeGenerator,
        program: dict[str, dict],
        vm: VirtualMachine,
        frontend_certificator: FrontendCertificator,
        backend_certificator: BackendCertificator,
    ) -> None:
        self.parsed_source = parsed_source
        self.ast = ast
        self.code_generator = code_generator
        self.program = program
        self.vm = vm
        self.frontend_certificator = frontend_certificator
        self.backend_certificator = backend_certificator

    def get_parsed_source(self) -> dict[str, dict]:
        """Get the `parsed_source` attribute."""

        return self.parsed_source

    def get_ast(self) -> AbstractSyntaxTree:
        """Get the `ast` attribute."""

        return self.ast
    
    def get_code_generator(self) -> CodeGenerator:
        """Get the `code_generator` attribute."""

        return self.code_generator

    def get_program(self) -> dict[str, dict]:
        """Get the `program` attribute."""

        return self.program

    def get_vm(self) -> VirtualMachine:
        """Get the `vm` attribute."""

        return self.vm

    def get_frontend_certificator(self) -> FrontendCertificator:
        """Get the `frontend_certificator` attribute."""

        return self.frontend_certificator

    def get_backend_certificator(self) -> BackendCertificator:
        """Get the `backend_certificator` attribute."""

        return self.backend_certificator


def create_instance(source_code: str) -> Charon:
    """
    Create an instance that certificates and runs the input `source_code`.

    Parameters
    ----------
    source_code : str
        The source code to parse and load on the Virtual Machine.

    Returns
    -------
    instance : Charon
        An instance of this [C]haron program.
    """

    lexer = Lexer(source_code=source_code)
    parsed_source = lexer.parse_source_code()

    _parsed_source = deepcopy(parsed_source)
    ast = AbstractSyntaxTree(source_code=_parsed_source)
    ast.build()

    generator = CodeGenerator(root=ast.get_root())
    program = generator.generate_code()

    vm = VirtualMachine(program=program)

    frontend_certificator = FrontendCertificator(ast=ast)

    # TODO: uncomment this
    # backend_certificator = BackendCertificator(program=program)
    backend_certificator = ...

    _instance = {
        "parsed_source": parsed_source,
        "ast": ast,
        "code_generator": generator,
        "program": program,
        "vm": vm,
        "frontend_certificator": frontend_certificator,
        "backend_certificator": backend_certificator,
    }

    return Charon(**_instance)
