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
        self.source_code: dict[str, dict] = source_code
        self.root: PROG = PROG()

        # Attributes to be used later
        self.current_symbol: str = None
        self.current_value: dict = {}
        self.current_statement_list: list[tuple[str, dict]] = []
        self.current_function_type: str = None

    def __eq__(self, other: "AbstractSyntaxTree") -> bool:
        """
        Implement the equality comparison between AST objects.

        Parameters
        ----------
        other : AbstractSyntaxTree
            The right hand side AbstractSyntaxTree of the comparison.

        Returns
        -------
        : bool
            `True` if all the attributes are equal, `False` otherwise.
        """

        return vars(self) == vars(other)

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
            struct_metadata["type"] = struct_name

            struct_def_node = STRUCT_DEF(struct_metadata=struct_metadata)

            self.root.add_child(struct_def_node)

    def parse_global_variables(self) -> None:
        """Parse global variables and add it to the Abstract Syntax Tree."""

        global_variables: dict[str, dict] = (
            self.source_code.get("globals")
                            .get("variables")
        )

        for variable_name, variable_metadata in global_variables.items():
            variable_metadata["name"] = variable_name

            var_def_node = VAR_DEF(variable_metadata=variable_metadata)

            self.root.add_child(var_def_node)

    def parse_functions(self) -> None:
        """Parse functions and add it to the Abstract Syntax Tree."""

        functions: dict[str, dict] = self.source_code.get("functions")

        for function_name, function_data in functions.items():
            # We'll don't want the `statements` field to be passed as it will
            # be parsed just ahead. Thus, we avoid unnecessary duplicate
            # information
            function_metadata = {
                key: value
                for key, value in function_data.items()
                if key != "statements"
            }

            function_def_node = FUNC_DEF(
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

        if self.current_symbol == "SEMI":
            self._next_symbol()
            return

        statement_handler_map = {
            "FUNC_CALL": self._func_call,
            "RET_SYM": self._ret_sym,
            "VAR_DEF": self._var_def,
            "IF_SYM": self._if_sym,
            "WHILE_SYM": self._while_sym,
            "DO_SYM": self._do_sym,
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

        func_call_node = FUNC_CALL(function_call_metadata=self.current_value)

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

        self._next_symbol()

        ret_sym_node = RET_SYM(
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

        var_def_node = VAR_DEF(variable_metadata=self.current_value)

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

        self._next_symbol()

        parenthesis_expression = self._parenthesis_expression()
        statement_if_true = self._statement()

        # If the next symbol is `ELSE`, generate an `IFELSE` object instead
        if self.current_symbol == "ELSE_SYM":
            self._next_symbol()

            statement_if_false = self._statement()

            return IFELSE(
                parenthesis_expression=parenthesis_expression,
                statement_if_true=statement_if_true,
                statement_if_false=statement_if_false
            )
    
        return IF(
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

        self._next_symbol()

        parenthesis_expression = self._parenthesis_expression()

        loop = self._statement()

        return WHILE(
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
            parenthesis_expression=parenthesis_expression,
            loop=loop
        )

    def _brackets(self) -> SEQ:
        """
        Parse a statement embraced by brackets: `{ <statement> }`.

        Returns
        -------
        statement_node : SEQ
            The parent node of a sequence of one or more statements.
        """

        statement_node = SEQ()
    
        self._next_symbol()

        while self.current_symbol != "RCBRA":
            temp_node = statement_node

            statement_node = SEQ()

            # Avoid multiple nested SEQ statements
            both_are_seq = (
                isinstance(temp_node, SEQ) and isinstance(statement_node, SEQ)
            )

            if both_are_seq:
                statement_node.children = [*temp_node.children, *statement_node.children]
            else:
                statement_node.add_child(temp_node)

            child_statement = self._statement()

            if child_statement is not None:
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

    def _expression(self) -> Operation:
        """
        Evaluate an expression.

        Expressions are evaluated with the following precedence order:

        1. Array subscripting and structure member access.
        2. Logical not.
        3. Multiplication and division.
        4. Addition and subtraction.
        5. Bitwise left and right shifts.
        6. Less/greater than operators.
        7. Equal/not equal operators.
        8. Bitwise and.
        9. Bitwise or.
        10. Logical and.
        11. Logical or.

        Returns
        -------
        expression_node : Operation
            The node representation of the expression.
        """

        expression_node = self._logical_or()

        if isinstance(expression_node, VAR):
            if self.current_symbol == "ASSIGN":
                expression_node = self.__handle_assign(expression_node)

            # Handle access to elements of a struct or an array
            elif self.current_symbol in ["LBRA", "DOT"]:
                variable = expression_node

                self._next_symbol()

                element = self._term()

                expression_node = ELEMENT_ACCESS(
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

        # Add context to the `VAR` or `ELEMENT_ACCESS` nodes so it will generate
        # the adequate instruction (load the address rather than the value)
        if isinstance(lhs, (VAR, ELEMENT_ACCESS)):
            lhs.add_context({"context": "write"})

        self._next_symbol()

        rhs = self._expression()

        expression_node = ASSIGN(
            lhs=lhs,
            rhs=rhs
        )

        return expression_node

    def _logical_or(self) -> Operation:
        """
        Parse a `or` logical operation.

        Returns
        -------
        expression : Operation
            The node representation of the operation.
        """

        expression = self._logical_and()

        while self.current_symbol == "OR":
            self._next_symbol()

            right_expression = self._logical_and()
            expression = OR(
                lhs=expression,
                rhs=right_expression
            )

        return expression

    def _logical_and(self) -> Operation:
        """
        Parse a `and` logical operation.

        Returns
        -------
        expression : Operation
            The node representation of the operation.
        """

        expression = self._bitwise_or()

        while self.current_symbol == "AND":
            self._next_symbol()

            right_expression = self._bitwise_or()
            expression = AND(
                lhs=expression,
                rhs=right_expression
            )

        return expression

    def _bitwise_or(self) -> Operation:
        """
        Parse a bitwise `or` operation.

        Returns
        -------
        expression : Operation
            The node representation of the operation.
        """

        expression = self._bitwise_and()

        while self.current_symbol == "BITOR":
            self._next_symbol()

            right_expression = self._bitwise_and()
            expression = BITOR(
                lhs=expression,
                rhs=right_expression
            )

        return expression

    def _bitwise_and(self) -> Operation:
        """
        Parse a bitwise `and` operation.

        Returns
        -------
        expression : Operation
            The node representation of the operation.
        """

        expression = self._equality()

        while self.current_symbol == "BITAND":
            self._next_symbol()

            right_expression = self._equality()
            expression = BITAND(
                lhs=expression,
                rhs=right_expression
            )

        return expression

    def _equality(self) -> Operation:
        """
        Parse a `equal`/`not equal` comparison.

        Returns
        -------
        expression : Operation
            The node representation of the operation.
        """

        expression = self._comparison()

        _equality_nodes: dict[str, Operation] = {
            "EQUAL": EQUAL,
            "DIFF": DIFF
        }

        while self.current_symbol in _equality_nodes.keys():
            _equality_class = _equality_nodes[self.current_symbol]

            self._next_symbol()

            right_expression = self._comparison()

            expression = _equality_class(
                lhs=expression,
                rhs=right_expression
            )

        return expression

    def _comparison(self) -> Operation:
        """
        Parse a `less than`/`greater than` comparison.

        Returns
        -------
        expression : Operation
            The node representation of the operation.
        """

        expression = self._bit_shift()

        _comparison_nodes: dict[str, Operation] = {
            "LESS": LESS,
            "GREATER": GREATER
        }

        while self.current_symbol in _comparison_nodes.keys():
            _comparison_class = _comparison_nodes[self.current_symbol]

            self._next_symbol()

            right_expression = self._bit_shift()

            expression = _comparison_class(
                lhs=expression,
                rhs=right_expression
            )

        return expression

    def _bit_shift(self) -> Operation:
        """
        Parse a left/right bit shift.

        Returns
        -------
        expression : Operation
            The node representation of the operation.
        """

        expression = self._addition()

        _bit_shift_nodes: dict[str, Operation] = {
            "LSHIFT": LSHIFT,
            "RSHIFT": RSHIFT
        }

        while self.current_symbol in _bit_shift_nodes.keys():
            _bit_shift_class = _bit_shift_nodes[self.current_symbol]

            self._next_symbol()

            right_expression = self._addition()

            expression = _bit_shift_class(
                lhs=expression,
                rhs=right_expression
            )

        return expression

    def _addition(self) -> Operation:
        """
        Parse an addition or subtraction operation.

        Returns
        -------
        expression : Operation
            The node representation of the operation.
        """

        expression = self._multiplication()

        _addition_nodes: dict[str, Operation] = {
            "ADD": ADD,
            "SUB": SUB
        }

        while self.current_symbol in _addition_nodes.keys():
            _addition_class = _addition_nodes[self.current_symbol]

            self._next_symbol()

            right_expression = self._multiplication()

            expression = _addition_class(
                lhs=expression,
                rhs=right_expression
            )

        return expression

    def _multiplication(self) -> Operation:
        """
        Parse a multiplication or division operation.

        Returns
        -------
        expression : Operation
            The node representation of the operation.
        """

        expression = self._unary_operation()

        _multiplication_nodes: dict[str, Operation] = {
            "MULT": MULT,
            "DIV": DIV,
            "MOD": MOD
        }

        while self.current_symbol in _multiplication_nodes.keys():
            _multiplication_class = _multiplication_nodes[self.current_symbol]

            self._next_symbol()

            right_expression = self._unary_operation()

            expression = _multiplication_class(
                lhs=expression,
                rhs=right_expression
            )

        return expression

    def _unary_operation(self) -> Operation:
        """
        Parse an unary operation.

        Returns
        -------
        expression : Operation
            The node representation of the operation.
        """

        if self.current_symbol == "NOT":
            self._next_symbol()

            expression = NOT(expression=self._unary_operation())

        else:
            expression = self._parenthesis_expression()

        return expression

    def _parenthesis_expression(self) -> Node:
        """
        Parse a `parenthesis_expression`.

        A `parenthesis_expression` is formed by an `expression` embraced by
        parenthesis -- `( <expression> )`.

        Returns
        -------
        expression : Node
            The node representation of the expression.
        """

        if self.current_symbol == "LPAR":
            self._next_symbol()

            expression = self._expression()

            if self.current_symbol == "RPAR":
                self._next_symbol()
                return expression
            else:
                _err_msg = "Missing closing right parenthesis in expression"
                raise SyntaxError(_err_msg)
        else:
            return self._term()

    def _term(self) -> Node:
        """
        Evaluate a term.

        A term is either a variable -- `<var>` --, a constant -- `<cst>` --, or
        a function call.

        Returns
        -------
        term_node : Node
            The node representation of the term.
        """

        terms_map: dict[str, Node] = {
            "CST": CST,
            "FUNC_CALL": FUNC_CALL,
            "VAR": VAR
        }

        term_handler = terms_map[self.current_symbol]
        term_node = term_handler(self.current_value)

        self._next_symbol()

        return term_node

    def _next_symbol(self) -> None:
        """Get the next symbol to evaluate."""

        if len(self.current_statement_list) > 0:
            self.current_symbol, self.current_value = self.current_statement_list.pop(0)
        else:
            self.current_symbol, self.current_value = ("EOI", {})
