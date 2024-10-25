"""Integration test to showcase the available operations."""

import pytest

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
            "expected_memory": {
                '0x0': 10,
                '0x2': 4,
                '0x6': 2.3,
                '0xa': 14,
                '0xc': 12
            }
        },
        {
            "function_name": "subtraction",
            "operator": "-",
            "expected_memory": {
                '0x0': 10,
                '0x2': 4,
                '0x6': 2.3,
                '0xa': 6,
                '0xc': 7
            }
        },
        {
            "function_name": "multiplication",
            "operator": "*",
            "expected_memory": {
                '0x0': 10,
                '0x2': 4,
                '0x6': 2.3,
                '0xa': 40,
                '0xc': 23
            }
        },
        {
            "function_name": "division",
            "operator": "/",
            "expected_memory": {
                '0x0': 10,
                '0x2': 4,
                '0x6': 2.3,
                '0xa': 2,
                '0xc': 4
            }
        },
        {
            "function_name": "greater_than",
            "operator": ">",
            "expected_memory": {
                '0x0': 10,
                '0x2': 4,
                '0x6': 2.3,
                '0xa': 1,
                '0xc': 1
            }
        },
        {
            "function_name": "less_than",
            "operator": "<",
            "expected_memory": {
                '0x0': 10,
                '0x2': 4,
                '0x6': 2.3,
                '0xa': 0,
                '0xc': 0
            }
        },
        {
            "function_name": "equal",
            "operator": "==",
            "expected_memory": {
                '0x0': 10,
                '0x2': 4,
                '0x6': 2.3,
                '0xa': 0,
                '0xc': 0
            }
        },
        {
            "function_name": "not_equal",
            "operator": "!=",
            "expected_memory": {
                '0x0': 10,
                '0x2': 4,
                '0x6': 2.3,
                '0xa': 1,
                '0xc': 1
            }
        },
        {
            "function_name": "logical_and",
            "operator": "&&",
            "expected_memory": {
                '0x0': 10,
                '0x2': 4,
                '0x6': 2.3,
                '0xa': 1,
                '0xc': 1
            }
        },
        {
            "function_name": "logical_or",
            "operator": "||",
            "expected_memory": {
                '0x0': 10,
                '0x2': 4,
                '0x6': 2.3,
                '0xa': 1,
                '0xc': 1
            }
        },
    ]
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
            "expected_memory": {
                '0x0': 11,
                '0x2': 3,
                '0x6': 88
            }
        },
        {
            "function_name": "right_shift",
            "operator": ">>",
            "expected_memory": {
                '0x0': 11,
                '0x2': 3,
                '0x6': 1
            }
        },
        {
            "function_name": "bitwise_and",
            "operator": "&",
            "expected_memory": {
                '0x0': 11,
                '0x2': 3,
                '0x6': 3
            }
        },
        {
            "function_name": "bitwise_or",
            "operator": "|",
            "expected_memory": {
                '0x0': 11,
                '0x2': 3,
                '0x6': 11
            }
        },
        {
            "function_name": "module",
            "operator": "%",
            "expected_memory": {
                '0x0': 11,
                '0x2': 3,
                '0x6': 2
            }
        },
    ]
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
