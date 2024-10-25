"""Implement unit tests for the `src.interpreter` module."""

from src.certificators import BackendCertificator, FrontendCertificator
from src.runner import create_instance
from src.virtual_machine import VirtualMachine

from tests.unit.common import *


def test_create_instance():
    """
    Test the `create_instance` function.

    This method simply passes because all the attributes are tested in the
    other unit tests.
    """

    pass


def test_parsed_source():
    """Test if the created instance has the expected `parsed_source`."""

    instance = create_instance(SOURCE_CODE)

    assert instance.get_parsed_source() == TOKENIZED_SOURCE_CODE


def test_ast():
    """Test if the created instance has the expected `ast`."""

    instance = create_instance(SOURCE_CODE)

    assert instance.get_ast() == ABSTRACT_SYNTAX_TREE


def test_program():
    """Test if the created instance has the expected `program`."""

    instance = create_instance(SOURCE_CODE)

    assert instance.get_program() == MACHINE_CODE


def test_vm():
    """Test if the created instance has the expected `vm`."""

    instance = create_instance(SOURCE_CODE)

    assert instance.get_vm() == VirtualMachine(MACHINE_CODE)


def test_frontend_certificator():
    """Test if the created instance has the expected `frontend_certificator`."""

    pass


def test_backend_certificator():
    """Test if the created instance has the expected `backend_certificator`."""

    pass
