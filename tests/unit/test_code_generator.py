"""Implement unit tests for the `src.code_generator` module."""

from copy import deepcopy

from src.code_generator import CodeGenerator
from tests.unit.common import ABSTRACT_SYNTAX_TREE_ROOT, ENVIRONMENT, MACHINE_CODE


def test_init() -> None:
    """Test the instantiation of CodeGenerator objects."""

    _ast_root = deepcopy(ABSTRACT_SYNTAX_TREE_ROOT)
    cg = CodeGenerator(root=_ast_root)

    assert cg.root == ABSTRACT_SYNTAX_TREE_ROOT
    assert cg.program == {
        "functions": {},
        "global_vars": [],
        "data": {},
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


def test_parse_global_variables() -> None:
    """Test the `CodeGenerator.parse_global_variables` method."""

    _ast_root = deepcopy(ABSTRACT_SYNTAX_TREE_ROOT)
    cg = CodeGenerator(root=_ast_root)
    cg.parse_global_variables()

    expected_environment = ENVIRONMENT

    # Manually add the IDs
    current_id = 1
    for element in cg.program["global_vars"]:
        element["bytecode_id"] = current_id
        current_id += 1

    assert cg.environment == expected_environment


def test_parse_functions() -> None:
    """Test the `CodeGenerator.parse_functions` method."""

    _ast_root = deepcopy(ABSTRACT_SYNTAX_TREE_ROOT)
    cg = CodeGenerator(root=_ast_root)

    # Mock the `register` to offset the global variables
    cg.register = len(MACHINE_CODE["global_vars"])

    # Mock the `environment` to account for global variables
    cg.environment = ENVIRONMENT

    cg.parse_functions()

    expected_functions_indices = MACHINE_CODE["functions"]

    assert cg.program["functions"] == expected_functions_indices
