"""Implement unit tests for the `src.code_generator` module."""

from copy import deepcopy

from src.code_generator import CodeGenerator
from tests.unit.common import ABSTRACT_SYNTAX_TREE_ROOT, MACHINE_CODE


def test_init() -> None:
    """Test the instantiation of CodeGenerator objects."""

    _ast_root = deepcopy(ABSTRACT_SYNTAX_TREE_ROOT)
    cg = CodeGenerator(root=_ast_root)

    assert cg.root == ABSTRACT_SYNTAX_TREE_ROOT
    assert cg.program == {
        "structs": {},
        "functions": {},
        "global_vars": [],
        "code": []
    }
    assert cg.register == 0


def test_generate_code() -> None:
    """Test the `CodeGenerator.generate_code` method."""

    _ast_root = deepcopy(ABSTRACT_SYNTAX_TREE_ROOT)
    cg = CodeGenerator(root=_ast_root)
    generated_code = cg.generate_code()

    expected_generated_code = MACHINE_CODE
    assert generated_code == expected_generated_code


def test_parse_struct_definitions() -> None:
    """Test the `CodeGenerator.parse_struct_definitions` method."""

    _ast_root = deepcopy(ABSTRACT_SYNTAX_TREE_ROOT)
    cg = CodeGenerator(root=_ast_root)
    cg.parse_struct_definitions()

    expected_parsed_structs = MACHINE_CODE["structs"]
    assert cg.program["structs"] == expected_parsed_structs


def test_parse_global_variables() -> None:
    """Test the `CodeGenerator.parse_global_variables` method."""

    _ast_root = deepcopy(ABSTRACT_SYNTAX_TREE_ROOT)
    cg = CodeGenerator(root=_ast_root)
    cg.parse_global_variables()

    expected_parsed_global_vars = MACHINE_CODE["global_vars"]

    # Manually add the IDs
    current_id = 1
    for element in cg.program["global_vars"]:
        element["instruction_id"] = current_id
        current_id += 1

    assert cg.program["global_vars"] == expected_parsed_global_vars


def test_parse_functions() -> None:
    """Test the `CodeGenerator.parse_functions` method."""

    _ast_root = deepcopy(ABSTRACT_SYNTAX_TREE_ROOT)
    cg = CodeGenerator(root=_ast_root)

    # Mock the `register` to offset the global variables
    cg.register = len(MACHINE_CODE["global_vars"])
    cg.parse_functions()

    expected_functions_indices = MACHINE_CODE["functions"]

    assert cg.program["functions"] == expected_functions_indices
