"""Implement unit tests for the `src.virtual_machine.VirtualMachine` class."""

from src.virtual_machine import VirtualMachine


HALT_INSTRUCTION = {
    "instruction": "HALT",
    "id": -1,
    "value": None
}


def test_init() -> None:
    """Test the instantiation of VirtualMachine objects."""

    code_collection = [
        {
            "instruction": "IFETCH",
            "id": 1,
            "value": "a"
        },
        HALT_INSTRUCTION
    ]
    stack_size = 10

    vm = VirtualMachine(code_collection=code_collection, stack_size=stack_size)

    assert len(vm.stack) == stack_size
    assert not any(vm.stack)
    assert all(code in vm.code_collection for code in code_collection)
    assert vm.stack_pointer == vm.program_counter == 0


def test_run() -> None:
    """
    Test the `VirtualMachine.run` method.
    
    This test is omitted because all of its possibilities are covered by the
    following `test_run_...` tests.
    """

    ...


def test_run_ifetch() -> None:
    """Test the `ifetch` instruction handling with the `run` method."""

    test_value = 23
    code_collection = [
        {
            "instruction": "IFETCH",
            "id": 1,
            "value": "a"
        },
        HALT_INSTRUCTION
    ]

    vm = VirtualMachine(code_collection=code_collection, stack_size=1)
    vm.variables = {"a": test_value}

    vm.run()

    # Assert the method was called and the `stack` has the expected value
    assert vm.stack == [test_value]


def test_run_ipush() -> None:
    """Test the `ipush` instruction handling with the `run` method."""

    test_value = 23

    code_collection = [
        {
            "instruction": "IPUSH",
            "id": 1,
            "value": test_value
        },
        HALT_INSTRUCTION
    ]

    vm = VirtualMachine(code_collection=code_collection, stack_size=1)

    vm.run()
    assert vm.stack == [test_value]


def test_run_istore() -> None:
    """Test the `istore` instruction handling with the `run` method."""

    test_value = 23
    test_variable = "a"

    code_collection = [
        {
            "instruction": "ISTORE",
            "id": 1,
            "value": test_variable
        },
        HALT_INSTRUCTION
    ]

    vm = VirtualMachine(code_collection=code_collection, stack_size=1)
    vm.stack = [test_value]

    vm.run()

    assert vm.stack == [test_value]
    assert vm.variables == {test_variable: test_value}


def test_run_ipop() -> None:
    """Test the `ipop` instruction handling with the `run` method."""

    test_value = 23

    code_collection = [
        {
            "instruction": "IPOP",
            "id": 1,
            "value": None
        },
        HALT_INSTRUCTION
    ]

    vm = VirtualMachine(code_collection=code_collection, stack_size=1)

    # Mock the stack to only contain the `test_value`, and point the
    # `stack_pointer` to it
    vm.stack.append(test_value)
    vm.stack_pointer = 1
    vm.run()

    # Assert the `test_value` has been removed from the stack
    assert vm.stack_pointer == 0
    assert test_value not in vm.stack


def test_run_iadd() -> None:
    """Test the `iadd` instruction handling with the `run` method."""

    lhs_value = 23
    lhs = {
        "instruction": "IPUSH",
        "id": 1,
        "value": lhs_value
    }

    rhs_value = 35
    rhs = {
        "instruction": "IPUSH",
        "id": 2,
        "value": rhs_value
    }

    iadd_instruction = {
        "instruction": "IADD",
        "id": 3,
        "value": None
    }

    code_collection = [
        lhs,
        rhs,
        iadd_instruction,
        HALT_INSTRUCTION
    ]

    vm = VirtualMachine(code_collection=code_collection, stack_size=2)
    vm.run()

    assert vm.stack == [lhs_value + rhs_value, rhs_value]


def test_run_isub() -> None:
    """Test the `isub` instruction handling with the `run` method."""

    lhs_value = 23
    lhs = {
        "instruction": "IPUSH",
        "id": 1,
        "value": lhs_value
    }

    rhs_value = 35
    rhs = {
        "instruction": "IPUSH",
        "id": 2,
        "value": rhs_value
    }

    isub_instruction = {
        "instruction": "ISUB",
        "id": 3,
        "value": None
    }

    code_collection = [
        lhs,
        rhs,
        isub_instruction,
        HALT_INSTRUCTION
    ]

    vm = VirtualMachine(code_collection=code_collection, stack_size=2)
    vm.run()

    assert vm.stack == [lhs_value - rhs_value, rhs_value]


def test_run_ilt() -> None:
    """Test the `ilt` instruction handling with the `run` method."""

    lhs_value = 23
    lhs = {
        "instruction": "IPUSH",
        "id": 1,
        "value": lhs_value
    }

    rhs_value = 35
    rhs = {
        "instruction": "IPUSH",
        "id": 2,
        "value": rhs_value
    }

    ilt_instruction = {
        "instruction": "ILT",
        "id": 3,
        "value": None
    }

    code_collection = [
        lhs,
        rhs,
        ilt_instruction,
        HALT_INSTRUCTION
    ]

    vm = VirtualMachine(code_collection=code_collection, stack_size=2)
    vm.run()

    assert vm.stack == [lhs_value < rhs_value, rhs_value]


