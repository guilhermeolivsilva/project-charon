"""Implement unit tests for the `src.virtual_machine.VirtualMachine` class."""

import pytest

from src.virtual_machine import VirtualMachine
from tests.unit.common import MACHINE_CODE


def test_init() -> None:
    """Test the instantiation of VirtualMachine objects."""

    memory_size = 20

    vm = VirtualMachine(program=MACHINE_CODE, memory_size=memory_size)

    assert vm.program == MACHINE_CODE
    assert vm.memory == {hex(_byte): None for _byte in range(memory_size)}
    assert vm.memory_size == memory_size
    assert vm.memory_pointer == 0x0
    assert vm.program_counter == 0
    assert vm.registers == {
        "arg": [],
        "ret_address": [],
        "ret_value": [],
        "zero": 0
    }
    assert vm.variables == {}


def test_get_memory() -> None:
    """Test the `VirtualMachine.get_memory` method."""

    memory_size = 8

    vm = VirtualMachine(program=MACHINE_CODE, memory_size=memory_size)
    vm.memory = {
        '0x0': 1,
        '0x1': None,
        '0x2': None,
        '0x3': None,
        '0x4': 2,
        '0x5': None,
        '0x6': 35,
        '0x7': None
    }

    expected_memory = {'0x0': 1, '0x4': 2, '0x6': 35}

    assert vm.get_memory() == expected_memory


