"""Integration test for the a program with tampered compilation."""

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.code_generator import CodeGenerator
from src.lexer import Lexer
from src.virtual_machine import VirtualMachine

from src.certificators import FrontendCertificator, BackendCertificator


def test_code_injection():
    """Test the code injection scenario."""

    ...
