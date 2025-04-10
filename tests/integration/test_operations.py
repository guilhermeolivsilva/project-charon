"""Integration test to showcase the available operations."""

import pytest

from src.certificators import BackendCertificator, FrontendCertificator
from src.runner import create_instance


SOURCE_CODE = """
int {function_name}() {{
    short var_1;
    var_1 = 10;

    int var_2;
    var_2 = 4;

    float var_3;
    var_3 = 2.3;

    short result_1;
    result_1 = var_1 {operator} var_2;

    short result_2;
    result_2 = var_1 {operator} var_3;

    return 0;
}}

int main() {{
    {function_name}();

    return 0;
}}
"""

BITWISE_SOURCE_CODE = """
int {function_name}() {{
    short var_1;
    var_1 = 11;

    int var_2;
    var_2 = 3;

    short result_1;
    result_1 = var_1 {operator} var_2;

    return 0;
}}

int main() {{
    {function_name}();

    return 0;
}}
"""


@pytest.mark.parametrize(
    "test_suite",
    [
        {
            "function_name": "addition",
            "operator": "+",
            "expected_memory": {"0x0": 10, "0x4": 4, "0x8": 2.3, "0xc": 14, "0x10": 12},
        },
        {
            "function_name": "subtraction",
            "operator": "-",
            "expected_memory": {"0x0": 10, "0x4": 4, "0x8": 2.3, "0xc": 6, "0x10": 7},
        },
        {
            "function_name": "multiplication",
            "operator": "*",
            "expected_memory": {"0x0": 10, "0x4": 4, "0x8": 2.3, "0xc": 40, "0x10": 23},
        },
        {
            "function_name": "division",
            "operator": "/",
            "expected_memory": {"0x0": 10, "0x4": 4, "0x8": 2.3, "0xc": 2, "0x10": 4},
        },
        {
            "function_name": "greater_than",
            "operator": ">",
            "expected_memory": {"0x0": 10, "0x4": 4, "0x8": 2.3, "0xc": 1, "0x10": 1},
        },
        {
            "function_name": "less_than",
            "operator": "<",
            "expected_memory": {"0x0": 10, "0x4": 4, "0x8": 2.3, "0xc": 0, "0x10": 0},
        },
        {
            "function_name": "equal",
            "operator": "==",
            "expected_memory": {"0x0": 10, "0x4": 4, "0x8": 2.3, "0xc": 0, "0x10": 0},
        },
        {
            "function_name": "not_equal",
            "operator": "!=",
            "expected_memory": {"0x0": 10, "0x4": 4, "0x8": 2.3, "0xc": 1, "0x10": 1},
        },
        {
            "function_name": "logical_and",
            "operator": "&&",
            "expected_memory": {"0x0": 10, "0x4": 4, "0x8": 2.3, "0xc": 1, "0x10": 1},
        },
        {
            "function_name": "logical_or",
            "operator": "||",
            "expected_memory": {"0x0": 10, "0x4": 4, "0x8": 2.3, "0xc": 1, "0x10": 1},
        },
    ],
)
def test_operation(test_suite: dict) -> None:
    """Test an operation."""

    test_parameters = {
        key: value
        for key, value in test_suite.items()
        if key in ["function_name", "operator"]
    }

    instance = create_instance(source_code=SOURCE_CODE.format(**test_parameters))
    vm = instance.get_vm()
    vm.run()

    assert vm.get_memory() == test_suite["expected_memory"]


@pytest.mark.parametrize(
    "test_suite",
    [
        {
            "function_name": "left_shift",
            "operator": "<<",
            "expected_memory": {"0x0": 11, "0x4": 3, "0x8": 88},
        },
        {
            "function_name": "right_shift",
            "operator": ">>",
            "expected_memory": {"0x0": 11, "0x4": 3, "0x8": 1},
        },
        {
            "function_name": "bitwise_and",
            "operator": "&",
            "expected_memory": {"0x0": 11, "0x4": 3, "0x8": 3},
        },
        {
            "function_name": "bitwise_or",
            "operator": "|",
            "expected_memory": {"0x0": 11, "0x4": 3, "0x8": 11},
        },
        {
            "function_name": "module",
            "operator": "%",
            "expected_memory": {"0x0": 11, "0x4": 3, "0x8": 2},
        },
    ],
)
def test_bitwise_operation(test_suite: dict) -> None:
    """Test a bit-wise operation."""

    test_parameters = {
        key: value
        for key, value in test_suite.items()
        if key in ["function_name", "operator"]
    }

    instance = create_instance(
        source_code=BITWISE_SOURCE_CODE.format(**test_parameters)
    )
    vm = instance.get_vm()
    vm.run()

    assert vm.get_memory() == test_suite["expected_memory"]


# @pytest.mark.parametrize(
#     "test_suite",
#     [
#         {"function_name": "addition", "operator": "+"},
#         {"function_name": "subtraction", "operator": "-"},
#         {"function_name": "multiplication", "operator": "*"},
#         {"function_name": "division", "operator": "/"},
#         {"function_name": "greater_than", "operator": ">"},
#         {"function_name": "less_than", "operator": "<"},
#         {"function_name": "equal", "operator": "=="},
#         {"function_name": "not_equal", "operator": "!="},
#         {"function_name": "logical_and", "operator": "&&"},
#         {"function_name": "logical_or", "operator": "||"},
#     ],
# )
# def test_operation_certification(test_suite: dict) -> None:
#     """Test the front and backend certification."""

#     test_parameters = {
#         key: value
#         for key, value in test_suite.items()
#         if key in ["function_name", "operator"]
#     }

#     instance = create_instance(source_code=SOURCE_CODE.format(**test_parameters))

#     ast = instance.get_ast()
#     frontend_certificate = FrontendCertificator(ast=ast).certificate()

#     program = instance.get_program()
#     backend_certificate = BackendCertificator(program=program).certificate()

#     assert frontend_certificate == backend_certificate


# @pytest.mark.parametrize(
#     "test_suite",
#     [
#         {"function_name": "left_shift", "operator": "<<"},
#         {"function_name": "right_shift", "operator": ">>"},
#         {"function_name": "bitwise_and", "operator": "&"},
#         {"function_name": "bitwise_or", "operator": "|"},
#         {"function_name": "module", "operator": "%"},
#     ],
# )
# def test_bitwise_operation(test_suite: dict) -> None:
#     """Test the front and backend certification."""

#     test_parameters = {
#         key: value
#         for key, value in test_suite.items()
#         if key in ["function_name", "operator"]
#     }

#     instance = create_instance(
#         source_code=BITWISE_SOURCE_CODE.format(**test_parameters)
#     )

#     ast = instance.get_ast()
#     frontend_certificate = FrontendCertificator(ast=ast).certificate()

#     program = instance.get_program()
#     backend_certificate = BackendCertificator(program=program).certificate()

#     assert frontend_certificate == backend_certificate
