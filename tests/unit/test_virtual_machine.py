"""Implement unit tests for the `src.virtual_machine.VirtualMachine` class."""

import pytest

from src.virtual_machine import VirtualMachine
from tests.unit.common import MACHINE_CODE


def test_init() -> None:
    """Test the instantiation of VirtualMachine objects."""

    ...


def test_run() -> None:
    """Test the `VirtualMachine.run` method."""

    ...


def test_ADD() -> None:
    """Test the `VirtualMachine.ADD` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = lhs + rhs

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_metadata = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.ADD(instruction_metadata=instruction_metadata)

    assert vm.registers[result_register] == expected_result

@pytest.mark.parametrize(
    "test_suite",
    [
        # Simple variable
        {
            "instruction_metadata": {
                "id": 0,
                "type": "int",
                "relative_position": 0
            },
            "expected_result": {
                "memory_pointer": 4,
                "variables": {0: "0x0"}
            }
        },

        # Struct
        {
            "instruction_metadata": {
                "id": 0,
                "type": "my_struct",
                "relative_position": 0
            },
            "expected_result": {
                "memory_pointer": 8,
                "variables": {0: "0x0"}
            }
        },

        # Array
        {
            "instruction_metadata": {
                "id": 0,
                "type": "int",
                "relative_position": 0,
                "length": 3
            },
            "expected_result": {
                "memory_pointer": 12,
                "variables": {0: "0x0"}
            }
        },
    ]
)
def test_ALLOC_success(test_suite) -> None:
    """Test the `VirtualMachine.ALLOC` method for successful allocations."""

    vm = VirtualMachine(program=MACHINE_CODE)

    instruction_metadata: dict = test_suite.get("instruction_metadata")
    vm.ALLOC(instruction_metadata=instruction_metadata)

    expected_result: dict = test_suite.get("expected_result")

    assert vm.memory_pointer == expected_result["memory_pointer"]
    assert vm.variables == expected_result["variables"]


@pytest.mark.parametrize(
    "test_suite",
    [
        # Upfront full memory
        {
            "instruction_metadata": {
                "id": 0,
                "type": "int",
                "relative_position": 0
            },
            "vm_settings": {
                "memory_size": 0
            }
        },

        # Memory does not have enough space for the new variable
        {
            "instruction_metadata": {
                "id": 0,
                "type": "my_struct",
                "relative_position": 0
            },
            "vm_settings": {
                "memory_size": 4
            }
        },
    ]
)
def test_ALLOC_failure(test_suite) -> None:
    """Test the `VirtualMachine.ALLOC` method for failed allocations."""

    vm_settings: dict = test_suite.get("vm_settings")
    vm = VirtualMachine(program=MACHINE_CODE, **vm_settings)

    with pytest.raises(MemoryError):
        instruction_metadata: dict = test_suite.get("instruction_metadata")
        vm.ALLOC(instruction_metadata=instruction_metadata)


def test_AND() -> None:
    """Test the `VirtualMachine.AND` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = int(bool(lhs and rhs))

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_metadata = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.AND(instruction_metadata=instruction_metadata)

    assert vm.registers[result_register] == expected_result


def test_BITAND() -> None:
    """Test the `VirtualMachine.BITAND` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = lhs & rhs

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_metadata = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.BITAND(instruction_metadata=instruction_metadata)

    assert vm.registers[result_register] == expected_result


def test_BITOR() -> None:
    """Test the `VirtualMachine.BITOR` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = lhs | rhs

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_metadata = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.BITOR(instruction_metadata=instruction_metadata)

    assert vm.registers[result_register] == expected_result


def test_CALL() -> None:
    """Test the `VirtualMachine.CALL` method."""

    ...


def test_CONSTANT() -> None:
    """Test the `VirtualMachine.CONSTANT` method."""

    ...


def test_DIV() -> None:
    """Test the `VirtualMachine.DIV` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = int(lhs / rhs)

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_metadata = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.DIV(instruction_metadata=instruction_metadata)

    assert vm.registers[result_register] == expected_result


def test_ELEMENT_PTR() -> None:
    """Test the `VirtualMachine.ELEMENT_PTR` method."""

    ...


def test_EQ() -> None:
    """Test the `VirtualMachine.EQ` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = int(lhs == rhs)

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_metadata = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.EQ(instruction_metadata=instruction_metadata)

    assert vm.registers[result_register] == expected_result


def test_FADD() -> None:
    """Test the `VirtualMachine.FADD` method."""

    ...


def test_FAND() -> None:
    """Test the `VirtualMachine.FAND` method."""

    ...


def test_FDIV() -> None:
    """Test the `VirtualMachine.FDIV` method."""

    ...


def test_FEQ() -> None:
    """Test the `VirtualMachine.FEQ` method."""

    ...


def test_FGT() -> None:
    """Test the `VirtualMachine.FGT` method."""

    ...


def test_FLT() -> None:
    """Test the `VirtualMachine.FLT` method."""

    ...


def test_FMULT() -> None:
    """Test the `VirtualMachine.FMULT` method."""

    ...


def test_FOR() -> None:
    """Test the `VirtualMachine.FOR` method."""

    ...


