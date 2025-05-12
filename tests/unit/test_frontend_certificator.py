"""Implement unit tests for the `src.certificators.frontend` module."""

from src.certificators import FrontendCertificator
from tests.unit.common import ABSTRACT_SYNTAX_TREE, CERTIFICATE


def test_init() -> None:
    """Test the instantiation of FrontendCertificator objects."""

    frontend_certificator = FrontendCertificator(ast=ABSTRACT_SYNTAX_TREE)

    assert frontend_certificator.computed_certificate == []
    assert frontend_certificator.current_prime == 2
    assert frontend_certificator.ast == ABSTRACT_SYNTAX_TREE


# def test_certificate():
#     """Test the FrontendCertificator.certificate method."""

#     frontend_certificator = FrontendCertificator(ast=ABSTRACT_SYNTAX_TREE)
#     frontend_certificator.certificate()

#     assert frontend_certificator.get_certificate() == CERTIFICATE
