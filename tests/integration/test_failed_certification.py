"""Integration test for the a program with tampered compilation."""

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.code_generator import CodeGenerator
from src.lexer import Lexer
from src.virtual_machine import VirtualMachine

from src.certificators import FrontendCertificator, BackendCertificator


def test_code_injection():
    """Test the code injection scenario."""

    source_code = """
    {
        a = 0;
        b = 10;

        while(a < 10) {
            b = b - 1;
            a = a + 1;
        }
    }
    """

    lexer = Lexer(source_code)
    parsed_source = lexer.parse_source_code()

    ast = AbstractSyntaxTree(source_code=parsed_source)
    ast.build()

    generator = CodeGenerator()
    generator.generate_code(node=ast.root)

    # Tampering the variable `b`, in order to export it to `c` after computing
    # the original source.
    code_to_inject = [
        {'instruction': 'IFETCH', 'id': 36, 'value': 'b'},
        {'instruction': 'ISTORE', 'id': 35, 'value': 'c'},
        {'instruction': 'IPOP', 'id': 33, 'value': None},
        {'instruction': 'HALT', 'id': 0, 'value': None}
    ]

    generator.code_collection = generator.code_collection[:-1] + code_to_inject

    vm = VirtualMachine(code_collection=generator.code_collection)

    frontend_certificator = FrontendCertificator(ast=ast)
    frontend_certificator.certificate()
    frontend_certificate = frontend_certificator.get_certificate()

    backend_certificator = BackendCertificator(
        code_collection=generator.code_collection
    )
    backend_certificator.certificate()
    backend_certificate = backend_certificator.get_certificate()

    # Assert the certification failed
    assert frontend_certificate != backend_certificate

    vm.run()

    # Assert the `vm.variables` have been tampered
    assert vm.variables["c"] == vm.variables["b"]

    untampered_variables = {'a': 10, 'b': 0}
    for key in untampered_variables.keys():
        assert vm.variables[key] == untampered_variables[key]


def test_variable_overwrite():
    """Test the variable overwriting scenario."""

    source_code = """
    {
        a = 1;
        b = 2;
        c = a + b;
    }
    """

    lexer = Lexer(source_code)
    parsed_source = lexer.parse_source_code()

    ast = AbstractSyntaxTree(source_code=parsed_source)
    ast.build()

    generator = CodeGenerator()
    generator.generate_code(node=ast.root)

    # Tampering the variable `a`, overwriting its value from `1` to `10`.
    generator.code_collection[1] = {
        'instruction': 'IPUSH',
        'id': 6,
        'value': 10
    }

    vm = VirtualMachine(code_collection=generator.code_collection)

    frontend_certificator = FrontendCertificator(ast=ast)
    frontend_certificator.certificate()
    frontend_certificate = frontend_certificator.get_certificate()

    backend_certificator = BackendCertificator(
        code_collection=generator.code_collection
    )
    backend_certificator.certificate()
    backend_certificate = backend_certificator.get_certificate()

    # Assert the certification failed
    assert frontend_certificate != backend_certificate

    vm.run()

    # Assert the `vm.variables` have been tampered
    assert vm.variables == {"a": 10, "b": 2, "c": 12}
