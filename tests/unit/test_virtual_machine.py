"""Implement unit tests for the `src.virtual_machine.VirtualMachine` class."""

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


def test_ALLOC() -> None:
    """Test the `VirtualMachine.ALLOC` method."""

    ...


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


def test_STORE() -> None:
    """Test the `VirtualMachine.STORE` method."""

    ...


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
