"""Implement unit tests for the `src.interpreter` module."""

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.code_generator import CodeGenerator
from src.interpreter import create_virtual_machine
from src.lexer import Lexer


def test_create_virtual_machine():
    """Test the `create_virtual_machine` function."""

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

    vm = create_virtual_machine(source_code)

    expected_parsed_source = Lexer.parse_source_code(source_code)

    expected_ast = AbstractSyntaxTree(expected_parsed_source)
    expected_ast.build()

    code_generator = CodeGenerator()
    code_generator.generate_code(expected_ast.root)

    for expected, tested in zip(code_generator.code_collection, vm.code_collection):
        expected_instruction, expected_node = expected
        tested_instruction, tested_node = tested

        assert expected_instruction == tested_instruction
        assert expected_node == tested_node

    vm.run()

    assert vm.variables == {"a": 1, "b": 2, "c": 2, "d": 9}