def test_FSUB() -> None:
    """Test the `VirtualMachine.FSUB` method."""

    ...


def test_GT() -> None:
    """Test the `VirtualMachine.GT` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = int(lhs > rhs)

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_metadata = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.GT(instruction_metadata=instruction_metadata)

    assert vm.registers[result_register] == expected_result


def test_HALT() -> None:
    """Test the `VirtualMachine.HALT` method."""

    ...


def test_JMP() -> None:
    """Test the `VirtualMachine.JMP` method."""

    ...


def test_JNZ() -> None:
    """Test the `VirtualMachine.JNZ` method."""
    ...


def test_JZ() -> None:
    """Test the `VirtualMachine.JZ` method."""

    ...


def test_LOAD() -> None:
    """Test the `VirtualMachine.LOAD` method."""

    vm = VirtualMachine(program=MACHINE_CODE, memory_size=10)

    expected_value = 77
    expected_value_register = 3

    # I.e., save the contents of the variable of relative position `2` to
    # register `3`
    instruction_metadata = {
        "register": expected_value_register,
        "value": 2
    }

    vm.variables = {
        0: "0x0",
        1: "0x4",
        2: "0x8"
    }

    vm.memory = {
        "0x0": 123,
        "0x1": 321,
        "0x2": 23,
        "0x3": 35,
        "0x4": 6,
        "0x5": 13,
        "0x6": 32,
        "0x7": 34,
        "0x8": expected_value,
        "0x9": 7
    }

    vm.LOAD(instruction_metadata=instruction_metadata)

    assert vm.registers[expected_value_register] == expected_value


def test_LSHIFT() -> None:
    """Test the `VirtualMachine.LSHIFT` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = lhs << rhs

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_metadata = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.LSHIFT(instruction_metadata=instruction_metadata)

    assert vm.registers[result_register] == expected_result


def test_LT() -> None:
    """Test the `VirtualMachine.LT` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = int(lhs < rhs)

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_metadata = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.LT(instruction_metadata=instruction_metadata)

    assert vm.registers[result_register] == expected_result


def test_MULT() -> None:
    """Test the `VirtualMachine.MULT` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = lhs * rhs

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_metadata = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.MULT(instruction_metadata=instruction_metadata)

    assert vm.registers[result_register] == expected_result


def test_PARAM() -> None:
    """Test the `VirtualMachine.PARAM` method."""

    vm = VirtualMachine(program=MACHINE_CODE, memory_size=20)

    expected_value_address = "0x8"
    expected_value = 23
    expected_value_relative_position = 1

    vm.memory_pointer = int(expected_value_address, 16)
    vm.variables = {0: "0x0", 2: "0xF"}
    vm.memory = {
        "0x0": 123321,
        "0xF": -1
    }
    vm.parameters = [expected_value]

    instruction_metadata = {
        "type": "int",
        "relative_position": expected_value_relative_position,
        "length": 1,
    }

    vm.PARAM(instruction_metadata)

    assert vm.variables[expected_value_relative_position] == expected_value_address
    assert vm.memory[expected_value_address] == expected_value


def test_OR() -> None:
    """Test the `VirtualMachine.OR` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = int(bool(lhs or rhs))

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_metadata = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.OR(instruction_metadata=instruction_metadata)

    assert vm.registers[result_register] == expected_result


def test_RET() -> None:
    """Test the `VirtualMachine.RET` method."""

    ...


def test_RSHIFT() -> None:
    """Test the `VirtualMachine.RSHIFT` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = lhs >> rhs

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_metadata = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.RSHIFT(instruction_metadata=instruction_metadata)

    assert vm.registers[result_register] == expected_result


def test_STORE_simple() -> None:
    """
    Test the `VirtualMachine.STORE` method when handling simple variables.

    In this case, the `lhs_register` contains the `relative_position` of the
    variable to be written to.
    """

    vm = VirtualMachine(program=MACHINE_CODE, memory_size=20)

    instruction_metadata = {
        "lhs_register": 0,
        "rhs_register": 1
    }

    value_to_store = 23
    vm.registers = {
        0: 0,
        1: value_to_store
    }

    store_address = "0x0"
    vm.variables = {0: store_address}

    vm.STORE(instruction_metadata)

    assert vm.memory[store_address] == value_to_store


def test_STORE_arrays_structs() -> None:
    """
    Test the `VirtualMachine.STORE` method when handling arrays/structs.
    
    In this case, the `lhs_register` contains the memory address to write to.
    """

    vm = VirtualMachine(program=MACHINE_CODE, memory_size=20)

    instruction_metadata = {
        "lhs_register": 0,
        "rhs_register": 1
    }

    value_to_store = 23
    store_address = "0x8"

    vm.registers = {
        0: store_address,
        1: value_to_store
    }

    vm.STORE(instruction_metadata)

    assert vm.memory[store_address] == value_to_store


def test_SUB() -> None:
    """Test the `VirtualMachine.SUB` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = lhs - rhs

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_metadata = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.SUB(instruction_metadata=instruction_metadata)

    assert vm.registers[result_register] == expected_result