def test_run_jmp() -> None:
    """Test the `jmp` instruction handling with the `run` method."""

    ran_instruction_1_value = 23
    ignored_instruction_values = 35
    ran_instruction_2_value = 13

    instruction_to_run = {
        "instruction": "IPUSH",
        "id": 1,
        "value": 23
    }

    instruction_to_ignore = {
        "instruction": "IPUSH",
        "id": 2,
        "value": 35
    }

    another_instruction_to_run = {
        "instruction": "IPUSH",
        "id": 3,
        "value": 13
    }

    jmp_instruction = {
        "instruction": "JMP",
        "id": -1,
        "value": 3
    }

    code_collection = [
        instruction_to_run,
        jmp_instruction,
        instruction_to_ignore,
        another_instruction_to_run,
        HALT_INSTRUCTION
    ]

    vm = VirtualMachine(code_collection=code_collection, stack_size=3)

    vm.run()

    assert ran_instruction_1_value in vm.stack
    assert ran_instruction_2_value in vm.stack
    assert ignored_instruction_values not in vm.stack


def test_run_jz_true() -> None:
    """Test the `jz` instruction handling with the `run` method.

    In this test, assert that the `jz` method correctly handles `True`
    conditions.
    """

    condition_instruction = {
        "instruction": "IPUSH",
        "id": 1,
        "value": True
    }

    instruction_to_run = {
        "instruction": "IPUSH",
        "id": 2,
        "value": 23
    }

    another_instruction_to_run = {
        "instruction": "IPUSH",
        "id": 3,
        "value": 35
    }

    conditional_jump_instruction = {
        "instruction": "JZ",
        "id": -1,
        "value": 3
    }

    code_collection = [
        condition_instruction,
        conditional_jump_instruction,
        instruction_to_run,
        another_instruction_to_run,
        HALT_INSTRUCTION
    ]

    vm = VirtualMachine(code_collection=code_collection, stack_size=3)

    vm.run()

    assert vm.stack == [
        condition_instruction["value"],
        instruction_to_run["value"],
        another_instruction_to_run["value"]
    ]


def test_run_jz_false() -> None:
    """Test the `jz` instruction handling with the `run` method.

    In this test, assert that the `jz` method correctly handles `False`
    conditions.
    """

    condition_instruction = {
        "instruction": "IPUSH",
        "id": 1,
        "value": False
    }

    instruction_to_ignore = {
        "instruction": "IPUSH",
        "id": 2,
        "value": 23
    }

    instruction_to_run = {
        "instruction": "IPUSH",
        "id": 3,
        "value": 35
    }

    conditional_jump_instruction = {
        "instruction": "JZ",
        "id": -1,
        "value": 3
    }

    code_collection = [
        condition_instruction,
        conditional_jump_instruction,
        instruction_to_ignore,
        instruction_to_run,
        HALT_INSTRUCTION
    ]

    vm = VirtualMachine(code_collection=code_collection, stack_size=3)

    vm.run()

    assert vm.stack == [
        condition_instruction["value"],
        instruction_to_run["value"],
        None
    ]

    assert instruction_to_ignore["value"] not in vm.stack


def test_run_jnz_true() -> None:
    """Test the `jnz` instruction handling with the `run` method.

    In this test, assert that the `jnz` method correctly handles `True`
    conditions.
    """

    condition_instruction = {
        "instruction": "IPUSH",
        "id": 1,
        "value": True
    }

    instruction_to_ignore = {
        "instruction": "IPUSH",
        "id": 2,
        "value": 23
    }

    instruction_to_run = {
        "instruction": "IPUSH",
        "id": 3,
        "value": 35
    }

    conditional_jump_instruction = {
        "instruction": "JNZ",
        "id": -1,
        "value": 3
    }

    code_collection = [
        condition_instruction,
        conditional_jump_instruction,
        instruction_to_ignore,
        instruction_to_run,
        HALT_INSTRUCTION
    ]

    vm = VirtualMachine(code_collection=code_collection, stack_size=3)

    vm.run()

    assert vm.stack == [
        condition_instruction["value"],
        instruction_to_run["value"],
        None
    ]

    assert instruction_to_ignore["value"] not in vm.stack


def test_run_jnz_false() -> None:
    """Test the `jnz` instruction handling with the `run` method.

    In this test, assert that the `jnz` method correctly handles `False`
    conditions.
    """

    condition_instruction = {
        "instruction": "IPUSH",
        "id": 1,
        "value": False
    }

    instruction_to_run = {
        "instruction": "IPUSH",
        "id": 2,
        "value": 23
    }

    another_instruction_to_run = {
        "instruction": "IPUSH",
        "id": 3,
        "value": 35
    }

    conditional_jump_instruction = {
        "instruction": "JNZ",
        "id": -1,
        "value": 3
    }

    code_collection = [
        condition_instruction,
        conditional_jump_instruction,
        instruction_to_run,
        another_instruction_to_run,
        HALT_INSTRUCTION
    ]

    vm = VirtualMachine(code_collection=code_collection, stack_size=3)

    vm.run()

    assert vm.stack == [
        condition_instruction["value"],
        instruction_to_run["value"],
        another_instruction_to_run["value"]
    ]


def test_run_empty() -> None:
    """Test the `empty` instruction handling with the `run` method."""

    code_collection = [
        {
            "instruction": "EMPTY",
            "id": 1,
            "value": None
        },
        HALT_INSTRUCTION
    ]

    vm = VirtualMachine(code_collection, stack_size=1)

    vm.run()
    assert vm.stack == [None]

