"""Certificator for the frontend representation of Tiny C programs."""

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.node import Node

from src.certificators.interface import Interface
from src.certificators.utils import next_prime


class FrontendCertificator(Interface):

    symbols = [
        *Interface.basic_symbols,
        *AbstractSyntaxTree.node_kinds,
    ]

    def __init__(self, ast: AbstractSyntaxTree, prunes: list[str] = []) -> None:
        self.ast = ast
        self.prunes = prunes

        self.tokens = {
            key: value
            for key, value in zip(
                self.symbols,
                range(1, len(self.symbols) + 1)
            )
        }

    def prune_ast(self) -> None:
        """Prune the AST by merging redundant Nodes."""

        enabled_prunes = [
            self.__getattribute__(prune)
            for prune in self.prunes
        ]

        for prune in enabled_prunes:
            self.prune(self.ast.root, prune)

    def prune(
        self, node: Node, _prune: callable
    ) -> None:
        """
        Apply a pruning method to the AST in recursive, inorder DFS fashion.

        Parameters
        ----------
        node : Node
            The current Node.
        _prune : callable
            The prune method to employ.
        """

        _prune(node)

        for child in node.children:
            self.prune(child, _prune)

    def _merge_seq_empty(self, node: Node) -> None:
        """
        Merge SEQ Nodes to EMPTY Nodes.

        This method only merges nodes if the EMPTY Node is the child of the
        SEQ Node. The SEQ Node is kept, while the EMPTY is removed from the
        tree.

        Parameters
        ----------
        node : Node
            The Node currently being evaluated.
        """

        if node.kind != "SEQ":
            return

        for child in node.children:
            if child.kind == "EMPTY":
                node.merge(child)

    def _merge_set_var(self, node: Node) -> None:
        """
        Merge SET Nodes to VAR Nodes.

        This method simplifies the value attribution operation by adding the
        target variable (left hand side of the `=` operator) to the SET Node
        itself.

        Parameters
        ----------
        node : Node
            The Node currently being evaluated.
        """

        if node.kind != "SET":
            return

        for child in node.children:
            if child.kind == "VAR":
                node.merge(child, {"absorb_value": True})

    def certificate(self) -> None:
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

    def get_certificate(self) -> str:

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

        return "*".join(certificate)

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
            "EMPTY": self._get_keyword_exponent,
            "SET": self._get_set_exponent,
            "IF": self._get_keyword_exponent,
            "IFELSE": self._get_keyword_exponent,
            "WHILE": self._get_keyword_exponent,
            "DO": self._get_keyword_exponent,
            "SEQ": self._get_keyword_exponent,
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
