"""Implement unit tests for the `src.certificators.backend` module."""

from src.certificators import BackendCertificator
from tests.unit.common import CERTIFICATE, MACHINE_CODE


def test_init() -> None:
    """Test the instantiation of BackendCertificator objects."""

    backend_certificator = BackendCertificator(program=MACHINE_CODE)

    assert backend_certificator.computed_certificate == []
    assert backend_certificator.initial_prime == 2
    assert backend_certificator.program == MACHINE_CODE
    assert backend_certificator.environment == {
        '0x28': {'prime': 2},
        '0x30': {'prime': 3},
        '0x34': {'prime': 5},
        '0x38': {'prime': 7},
        '0x3c': {'prime': 11},
        '0x40': {'prime': 13},
        '0x4c': {'prime': 17},
        '0x50': {'prime': 19},
        '0x58': {'prime': 23},
        '0x60': {'prime': 29},
        '0x64': {'prime': 31},
        '0x8c': {'prime': 37}
    }
    assert backend_certificator.current_positional_prime == 2
    assert backend_certificator.current_variable_prime == 2


# def test_certificate():
#     """Test the BackendCertificator.certificate method."""

#     backend_certificator = BackendCertificator(program=MACHINE_CODE)
#     backend_certificator.certificate()

#     assert backend_certificator.get_certificate() == CERTIFICATE