def test_run() -> None:
    """Test the `VirtualMachine.run` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    vm.run()

    expected_memory = {
        '0x30': 3,
        '0x34': 1,
        '0x38': 2,
        '0x3c': 1,
        '0x40': 2.0,
        '0x46': 1,
        '0x4e': 2.0,
        '0x52': 123,
        '0x6a': 1,
        '0x7e': 1
    }

    assert vm.get_memory() == expected_memory


def test_ADD() -> None:
    """Test the `VirtualMachine.ADD` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = lhs + rhs

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.ADD(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_ADDRESS() -> None:
    """Test the `VirtualMachine.ADDRESS` method."""

    vm = VirtualMachine(program=MACHINE_CODE, memory_size=10)

    variable_id = 2
    expected_value_register = 3
    expected_address = "0x8"

    # I.e., save the contents of the variable of ID `2` to
    # register `3`
    instruction_params = {
        "register": expected_value_register,
        "value": variable_id,
    }

    vm.variables = {
        0: "0x0",
        1: "0x4",
        variable_id: expected_address
    }

    vm.ADDRESS(instruction_params=instruction_params)

    assert vm.registers[expected_value_register] == expected_address


@pytest.mark.parametrize(
    "test_suite",
    [
        # Simple variable
        {
            "instruction_params": {
                "id": 0,
                "size": 4,
                "id": 0,
                "register": 0
            },
            "expected_result": {
                "memory_pointer": 4,
                "variables": {0: "0x0"}
            }
        },

        # Struct
        {
            "instruction_params": {
                "id": 0,
                "size": 8,
                "id": 0,
                "register": 0
            },
            "expected_result": {
                "memory_pointer": 8,
                "variables": {0: "0x0"}
            }
        },

        # Array
        {
            "instruction_params": {
                "id": 0,
                "size": 12,
                "id": 0,
                "register": 0
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

    instruction_params: dict = test_suite.get("instruction_params")
    vm.ALLOC(instruction_params=instruction_params)

    expected_result: dict = test_suite.get("expected_result")

    assert vm.memory_pointer == expected_result["memory_pointer"]
    assert vm.variables == expected_result["variables"]


@pytest.mark.parametrize(
    "test_suite",
    [
        # Upfront full memory
        {
            "instruction_params": {
                "id": 0,
                "size": 4,
                "id": 0,
                "register": 0
            },
            "vm_settings": {
                "memory_size": 0
            }
        },

        # Memory does not have enough space for the new variable
        {
            "instruction_params": {
                "id": 0,
                "size": 8,
                "id": 0,
                "register": 0
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
        instruction_params: dict = test_suite.get("instruction_params")
        vm.ALLOC(instruction_params=instruction_params)


def test_AND() -> None:
    """Test the `VirtualMachine.AND` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = int(bool(lhs and rhs))

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.AND(instruction_params=instruction_params)

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

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.BITAND(instruction_params=instruction_params)

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

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.BITOR(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_CONSTANT() -> None:
    """Test the `VirtualMachine.CONSTANT` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    expected_value = 23
    result_register = 0

    instruction_params = {
        "register": result_register,
        "value": expected_value,
        "type": "int"
    }

    vm.CONSTANT(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_value


def test_DIV() -> None:
    """Test the `VirtualMachine.DIV` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = int(lhs / rhs)

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.DIV(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_EQ() -> None:
    """Test the `VirtualMachine.EQ` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = int(lhs == rhs)

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.EQ(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_FADD() -> None:
    """Test the `VirtualMachine.FADD` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23.4, 0
    rhs, rhs_register = 35.9, 1
    result_register = 2

    expected_result = lhs + rhs

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.FADD(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_FAND() -> None:
    """Test the `VirtualMachine.FAND` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 1.12, 0
    rhs, rhs_register = 0, 1
    result_register = 2

    expected_result = int(bool(lhs and rhs))

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.FAND(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_FDIV() -> None:
    """Test the `VirtualMachine.FDIV` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23.4, 0
    rhs, rhs_register = 3, 1
    result_register = 2

    expected_result = lhs / rhs

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.FDIV(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_FEQ() -> None:
    """Test the `VirtualMachine.FEQ` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23.1, 0
    rhs, rhs_register = 35.44, 1
    result_register = 2

    expected_result = int(lhs == rhs)

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.FEQ(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_FGT() -> None:
    """Test the `VirtualMachine.FGT` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23.1, 0
    rhs, rhs_register = 35.12, 1
    result_register = 2

    expected_result = int(lhs > rhs)

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.GT(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_FLT() -> None:
    """Test the `VirtualMachine.FLT` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23.1, 0
    rhs, rhs_register = 35.12, 1
    result_register = 2

    expected_result = int(lhs < rhs)

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.LT(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_FMULT() -> None:
    """Test the `VirtualMachine.FMULT` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23.12, 0
    rhs, rhs_register = 35.44, 1
    result_register = 2

    expected_result = lhs * rhs

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.MULT(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_FNEQ() -> None:
    """Test the `VirtualMachine.FNEQ` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23.1, 0
    rhs, rhs_register = 35.44, 1
    result_register = 2

    expected_result = int(lhs != rhs)

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.FNEQ(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_FOR() -> None:
    """Test the `VirtualMachine.FOR` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23.12, 0
    rhs, rhs_register = 35.99, 1
    result_register = 2

    expected_result = int(bool(lhs or rhs))

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.OR(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result

def test_FSUB() -> None:
    """Test the `VirtualMachine.FSUB` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23.12, 0
    rhs, rhs_register = 35.99, 1
    result_register = 2

    expected_result = lhs - rhs

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.SUB(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_GT() -> None:
    """Test the `VirtualMachine.GT` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = int(lhs > rhs)

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.GT(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_HALT() -> None:
    """Test the `VirtualMachine.HALT` method."""

    ...


def test_JR() -> None:
    """Test the `VirtualMachine.JR` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    jump_register = 1
    jump_size = 23
    expected_program_counter = jump_size

    vm.registers[jump_register] = jump_size

    instruction_params = {
        "register": jump_register
    }

    vm.JR(instruction_params=instruction_params)

    assert vm.program_counter == expected_program_counter


def test_JZ_true() -> None:
    """
    Test the `VirtualMachine.JZ` method.

    For this test, the `conditional_register` contains a `true` value (1).
    """

    vm = VirtualMachine(program=MACHINE_CODE)

    jump_size = 23
    expected_program_counter = vm.program_counter
    conditional_register = 0

    instruction_params = {
        "conditional_register": conditional_register,
        "jump_size": jump_size
    }

    vm.registers[conditional_register] = 1

    vm.JZ(instruction_params=instruction_params)

    assert vm.program_counter == expected_program_counter


def test_JZ_false() -> None:
    """
    Test the `VirtualMachine.JZ` method.

    For this test, the `conditional_register` contains a `false` value (1).
    """

    vm = VirtualMachine(program=MACHINE_CODE)

    jump_size = 23
    expected_program_counter = jump_size - 1
    conditional_register = 0

    instruction_params = {
        "conditional_register": conditional_register,
        "jump_size": jump_size
    }

    vm.registers[conditional_register] = 0

    vm.JZ(instruction_params=instruction_params)

    assert vm.program_counter == expected_program_counter


def test_LOAD() -> None:
    """Test the `VirtualMachine.LOAD` method."""

    vm = VirtualMachine(program=MACHINE_CODE, memory_size=10)

    expected_value = 77
    expected_value_register = 3

    # I.e., save the contents of the variable of ID `2` to
    # register `3`
    instruction_params = {
        "register": expected_value_register,
        "value": 2,
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

    vm.LOAD(instruction_params=instruction_params)

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

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.LSHIFT(instruction_params=instruction_params)

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

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.LT(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_MOD() -> None:
    """Test the `VirtualMachine.MOD` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = lhs % rhs

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.MOD(instruction_params=instruction_params)

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

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.MULT(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_NEQ() -> None:
    """Test the `VirtualMachine.NEQ` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = int(lhs != rhs)

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.NEQ(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_OR() -> None:
    """Test the `VirtualMachine.OR` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = int(bool(lhs or rhs))

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.OR(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_RSHIFT() -> None:
    """Test the `VirtualMachine.RSHIFT` method."""

    vm = VirtualMachine(program=MACHINE_CODE)

    lhs, lhs_register = 23, 0
    rhs, rhs_register = 35, 1
    result_register = 2

    expected_result = lhs >> rhs

    vm.registers[lhs_register] = lhs
    vm.registers[rhs_register] = rhs

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.RSHIFT(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result


def test_STORE_simple() -> None:
    """
    Test the `VirtualMachine.STORE` method when handling simple variables.

    In this case, `register` contains the register with the `id`
    of the variable to be written to.
    """

    vm = VirtualMachine(program=MACHINE_CODE, memory_size=20)

    instruction_params = {
        "register": 0,
        "value": 1
    }

    value_to_store = 23
    vm.registers = {
        0: 0,
        1: value_to_store
    }

    store_address = "0x0"
    vm.variables = {0: store_address}

    vm.STORE(instruction_params)

    assert vm.memory[store_address] == value_to_store


def test_STORE_arrays_structs() -> None:
    """
    Test the `VirtualMachine.STORE` method when handling arrays/structs.
    
    In this case, `register` contains the register with the address to write to.
    """

    vm = VirtualMachine(program=MACHINE_CODE, memory_size=20)

    instruction_params = {
        "register": 0,
        "value": 1
    }

    value_to_store = 23
    store_address = "0x8"

    vm.registers = {
        0: store_address,
        1: value_to_store
    }

    vm.STORE(instruction_params)

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

    instruction_params = {
        "id": 15,
        "register": 2,
        "lhs_register": lhs_register,
        "rhs_register": rhs_register
    }

    vm.SUB(instruction_params=instruction_params)

    assert vm.registers[result_register] == expected_result
