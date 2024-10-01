"""Implement unit tests for the `src.interpreter` module."""

from src.runner import create_instance
from src.virtual_machine import VirtualMachine
from tests.unit.common import MACHINE_CODE, SOURCE_CODE


def test_create_instance():
    """Test the `create_instance` function."""

    instance = create_instance(SOURCE_CODE)

    generated_vm = instance["vm"]
    expected_vm = VirtualMachine(MACHINE_CODE)

    assert generated_vm == expected_vm
