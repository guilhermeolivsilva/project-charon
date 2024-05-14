"""Certificator for the frontend representation of Tiny C programs."""

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.node import Node

from src.certificators.interface import Interface
from src.utils import next_prime


class FrontendCertificator(Interface):
    """
    Certificate the frontend representation of some program.

    Parameters
    ----------
    ast : AbstractSyntaxTree
        The AST of the program to certificate.
    """

    symbols = [
        *Interface.basic_symbols,
        *AbstractSyntaxTree.node_kinds,
    ]

    def __init__(self, ast: AbstractSyntaxTree) -> None:
        self.ast = ast

        self.tokens = {
            key: value
            for key, value in zip(
                self.symbols,
                range(1, len(self.symbols) + 1)
            )
        }

    def certificate(self, **kwargs) -> None:
        """
        Certificate the frontend code.
        
        This method traverses the AST and annotate each node with its relative
        position and contents.
        """

        # Using a list to avoid issues with variable scoping in nested function
        base = [1]

        def traverse(node: Node) -> None:
            if node is None:
                return
            
            # TODO: implement custom traversal modes for each `node.kind`,
            # and invoke here with node.traverse_children (or something like
            # this). This new traversal method should be used in the Code
            # Generator, too!
            elif node.kind in ["IF", "IFELSE"]:
                traverse(node.children[0])

                base[0] = next_prime(base[0])
                exponent = self._get_frontend_exponent(node)

                certificate_label = f"{base[0]}^{exponent}"

                node.set_certificate_label(certificate_label)

                for child in node.children[1:]:
                    traverse(child)

                return
            
            elif node.kind == "SEQ":
                base[0] = next_prime(base[0])
                exponent = self._get_frontend_exponent(node)

                certificate_label = f"{base[0]}^{exponent}"

                node.set_certificate_label(certificate_label)

                for child in node.children:
                    traverse(child)

                return

            for child in node.children:
                traverse(child)

            base[0] = next_prime(base[0])
            exponent = self._get_frontend_exponent(node)

            certificate_label = f"{base[0]}^{exponent}"

            node.set_certificate_label(certificate_label)

        traverse(self.ast.root)

    def get_certificate(self) -> list[str]:
        """
        Get the complete certificate of the frontend code.

        Returns
        -------
        : list[str]
            The string representation that concatenates all of the certification
            labels of the AST Nodes.
        """

        # Using a list to avoid issues with variable scoping in nested function
        certificate = []

        def traverse(node: Node) -> None:
            if node is None:
                return
            
            # TODO: implement custom traversal modes for each `node.kind`,
            # and invoke here with node.traverse_children (or something like
            # this). This new traversal method should be used in the Code
            # Generator, too!
            elif node.kind in ["IF", "IFELSE"]:
                traverse(node.children[0])

                certificate.append(f"({node.certificate_label})")

                for child in node.children[1:]:
                    traverse(child)

                return
            
            elif node.kind == "SEQ":
                certificate.append(f"({node.certificate_label})")

                for child in node.children:
                    traverse(child)

                return

            for child in node.children:
                traverse(child)

            certificate.append(f"({node.certificate_label})")

        traverse(self.ast.root)

        return certificate

    def _get_frontend_exponent(self, node: Node) -> str:
        """
        Compute the exponent to label the given `node`.

        Parameters
        ----------
        node : Node
            The AST node to compute its associated exponent.

        Returns
        -------
        : str
            The unique exponent to label the `node`.
        """

        node_handlers = {
            "VAR": self._get_value_exponent,
            "CST": self._get_value_exponent,
            "ADD": self._get_keyword_exponent,
            "SUB": self._get_keyword_exponent,
            "LT": self._get_keyword_exponent,
            "EXPR": self._get_keyword_exponent,
            "PROG": self._get_keyword_exponent,
            "EMPTY": self._get_empty_exponent,
            "SET": self._get_set_exponent,
            "IF": self._get_keyword_exponent,
            "IFELSE": self._get_keyword_exponent,
            "WHILE": self._get_keyword_exponent,
            "DO": self._get_keyword_exponent,
            "SEQ": self._get_empty_exponent,
        }

        handler = node_handlers.get(node.kind)

        return handler(node=node)
    
    def _get_value_exponent(self, node: Node) -> str:
        """
        Parse a VAR or CST Node.

        Parameters
        ----------
        node : Node
            The Node to compute the exponent for.

        Returns
        -------
        : str
            The exponent associated to the `node`.
        """

        # TODO: parse integers digit by digit

        return self.tokens.get(str(node.value))

    def _get_keyword_exponent(self, node: Node) -> str:
        """
        Parse a keyword Node.

        A keyword Node is a node whose `kind` is Tiny C reserved word or an
        operator (+, -, <).

        Parameters
        ----------
        node : Node
            The Node to compute the exponent for.

        Returns
        -------
        : str
            The exponent associated to the `node`.
        """

        return self.tokens.get(node.kind)

    def _get_set_exponent(self, node: Node) -> str:
        """
        Parse a SET Node.

        Parameters
        ----------
        node : Node
            The Node to compute the exponent for.

        Returns
        -------
        : str
            The exponent associated to the `node`.
        """

        exponent = (
            100 * self.tokens.get(node.kind) +
            self.tokens.get(node.value)
        )

        return str(exponent)
    
    def _get_empty_exponent(self, node: Node) -> str:

        return self.tokens.get("EMPTY")
