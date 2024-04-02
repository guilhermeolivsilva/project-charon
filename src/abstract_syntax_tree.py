"""Implement the Abstract Syntax Tree (AST)."""

from typing import Generator, Union

from src.node import Node


class AbstractSyntaxTree:
    """
    Abstract Syntax Tree that contains Nodes generated from a source code.

    Parameters
    ----------
    source_code : Generator
        A Generator created by the `Lexer` that contains the representation of
        the source code in (`symbol`, `value`) format.
    """

    node_kinds = [
        "VAR",
        "CST",
        "SET",
        "EXPR",
        "ADD",
        "SUB",
        "LT",
        "PROG",
        "IF",
        "IFELSE",
        "WHILE",
        "DO",
        "SEQ",
        "EMPTY"
    ]

    def __init__(self, source_code: Generator) -> None:
        self.node_id_manager: int = 1
        self.source_code = list(source_code)
        self.current_symbol = None
        self.current_value = None
        self.root = Node(id=0, kind="PROG")

    def build(self) -> None:
        """Build the Abstract Syntax Tree from the source code."""

        self._next_symbol()
        program_node = self._statement()
        
        self.root.add_child(program_node)
        program_node.add_parent(self.root)

        if self.current_symbol != "EOI":
            raise SyntaxError("Source code does not have EOI identifier.")

    def _statement(self) -> Node:
        """
        Evaluate a statement and add its nodes to the AST.

        A `statement` is either a `if`, `if/else`, `while`, `do/while` or
        an `expression` followed by a semicolon.

        Returns
        -------
        : Node
            The parent node of the statement representation.
        """

        statement_handler_map = {
            "IF_SYM": self._if_sym,
            "WHILE_SYM": self._while_sym,
            "DO_SYM": self._do_sym,
            "SEMI": self._semi,
            "LBRA": self._brackets
        }

        handler = statement_handler_map.get(
            self.current_symbol,
            self._handle_eol
        )

        return handler()

    def _if_sym(self) -> Node:
        """
        Parse an `if` statement: `if <parenthesis_expression> <statement>`

        Returns
        -------
        statement_node : Node
            The parent node of the statement representation.
        """

        statement_node = self._create_node(kind="IF")

        self._next_symbol()

        parenthesis_expression = self._parenthesis_expression()
        if_statement = self._statement()

        parenthesis_expression.add_parent(statement_node)
        statement_node.add_child(parenthesis_expression)

        if_statement.add_parent(statement_node)
        statement_node.add_child(if_statement)

        # Add the `else` clause to the `if`: `else <statement>`
        if self.current_symbol == "ELSE_SYM":
            statement_node.set_kind("IFELSE")

            self._next_symbol()

            else_statement = self._statement()

            else_statement.add_parent(statement_node)
            statement_node.add_child(else_statement)

        return statement_node
    
    def _while_sym(self) -> Node:
        """
        Parse a `while` statement: `while <parenthesis_expression> <statement>`.

        Returns
        -------
        statement_node : Node
            The parent node of the statement representation.
        """

        statement_node = self._create_node(kind="WHILE")

        self._next_symbol()

        parenthesis_expression = self._parenthesis_expression()
        while_statement = self._statement()

        parenthesis_expression.add_parent(statement_node)
        statement_node.add_child(parenthesis_expression)

        while_statement.add_parent(statement_node)
        statement_node.add_child(while_statement)

        return statement_node
    
    def _do_sym(self) -> Node:
        """
        Parse a `do/while` statement: `do <statement> while <parenthesis_expression> ;`
        Returns
        -------
        statement_node : Node
            The parent node of the statement representation.
        """

        statement_node = self._create_node(kind="DO")

        self._next_symbol()

        do_statement = self._statement()

        do_statement.add_parent(statement_node)
        statement_node.add_child(do_statement)

        if self.current_symbol == "WHILE_SYM":
            self._next_symbol()
        else:
            raise SyntaxError("Malformed `do` statement: missing `while`.")
        
        parenthesis_expression = self._parenthesis_expression()
        parenthesis_expression.add_parent(statement_node)
        statement_node.add_child(parenthesis_expression)

        if self.current_symbol == "SEMI":
            self._next_symbol()
        else:
            raise SyntaxError("Missing semicolon at the end of statement.")
        
        return statement_node
    
    def _semi(self) -> Node:
        """
        Parse the semicolon.
        
        Returns
        -------
        statement_node : Node
            The parent node of the statement representation.
        """

        statement_node = self._create_node(kind="EMPTY")
        self._next_symbol()

        return statement_node
    
    def _brackets(self) -> Node:
        """
        Parse a statement embraced by brackets: `{ <statement> }`.

        Returns
        -------
        statement_node : Node
            The parent node of the statement representation.
        """

        statement_node = self._create_node(kind="EMPTY")
    
        self._next_symbol()

        while self.current_symbol != "RBRA":
            temp_node = statement_node
            statement_node = self._create_node(kind="SEQ")

            temp_node.add_parent(statement_node)
            statement_node.add_child(temp_node)

            child_statement = self._statement()

            child_statement.add_parent(statement_node)
            statement_node.add_child(child_statement)

        self._next_symbol()

        return statement_node
        
    def _handle_eol(self) -> Node:
        """
        Parse an expression terminated by a semicolon: `<expression> ;`

        Returns
        -------
        statement_node : Node
            The parent node of the statement representation.
        """

        statement_node = self._create_node(kind="EXPR")
        expression = self._expression()

        expression.add_parent(statement_node)
        statement_node.add_child(expression)

        if self.current_symbol == "SEMI":
            self._next_symbol()
        else:
            raise SyntaxError("Missing semicolon at the end of expression.")

        return statement_node

    def _parenthesis_expression(self) -> Node:
        """
        Evaluate a parenthesis expression.

        A `parenthesis_expression` is formed by an `expression` embraced by
        parenthesis -- `( <expression> )`.

        Returns
        -------
        parenthesis_expression_node : Node
            The node representation of the parenthesis expression.
        """

        if self.current_symbol == "LPAR":
            self._next_symbol()
        else:
            raise SyntaxError("Missing left parenthesis in parenthesis_expression.")
        
        parenthesis_expression_node = self._expression()

        if self.current_symbol == "RPAR":
            self._next_symbol()
        else:
            raise SyntaxError("Missing right parenthesis in parenthesis_expression.")
        
        return parenthesis_expression_node

    def _expression(self) -> Node:
        """
        Evaluate an expression.

        An `expression` is either a `comparison` or the assignment of a
        `variable` to the result of an `expression` -- `<id> = <expression>`.

        Returns
        -------
        expression_node : Node
            The node representation of the expression.
        """
        
        if self.current_symbol != "ID":
            return self._comparison()

        expression_node = self._comparison()

        if expression_node.get_kind() == "VAR" and self.current_symbol == "EQUAL":
            variable = expression_node

            expression_node = self._create_node(kind="SET")

            self._next_symbol()

            variable.add_parent(expression_node)
            expression_node.add_child(variable)

            child_expression = self._expression()

            child_expression.add_parent(expression_node)
            expression_node.add_child(child_expression)
        
        return expression_node

    def _comparison(self) -> Node:
        """
        Evaluate a comparison.

        A `comparison` is either a `sum` or the comparison between two sums
        -- `<sum> < <sum>`.

        Returns
        -------
        comparison_node : Node
            The node representation of the comparison.
        """
        
        comparison_node = self._sum()

        if self.current_symbol == "LESS":
            left_operand = comparison_node

            comparison_node = self._create_node(kind="LT")

            self._next_symbol()

            left_operand.add_parent(comparison_node)
            comparison_node.add_child(left_operand)

            right_operand = self._sum()

            right_operand.add_parent(comparison_node)
            comparison_node.add_child(right_operand)

        return comparison_node

    def _sum(self) -> Node:
        """
        Evaluate a sum.

        A `sum` is either a `term`, the addition of two terms --
        `<term> + <term>` --, or the subtraction of two terms --
        `<term> - <term>`.

        Returns
        -------
        sum_node : Node
            The node representation of the sum.
        """

        term_node = self._term()
        sum_node = term_node

        while self.current_symbol in ["PLUS", "MINUS"]:
            left_operand = sum_node

            _node_kind = "ADD" if self.current_symbol == "PLUS" else "SUB"
            sum_node = self._create_node(kind=_node_kind)

            self._next_symbol()

            left_operand.add_parent(sum_node)
            sum_node.add_child(left_operand)

            other_term = self._term()

            other_term.add_parent(sum_node)
            sum_node.add_child(other_term)

        return sum_node

    def _term(self) -> Node:
        """
        Evaluate a term.

        A term is either a variable -- `<id>` --, an integer -- `<int>` --, or
        a parenthesis expression.

        Returns
        -------
        term_node : Node
            The node representation of the term.
        """

        if self.current_symbol in ["ID", "INT"]:
            _node_kind = "VAR" if self.current_symbol == "ID" else "CST"
            term_node = self._create_node(
                kind=_node_kind,
                value=self.current_value
            )

            self._next_symbol()

        else:
            term_node = self._parenthesis_expression()

        return term_node

    def _next_symbol(self) -> None:
        """Get the next symbol to evaluate."""

        if len(self.source_code) > 0:
            self.current_symbol, self.current_value = self.source_code.pop(0)
        else:
            self.current_symbol, self.current_value = ("EOI", None)

    def _create_node(self, kind: str, value: Union[None, int] = None) -> Node:
        
        new_node = Node(id=self.node_id_manager, kind=kind, value=value)
        self.node_id_manager += 1

        return new_node
