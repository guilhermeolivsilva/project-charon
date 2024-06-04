"""Implement unit tests for the `src.certificators.frontend` module."""

from copy import deepcopy

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.certificators import FrontendCertificator

SOURCE_CODE = [
    ("LCBRA", None),
    ("ID", "a"),
    ("EQUAL", None),
    ("INT", 5),
    ("SEMI", None),
    ("ID", "b"),
    ("EQUAL", None),
    ("ID", "a"),
    ("MINUS", None),
    ("INT", 1),
    ("SEMI", None),
    ("DO_SYM", None),
    ("LCBRA", None),
    ("ID", "c"),
    ("EQUAL", None),
    ("ID", "a"),
    ("MINUS", None),
    ("ID", "b"),
    ("SEMI", None),
    ("ID", "b"),
    ("EQUAL", None),
    ("ID", "b"),
    ("PLUS", None),
    ("INT", 1),
    ("SEMI", None),
    ("IF_SYM", None),
    ("LPAR", None),
    ("ID", "a"),
    ("LESS", None),
    ("ID", "c"),
    ("RPAR", None),
    ("LCBRA", None),
    ("ID", "d"),
    ("EQUAL", None),
    ("INT", 10),
    ("SEMI", None),
    ("RCBRA", None),
    ("ELSE_SYM", None),
    ("LCBRA", None),
    ("ID", "d"),
    ("EQUAL", None),
    ("INT", 0),
    ("SEMI", None),
    ("RCBRA", None),
    ("RCBRA", None),
    ("WHILE_SYM", None),
    ("LPAR", None),
    ("ID", "b"),
    ("LESS", None),
    ("ID", "a"),
    ("RPAR", None),
    ("SEMI", None),
    ("RCBRA", None)
]

EXPECTED_CERTIFICATE = [
    '1^(27)',
    '2^(29^5)',
    '3^(30^1)',
    '5^(31)',
    '7^(28^1)',
    '11^(29^1)',
    '13^(33)',
    '17^(30^2)',
    '19^(31)',
    '23^(27)',
    '29^(28^1)',
    '31^(28^2)',
    '37^(33)',
    '41^(30^3)',
    '43^(31)',
    '47^(28^2)',
    '53^(29^1)',
    '59^(32)',
    '61^(30^2)',
    '67^(31)',
    '71^(28^1)',
    '73^(28^3)',
    '79^(34)',
    '83^(37)',
    '89^(27)',
    '97^(29^10)',
    '101^(30^4)',
    '103^(31)',
    '107^(27)',
    '109^(29^0)',
    '113^(30^4)',
    '127^(31)',
    '131^(28^2)',
    '137^(28^1)',
    '139^(34)',
    '149^(39)',
    '151^(35)'
]


def test_init() -> None:
    """Test the instantiation of FrontendCertificator objects."""

    ast = AbstractSyntaxTree([])
    frontend_certificator = FrontendCertificator(ast)

    assert frontend_certificator.ast == ast
    assert frontend_certificator.computed_certificate == []


def test_certificate():
    """Test the FrontendCertificator.certificate method."""

    ast = AbstractSyntaxTree(source_code=deepcopy(SOURCE_CODE))
    ast.build()

    frontend_certificator = FrontendCertificator(ast=ast)
    frontend_certificator.certificate()

    assert frontend_certificator.computed_certificate == EXPECTED_CERTIFICATE


def test_get_certificate():
    """Test the FrontendCertificator.get_certificate method."""

    ast = AbstractSyntaxTree(source_code=deepcopy(SOURCE_CODE))
    ast.build()

    frontend_certificator = FrontendCertificator(ast=ast)
    frontend_certificator.certificate()

    assert frontend_certificator.get_certificate() == EXPECTED_CERTIFICATE
