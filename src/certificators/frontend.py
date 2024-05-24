"""Certificator for the frontend representation of Tiny C programs."""

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.certificators.interface import Interface


class FrontendCertificator(Interface):
    """
    Certificate the frontend representation of some program.

    Parameters
    ----------
    ast : AbstractSyntaxTree
        The AST of the program to certificate.
    """

    def __init__(self, ast: AbstractSyntaxTree) -> None:
        super().__init__()
        self.ast: AbstractSyntaxTree = ast

    def certificate(self, **kwargs) -> None:
        """
        Certificate the frontend code.
        
        This method traverses the AST and annotate each node with its relative
        position and contents.
        """

        self.ast.root.certificate(prime=1)

    def get_certificate(self) -> list[str]:
        """
        Get the complete certificate of the frontend code.

        Returns
        -------
        : list[str]
            A list of containing all of the certification labels of the AST
            Nodes.
        """

        if not self.computed_certificate:
            self.computed_certificate = self.ast.root.get_certificate_label()

        return self.computed_certificate
