"""Implement the Abstract Syntax Tree (AST)."""

from src.ast_nodes import *


class AbstractSyntaxTree:
    """
    Abstract Syntax Tree that contains Nodes generated from a source code.

    Parameters
    ----------
    source_code : dict[str, dict]
        A list of tuples created by the `Lexer` that contains the
        representation of the source code in (`symbol`, `value`) format.
    """

    def __init__(self, source_code: dict[str, dict]) -> None:
        self.node_id_manager: int = 1
        self.source_code: dict[str, dict] = source_code
        self.root: PROG = PROG(id=0)

        # Attributes to be used later
        self.current_symbol: str = None
        self.current_value: dict = {}
        self.current_statement_list: list[tuple[str, dict]] = []
        self.current_node: Node = None
        self.current_function_type: str = None

    def build(self) -> PROG:
        """
        Build the Abstract Syntax Tree (AST) from the source code.

        Returns
        -------
        root : PROG
            The root of the built AST.
        """

        # Build the node representations of globals
        self.parse_struct_definitions()
        self.parse_global_variables()

        # Parse each function and add it to the `global` scope
        self.parse_functions()

        return self.root
        
    def parse_struct_definitions(self) -> None:
        """Parse struct definitions and add it to the Abstract Syntax Tree."""

        struct_definitions: dict[str, dict] = (
            self.source_code.get("globals")
                            .get("structs")
        )

        for struct_name, struct_metadata in struct_definitions.items():
            current_id = self._get_next_id()
            struct_metadata["type"] = struct_name

            struct_def_node = STRUCT_DEF(
                id=current_id,
                struct_metadata=struct_metadata
            )

            self.root.add_child(struct_def_node)

    def parse_global_variables(self) -> None:
        """Parse global variables and add it to the Abstract Syntax Tree."""

        global_variables: dict[str, dict] = (
            self.source_code.get("globals")
                            .get("variables")
        )

        for variable_name, variable_metadata in global_variables.items():
            current_id = self._get_next_id()
            variable_metadata["name"] = variable_name

            var_def_node = VAR_DEF(
                id=current_id,
                variable_metadata=variable_metadata
            )

            self.root.add_child(var_def_node)

    def parse_functions(self) -> None:
        """Parse functions and add it to the Abstract Syntax Tree."""

        functions: dict[str, dict] = self.source_code.get("functions")

        for function_name, function_data in functions.items():
            current_id = self._get_next_id()

            # We'll don't want the `statements` field to be passed as it will
            # be parsed just ahead. Thus, we avoid unnecessary duplicate
            # information
            function_metadata = {
                key: value
                for key, value in function_data.items()
                if key != "statements"
            }

            function_def_node = FUNC_DEF(
                id=current_id,
                function_name=function_name,
                function_metadata=function_metadata
            )

            self.current_function_type = function_def_node.get_type()
            self.current_statement_list = function_data.get("statements")

            self._next_symbol()
            function_def_node.set_statements(self._statement())

            self.root.add_child(function_def_node)

    def print_tree(self, indent: int = 0) -> None:
        """
        Recursively print the AST starting from the `root`.

        Parameters
        ----------
        indent : int (optional, default = 0)
            The indentation level for pretty printing. Defaults to 0 for the
            root (and is incremented by 1 for each level).
        """

        self.root.print(indent=indent)

    def get_root(self) -> PROG:
        """
        Get the root of this Abstract Syntax Tree.

        Returns
        -------
        root : PROG
            The root of the tree.
        """

        return self.root

    def _statement(self) -> Node:
        """
        Evaluate a statement and add its nodes to the AST.

        A `statement` is either an expression, a variable definition, a function
        call, a `Conditional` (loops, `if`/`if/else`) or a `return` followed by
        a semicolon.

        Returns
        -------
        : Node
            The parent node of the statement representation.
        """

        statement_handler_map = {
            "FUNC_CALL": self._func_call,
            "RET_SYM": self._ret_sym,
            "VAR_DEF": self._var_def,
            "IF_SYM": self._if_sym,
            "WHILE_SYM": self._while_sym,
            "DO_SYM": self._do_sym,
            "SEMI": self._semi,
            "LCBRA": self._brackets
        }

        handler = statement_handler_map.get(
            self.current_symbol,
            self._handle_eol
        )

        return handler()
    
    def _func_call(self) -> FUNC_CALL:
        """
        Parse a call to a function.

        Returns
        -------
        statement_node : FUNC_CALL
            A Node that represents a call to a function.
        """

        func_call_node_id = self._get_next_id()
        func_call_node = FUNC_CALL(
            id=func_call_node_id,
            function_call_metadata=self.current_value
        )

        self._next_symbol()

        return func_call_node

    def _ret_sym(self) -> RET_SYM:
        """
        Parse the `return` of a function.

        Returns
        -------
        statement_node : RET_SYM
            A Node that represents the `return` statement.
        """

        ret_sym_node_id = self._get_next_id()
        self._next_symbol()

        ret_sym_node = RET_SYM(
            id=ret_sym_node_id,
            returned_value=self._handle_eol(),
            type=self.current_function_type
        )

        return ret_sym_node

    def _var_def(self) -> VAR_DEF:
        """
        Parse a (local) variable definition.

        Returns
        -------
        statement_node : VAR_DEF
            A Node that represents a (local) variable definition.
        """

        var_def_node_id = self._get_next_id()
        var_def_node = VAR_DEF(
            id=var_def_node_id,
            variable_metadata=self.current_value
        )

        self._next_symbol()

        return var_def_node

    def _if_sym(self) -> Conditional:
        """
        Parse an `if` statement: `if <parenthesis_expression> <statement>`

        Returns
        -------
        : Conditional
            A `Conditional` node that is parent of the expression to evaluate,
            and the code to run if `True`. If `IFELSE`, this node is also the
            parent of the code to run if the expression evaulates to `False`.
        """

        conditional_node_id = self._get_next_id()
        self._next_symbol()

        parenthesis_expression = self._parenthesis_expression()
        statement_if_true = self._statement()

        # If the next symbol is `ELSE`, generate an `IFELSE` object instead
        if self.current_symbol == "ELSE_SYM":
            self._next_symbol()

            statement_if_false = self._statement()

            return IFELSE(
                id=conditional_node_id,
                parenthesis_expression=parenthesis_expression,
                statement_if_true=statement_if_true,
                statement_if_false=statement_if_false
            )
    
        return IF(
            id=conditional_node_id,
            parenthesis_expression=parenthesis_expression,
            statement_if_true=statement_if_true
        )
    
    def _while_sym(self) -> Conditional:
        """
        Parse a `while` statement: `while <parenthesis_expression> <statement>`.

        Returns
        -------
        : Conditional
            A `Conditional` node that is parent of the expression to evaluate,
            and the code to run while it is `True`.
        """

        conditional_node_id = self._get_next_id()
        self._next_symbol()

        parenthesis_expression = self._parenthesis_expression()

        loop = self._statement()

        return WHILE(
            id=conditional_node_id,
            parenthesis_expression=parenthesis_expression,
            loop=loop
        )
    
    def _do_sym(self) -> Conditional:
        """
        Parse a `do/while` statement: `do <statement> while <parenthesis_expression> ;`

        Returns
        -------
        : Conditional
            A `Conditional` node that is parent of the expression to evaluate,
            and the code to run while it is `True`. Note that the code to loop
            is executed at least once, even if the `parenthesis_expression`
            always evaluates to `False`.
        """

        conditional_node_id = self._get_next_id()
        self._next_symbol()

        loop = self._statement()

        if self.current_symbol == "WHILE_SYM":
            self._next_symbol()
        else:
            raise SyntaxError("Malformed `do` statement: missing `while`.")
        
        parenthesis_expression = self._parenthesis_expression()

        if self.current_symbol == "SEMI":
            self._next_symbol()
        else:
            raise SyntaxError("Missing semicolon at the end of statement.")
        
        return DO(
            id=conditional_node_id,
            parenthesis_expression=parenthesis_expression,
            loop=loop
        )

    def _semi(self) -> EMPTY:
        """
        Parse the semicolon.
        
        Returns
        -------
        statement_node : EMPTY
            An EMPTY node.
        """

        empty_node_id = self._get_next_id()
        statement_node = EMPTY(id=empty_node_id)

        self._next_symbol()

        return statement_node

    def _brackets(self) -> SEQ:
        """
        Parse a statement embraced by brackets: `{ <statement> }`.

        Returns
        -------
        statement_node : SEQ
            The parent node of a sequence of one or more statements.
        """

        statement_node_id = self._get_next_id()
        statement_node = SEQ(id=statement_node_id)
    
        self._next_symbol()

        while self.current_symbol != "RCBRA":
            temp_node = statement_node

            sequence_node_id = self._get_next_id()
            statement_node = SEQ(id=sequence_node_id)

            # Avoid multiple nested SEQ statements
            both_are_seq = (
                isinstance(temp_node, SEQ) and isinstance(statement_node, SEQ)
            )

            if both_are_seq:
                statement_node.children = [*temp_node.children, *statement_node.children]
            else:
                statement_node.add_child(temp_node)

            child_statement = self._statement()

            # Avoid adding EMPTY nodes to the tree (`self._semi` only exists
            # because removing it breaks a lot of stuff)
            if not isinstance(child_statement, EMPTY):
                statement_node.add_child(child_statement)

        self._next_symbol()

        return statement_node

    def _handle_eol(self) -> Operation:
        """
        Parse an expression terminated by a semicolon: `<expression> ;`

        Returns
        -------
        statement_node : Operation
            The expression itself.
        """

        child_expression = self._expression()

        if self.current_symbol == "SEMI":
            self._next_symbol()
        else:
            raise SyntaxError("Missing semicolon at the end of expression.")

        return child_expression

    def _parenthesis_expression(self) -> Node:
        """
        Parse a `parenthesis_expression`.

        A `parenthesis_expression` is formed by an `expression` embraced by
        parenthesis -- `( <expression> )`.

        Returns
        -------
        parenthesis_expression_node : Node
            The node representation of the parenthesis expression.
        """

        if self.current_symbol == "LPAR":
            self._next_symbol()
            self.current_node = self._parenthesis_expression()
        
        parenthesis_expression_node = self._expression()

        if self.current_symbol == "RPAR":
            self._next_symbol()

        return parenthesis_expression_node

    def _expression(self) -> Operation:
        """
        Evaluate an expression.

        An `expression` is either a `comparison` or the assignment of a
        `variable` to the result of an `expression` -- `<var> = <expression>`.

        Returns
        -------
        expression_node : Operation
            The node representation of the expression.
        """

        if self.current_symbol != "VAR":
            return self._comparison()

        expression_node = self._comparison()

        if isinstance(expression_node, VAR):
            if self.current_symbol == "ASSIGN":
                expression_node = self.__handle_assign(expression_node)

            # Handle access to elements of a struct or an array
            elif self.current_symbol in ["LBRA", "DOT"]:
                variable = expression_node

                element_access_node_id = self._get_next_id()
                self._next_symbol()

                element = self._term()

                expression_node = ELEMENT_ACCESS(
                    id=element_access_node_id,
                    variable=variable,
                    element=element
                )

                if self.current_symbol == "RBRA":
                    self._next_symbol()

                # Finally, handle the `ASSIGN` case (i.e., setting the value of
                # an element in a struct or an array)
                # I'm not proud of this :( but it works :)
                if self.current_symbol == "ASSIGN":
                    expression_node = self.__handle_assign(expression_node)
        
        return expression_node
    
    def __handle_assign(self, expression_node: Node) -> ASSIGN:
        lhs = expression_node

        # Add context to the `VAR` node so it will generate a `ADDRESS`
        # instruction instead of `LOAD`
        if isinstance(lhs, VAR):
            lhs.add_context({"context": "write"})

        assign_node_id = self._get_next_id()
        self._next_symbol()

        rhs = self._expression()

        expression_node = ASSIGN(
            id=assign_node_id,
            lhs=lhs,
            rhs=rhs
        )

        return expression_node

    def _comparison(self) -> Operation:
        """
        Evaluate a comparison.

        A `comparison` is either a `binary_operation` or the comparison between
        two sums -- `<binary_operation> ( < | > | == ) <binary_operation>`.

        Returns
        -------
        comparison_node : Operation
            The node representation of the comparison.
        """

        comparison_node = self._binary_operation()

        while self.current_symbol == "RPAR":
            self._next_symbol()

        comparison_operators: dict[str, Operation] = {
            "EQUAL": EQUAL,
            "GREATER": GREATER,
            "LESS": LESS
        }

        if self.current_symbol in comparison_operators:
            _comparison_class = comparison_operators[self.current_symbol]
            comparison_node_id = self._get_next_id()

            left_operand = comparison_node

            self._next_symbol()

            right_operand = self._binary_operation()

            comparison_node = _comparison_class(
                id=comparison_node_id,
                lhs=left_operand,
                rhs=right_operand
            )

        return comparison_node

    def _binary_operation(self) -> Operation:
        """
        Evaluate a binary operation.

        Returns
        -------
        binary_operation_node : Operation
            The node representation of the binary operation.

        Notes
        -----
        The currently supported binary operations are:
            - addition (+)
            - subtraction (-)
            - multiplication (*)
            - division (/)
            - left bitshift (<<)
            - right bitshift (>>)
            - logical and (&&)
            - logical or (||)
            - bitwise and (&)
            - bitwise or (|)
        """

        if self.current_node:
            term_node = self.current_node
            self.current_node = None
        else:
            term_node = self._term()

        binary_operation_node = term_node

        binary_operations: dict[str, Operation] = {
            "ADD": ADD,
            "SUB": SUB,
            "MULT": MULT,
            "DIV": DIV,
            "LSHIFT": LSHIFT,
            "RSHIFT": RSHIFT,
            "AND": AND,
            "OR": OR,
            "BITAND": BITAND,
            "BITOR": BITOR
        }

        while self.current_symbol in binary_operations:
            left_operand = binary_operation_node

            binary_operation_node_class = binary_operations[self.current_symbol]
            binary_operation_node_id = self._get_next_id()

            self._next_symbol()

            right_operand = self._term()

            binary_operation_node = binary_operation_node_class(
                id=binary_operation_node_id,
                lhs=left_operand,
                rhs=right_operand
            )

        return binary_operation_node

    def _term(self) -> Node:
        """
        Evaluate a term.

        A term is either a variable -- `<var>` --, a constant -- `<cst>` --, or
        a parenthesis expression.

        Returns
        -------
        term_node : Node
            The node representation of the term.
        """

        terms_map = {
            "CST": CST,
            "FUNC_CALL": FUNC_CALL,
            "VAR": VAR
        }

        if self.current_symbol in terms_map:
            term_handler = terms_map.get(self.current_symbol)

            term_node_id = self._get_next_id()
            term_node = term_handler(
                term_node_id,
                self.current_value
            )

        else:
            return self._parenthesis_expression()
        
        self._next_symbol()

        return term_node

    def _next_symbol(self) -> None:
        """Get the next symbol to evaluate."""

        if len(self.current_statement_list) > 0:
            self.current_symbol, self.current_value = self.current_statement_list.pop(0)
        else:
            self.current_symbol, self.current_value = ("EOI", {})

    def _get_next_id(self) -> int:
        """
        Get the ID to use in the next Node to be created.

        This function centralizes the management of the `node_id_manager`
        property.

        Returns
        -------
        next_id : int
            The ID to use.
        """

        next_id = self.node_id_manager
        self.node_id_manager += 1

        return next_id
