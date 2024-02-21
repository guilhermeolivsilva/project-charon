"""Implement unit tests for the `src.virtual_machine.VirtualMachine` class."""

# Just to annotate functions with fixtures.
from pytest_mock.plugin import MockerFixture

from src.node import Node
from src.virtual_machine import VirtualMachine


def test_init() -> None:
    """Test the instantiation of VirtualMachine objects."""

    code_collection = [("IFETCH", Node(id=1, kind="VAR", value=0))]
    stack_size = 10

    vm = VirtualMachine(code_collection=code_collection, stack_size=stack_size)

    assert len(vm.variables) == 26
    assert len(vm.stack) == stack_size
    assert not any(vm.stack)
    assert all(code in vm.code_collection for code in code_collection)
    assert ("HALT", None) in vm.code_collection
    assert vm.stack_pointer == vm.program_counter == 0


def test_run() -> None:
    """Test the `VirtualMachine.run` method."""

    ...


def test_run_ifetch(mocker: MockerFixture) -> None:
    """Test `VirtualMachine.ifetch` through the `run` method."""

    test_value = 23
    test_node = Node(id=1, kind="VAR", value=0)

    vm = VirtualMachine(
        code_collection=[("IFETCH", test_node)],
        stack_size=1
    )
    vm.variables[0] = test_value

    vm.ifetch = mocker.spy(vm, "ifetch")
    vm.run()

    # Assert the method was called and the stack has the expected value
    vm.ifetch.assert_called_once_with(test_node)
    assert vm.stack == [test_value]


def test_run_istore(mocker: MockerFixture) -> None:
    """Test `VirtualMachine.istore` through the `run` method."""

    test_value = 23
    test_node = Node(id=1, kind="CST", value=0)

    vm = VirtualMachine(
        code_collection=[("ISTORE", test_node)],
        stack_size=1
    )

    vm.stack = [test_value]
    vm.istore = mocker.spy(vm, "istore")
    vm.run()

    # Assert the method was called and the stack has the expected value
    vm.istore.assert_called_once_with(test_node)
    assert vm.variables[0] == test_value
