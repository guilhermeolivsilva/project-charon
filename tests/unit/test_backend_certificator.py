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
       "functions": {
           1: {"prime": 2},
           2: {"prime": 3},
           3: {"prime": 5},
           4: {"prime": 7}
        },
        "variables": {
            "0x28": {"addresses": {"0x28": "int"}, "prime": 2},
            "0x30": {"addresses": {"0x30": "int"}, "prime": 3},
            "0x34": {"addresses": {"0x34": "int"}, "prime": 5},
            "0x38": {"addresses": {"0x38": "int"}, "prime": 7},
            "0x3c": {"addresses": {"0x3c": "float"}, "prime": 11},
            "0x40": {"addresses": {"0x40": "int"}, "prime": 13},
            "0x4c": {"addresses": {"0x4c": "int"}, "prime": 17},
            "0x50": {"addresses": {"0x50": "float"}, "prime": 19},
            "0x58": {"addresses": {"0x58": "int"}, "prime": 23},
            "0x60": {"addresses": {"0x60": "int"}, "prime": 29},
            "0x64": {"addresses": {"0x78": "int"}, "prime": 31},
            "0x8c": {"addresses": {"0x8c": "int"}, "prime": 37}
        }
    }


# def test_certificate():
#     """Test the BackendCertificator.certificate method."""

#     backend_certificator = BackendCertificator(program=MACHINE_CODE)
#     backend_certificator.certificate()

#     assert backend_certificator.get_certificate() == CERTIFICATE
