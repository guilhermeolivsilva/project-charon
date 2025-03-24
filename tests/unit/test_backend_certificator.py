"""Implement unit tests for the `src.certificators.backend` module."""

from src.certificators import BackendCertificator
from tests.unit.common import CERTIFICATE, MACHINE_CODE


def test_init() -> None:
    """Test the instantiation of BackendCertificator objects."""

    backend_certificator = BackendCertificator(program=MACHINE_CODE)

    assert backend_certificator.computed_certificate == []
    assert backend_certificator.initial_prime == 2
    assert backend_certificator.program == MACHINE_CODE
    assert backend_certificator.register_tracker == {}
    assert backend_certificator.variable_prime_tracker == {}
    assert backend_certificator.current_positional_prime == 2
    assert backend_certificator.current_variable_prime == 2


# def test_certificate():
#     """Test the BackendCertificator.certificate method."""

#     backend_certificator = BackendCertificator(program=MACHINE_CODE)
#     backend_certificator.certificate()

#     assert backend_certificator.get_certificate() == CERTIFICATE
