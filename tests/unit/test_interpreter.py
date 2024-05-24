"""Implement unit tests for the `src.interpreter` module."""

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.code_generator import CodeGenerator
from src.interpreter import create_instance
from src.lexer import Lexer


def test_create_instance():
    """Test the `create_instance` function."""

    source_code = """
    {
        a = 1;
        b = 2;
        c = b;

        if (a < b) {
            d = 9;
        }
        else {
            d = 1;
        }
    }
    """

    instance = create_instance(source_code)

    vm, frontend_certificate, backend_certificate = instance.values()

    expected_parsed_source = Lexer.parse_source_code(source_code)

    expected_ast = AbstractSyntaxTree(expected_parsed_source)
    expected_ast.build()

    code_generator = CodeGenerator()
    code_generator.generate_code(expected_ast.root)

    for expected, tested in zip(code_generator.code_collection, vm.code_collection):
        expected_instruction, expected_id, expected_value = expected.values()
        tested_instruction, tested_id, tested_value = tested.values()

        assert expected_instruction == tested_instruction
        assert expected_id == tested_id
        assert expected_value == tested_value

    assert frontend_certificate == backend_certificate

    vm.run()

    assert vm.variables == {"a": 1, "b": 2, "c": 2, "d": 9}
