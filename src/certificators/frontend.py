"""Certificator for the frontend representation of Tiny C programs."""

from typing_extensions import override

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.ast_nodes.variables.STRUCT_DEF import STRUCT_DEF
from src.ast_nodes.certificate_mapping import TYPE_SYMBOLS_MAP
from src.certificators.abstract_certificator import AbstractCertificator


class FrontendCertificator(AbstractCertificator):
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

    @override
    def certificate(self, **kwargs) -> list[str]:
        """
        Certificate the frontend code.
        
        This method traverses the AST and annotate each node with its relative
        position and contents.

        Returns
        -------
        computed_certificate : list[str]
            The list of labels that compose the computed certificate.
        """

        ast_certificate = self._certificate_ast()
        types_symbols = self._compute_types_symbols()

        self.computed_certificate = self._certificate_types(
            ast_certificate=ast_certificate,
            types_symbols=types_symbols
        )

        return self.computed_certificate

    def _certificate_ast(self) -> list[str]:
        """
        Certificate the Abstract Syntax Tree.

        Notice that the certificate generated by this method is incomplete: it
        lacks symbols for the types.

        Returns
        -------
        ast_certificate : list[str]
            The list of labels of the AST certificate.
        """

        _ = self.ast.root.certificate(prime=2)
        ast_certificate = self.ast.root.get_certificate_label()

        return ast_certificate
    
    def _compute_types_symbols(self) -> dict[str, str]:
        """
        Compute the symbols the user-defined types (i.e., structs).

        Returns
        -------
        types_symbols : dict[str, str]
            A (type, symbol) mapping.
        """

        built_in_types_symbols = {
            key: value["type_symbol"]
            for key, value in TYPE_SYMBOLS_MAP.items()
        }
        struct_types_symbols: dict[str, str] = {}

        struct_def_nodes: list[STRUCT_DEF] = [
            node for node in self.ast.root.children
            if isinstance(node, STRUCT_DEF) and node.is_active()
        ]

        for struct_def in struct_def_nodes:
            struct_type = struct_def.get_type()
            struct_symbol = struct_def.get_symbol()

            struct_types_symbols[struct_type] = struct_symbol

        types_symbols: dict[str, str] = {
            **built_in_types_symbols,
            **struct_types_symbols
        }

        return types_symbols
    
    def _certificate_types(
        self,
        ast_certificate: list[str],
        types_symbols: dict[str, str]
    ) -> list[str]:
        """
        Certificate the types from labels in an AST certificate list.

        Parameters
        ----------
        ast_certificate : list[str]
            The "raw" certificate of an AST.
        types_symbols : dict[str, str]
            A (type, symbol) mapping.

        Returns
        -------
        type_certificated_labels : list[str]
            The certificate with certificated labels.
        """

        type_certificated_labels: list[str] = []

        for label in ast_certificate:
            parsed_label = label

            # Extract the placeholder and replace it with the type symbol
            if "_certificate" in label:
                label_to_parse = "".join(
                    reversed(label[:label.index("_certificate")])
                )
                idx = 0

                # This is a trick! All placeholders are within parenthesis. So,
                # we only have to iterate until we find the opening one!
                type_name = ""
                while label_to_parse[idx] != "(":
                    type_name = label_to_parse[idx] + type_name
                    idx += 1

                type_symbol = types_symbols[type_name]
                parsed_label = label.replace(
                    type_name + "_certificate",
                    str(type_symbol)
                )

            type_certificated_labels.append(parsed_label)

        return type_certificated_labels
