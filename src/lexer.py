"""Implement a lexer for the Tiny C compiler."""


class Lexer:
    types = {
        "int": "INT_TYPE",
        "float": "FLOAT_TYPE",
        "long": "LONG_TYPE"
    }

    conditionals = {
        "do": "DO_SYM",
        "while": "WHILE_SYM",
        "if": "IF_SYM",
        "else": "ELSE_SYM"
    }

    symbols = {
        "{": "LCBRA",
        "}": "RCBRA",
        "[": "LBRA",
        "]": "RBRA",
        "(": "LPAR",
        ")": "RPAR",
        ";": "SEMI",
        ".": "DOT"
    }

    operators = {
        "=": "ASSIGN",
        "+": "PLUS",
        "-": "MINUS",
        "*": "MULT",
        "/": "DIV",
        "<": "LESS",
        ">": "GREATER",
        "&&": "AND",
        "||": "OR",
        "<<": "LSHIFT",
        ">>": "RSHIFT",
        "&": "BITAND",
        "|": "BITOR",
        "==": "EQUAL"
    }

    reserved_words = {
        **types,
        **conditionals,
        **symbols,
        **operators,

        # Additional reserved words that are not in previous categories
        "struct": "STRUCT_DEF",
        "return": "RET_SYM"
    }

    def __init__(self, source_code: str) -> None:
        self.source_code: str = source_code
        self.functions: dict[str, dict] = {}
        self.globals: dict[str, dict] = {
            "variables": {},
            "structs": {}
        }

    def parse_source_code(self) -> dict:
        """
        Parse the scopes and functions from the given source code.

        Returns
        -------
        scopes : dict
            A dictionary containing the scopes parsed from the source code.
            This dictionary is formatted as

            {
                `scope_name`: {
                    "start_idx": int,
                    "end_idx": int,
                    "variables": list[str],
                    "structs": list[str]
                },
                ...
            }

            where each `scope_name` is either a function or "globals" (for the
            case of the `global` scope). In this context, the `start` and `end`
            indices refer to the position of the tokenized source code where
            the scope lies.

        functions : dict
            A dictionary containing the parsed from the source code. This
            dictionary is formatted as

            {
                `function_name`: {
                    "type": element of `types` or a `struct` from the global
                            scope.
                    "parameters": list of (attr_type, attr_name) tuples.
                }
            }
        """

        symbol_collection = self.split_source()

        # Annotate constants with their types
        symbol_collection = self.annotate_constants(symbol_collection)

        # Parse the global scope first
        self.parse_global_scope(symbol_collection)

        # Then, compute the bounding indices of each function, and parse them
        # one by one.
        functions_scopes = self._compute_functions_scopes_limits(
            symbol_collection=symbol_collection
        )

        for function in functions_scopes:
            self.parse_function_scope(
                symbol_collection,
                **functions_scopes.get(function)
            )

    def split_source(self) -> list[str]:
        """
        Split the source code in individual words and symbols.

        This method is intended to handle reserved words, spaces, line breaks
        and other style-related issues.

        Returns
        -------
        tokenized_source_code : list of str
            A list of words and individual characters obtained from the source
            code.
        """

        # Remove line breaks
        source_code = self.source_code.replace("\n", "")

        # Collapse `long int` to just `long`
        source_code = source_code.replace("long int", "long")

        # Replace commas with spaces
        source_code = source_code.replace(",", " ")

        # Tweak braces, parenthesis and semicolons before splitting the string
        # by blank spaces
        tokens_to_tweak = ["(", ")", "{", "}", ";", "[", "]"]
        for token in tokens_to_tweak:
            source_code = source_code.replace(token, f" {token} ")

        # Split the code word by word (or character by character)
        source_code = source_code.split(" ")

        # Remove empty tokens
        remove_empty_filter = (
            lambda curr_token: curr_token if len(curr_token) > 0 else None
        )
        tokenized_source = list(
            filter(remove_empty_filter, source_code)
        )

        return tokenized_source

    def annotate_constants(self, symbol_collection: list[str]) -> list[str]:
        """
        Annotate constants with types.

        Parameters
        ----------
        symbol_collection : list of str
            The collection of symbols generated by the `split_source` method.

        Returns
        -------
        symbol_collection : list of str
            The `symbol_collection` with annotated constants.
        """

        for idx, token in enumerate(symbol_collection):
            try:
                _ = int(token)
                symbol_collection[idx] = "int_cst_" + token
                continue

            except ValueError:
                pass

            try:
                _ = float(token)
                symbol_collection[idx] = "float_cst_" + token
                continue

            except ValueError:
                pass

        return symbol_collection
    
    def parse_global_scope(self, symbol_collection: list[str]) -> None:
        """
        Parse the struct types and variables to be available globally.

        This method fills the `self.globals` dictionary.

        Parameters
        ----------
        symbol_collection : list of str
            The collection of symbols generated by the `split_source` method.
        """

        curly_brackets_stack = []

        for idx, token in enumerate(symbol_collection):
            if token == "{":
                curly_brackets_stack.append(1)

            # If the `curly_brackets_stack` is empty, then its a global value
            # We are only interested in structs and variables. Thus, we'll only
            # handle these constructs for now.
            if not len(curly_brackets_stack):

                if token == "struct":
                    struct_name, struct_attributes = self._handle_struct(
                        symbol_collection=symbol_collection,
                        struct_idx=idx
                    )
                    self.globals["structs"][struct_name] = struct_attributes

                else:
                    variable_metadata = self._handle_variable(
                        symbol_collection=symbol_collection,
                        token_idx=idx
                    )

                    # The `_handle_variable` method will return an empty tuple
                    # if the current token is not a variable. Thus, only add it
                    # to the `globals` dict if the returned value is not valid.
                    if variable_metadata:
                        variable_name, variable_type = variable_metadata
                        self.globals["variables"][variable_name] = variable_type

            elif token == "}":
                curly_brackets_stack.pop()

    def parse_function_scope(
        self,
        symbol_collection: list[str],
        start_idx: int,
        end_idx: int
    ) -> None:
        """
        Parse the scope of a function defined in the source code.

        This method fills the `self.functions` dictionary key of the function.

        Parameters
        ----------
        symbol_collection : list of str
            The collection of symbols generated by the `split_source` method.
        start_idx : int
            The starting index of the function scope in the `symbol_collection`.
        end_idx : int
            The ending index of the function scope in the `symbol_collection`.
        """

        ...

    def _handle_struct(
        self,
        symbol_collection: list[str],
        struct_idx: int
    ) -> tuple[str, dict[str, str]]:
        """
        Handle a struct type definition.

        The extracted attributes are returned as a dictionary with mappings of
        `attr_name`: `attr_type`.

        Parameters
        ----------
        symbol_collection : list of str
            The collection of symbols generated by the `split_source` method.
        struct_idx : int
            The index of the `struct` keyword in the `symbol_collection` list.

        Returns
        -------
        struct_metadata : tuple of (<struct_name>, <attributes>)
            A tuple containing the name of the struct at the first position, and
            the dictionary of its attributes (mapping of `attr_name`: `attr_type`).

        Raises
        ------
        SyntaxError
            Raised if
                - the struct is named after a reserved word or symbol;
                - any attributes are named after a reserved word or symbol;
                - an attribute is redefined within the struct;
                - the struct uses an unknown type for one of its attributes.
        """

        struct_name: str = symbol_collection[struct_idx + 1]
        attributes: dict[str, str] = {}

        # Offset of three tokens: `struct`, `<struct name>` and `{`
        struct_start: int = struct_idx + 3
        subset: list[str] = symbol_collection[struct_start:]

        idx: int = 0

        # Extract
        while idx < len(subset):
            if subset[idx] == "}":
                break

            attr_type, attr_name = subset[idx:idx + 2]
            attributes[attr_name] = attr_type

            # Expected format: `<attr_type>` `<attr_name>` `;`.
            # Thus, offset 3 tokens
            idx += 3

        # Validate
        # 1. Check if the struct has a valid name
        if struct_name in self.reserved_words:
            err_msg = f"Invalid struct name '{struct_name}'"
            raise SyntaxError(err_msg)

        unique_attr_names = set()
        for attr_name, attr_type in attributes.items():

            # 2. Check if all the types are valid
            if attr_type not in self.types:
                err_msg = (
                    f"Unknown type '{attr_type}' of struct attribute"
                    f" '{attr_name}'"
                )
                raise SyntaxError(err_msg)
            
            # 3. Check if there are no attributes with duplicate names
            if attr_name in unique_attr_names:
                err_msg = (
                    f"Redefinition of attribute '{attr_name}' in struct"
                    f" '{struct_name}'"
                )
                raise SyntaxError(err_msg)
            else:
                unique_attr_names.add(attr_name)

            # 4. Check if there are attributes named after reserved words
            if attr_name in self.reserved_words:
                err_msg = (
                    f"Invalid name of attribute '{attr_name}' in struct"
                    f"' {struct_name}'"
                )
                raise SyntaxError(err_msg)

        struct_metadata = (struct_name, attributes)

        return struct_metadata

    def _handle_variable(
        self,
        symbol_collection: list[str],
        token_idx: int
    ) -> tuple[str, str]:
        """
        Handle a variable definition.

        This method first tests if the token at the given `token_idx` is a
        variable. If it is, then validate it (check the `Raises` section for
        more details) and return its name and type. If not, simply return an
        empty tuple.

        Parameters
        ----------
        symbol_collection : list of str
            The collection of symbols generated by the `split_source` method.
        token_idx : int
            The index of the current token in the `symbol_collection` list.

        Returns
        -------
        : tuple of (`variable_name`, `variable_type`) or empty tuple
            A tuple of the variable metadata. If not a variable, an empty tuple

        Raises
        ------
        SyntaxError
            Raised if
             - the variable is of unknown type;
             - the variable is not followed by a valid token (`;`, `(`, `)`,
               `=`).
        """

        try:
            # First, discard tokens that represent reserved words/symbols or constants
            token = symbol_collection[token_idx]

            if token in self.reserved_words or 'cst' in token:
                return tuple()

            previous_token = symbol_collection[token_idx - 1]
            next_token = symbol_collection[token_idx + 1]

            previous_token_is_valid_type = (
                previous_token in [*self.types, *self.globals["structs"]]
            )
            next_token_is_valid = next_token in [";", "="]

            variable_name = symbol_collection[token_idx]
            variable_type = previous_token

            if previous_token_is_valid_type and next_token_is_valid:
                return (variable_name, variable_type)
            
            elif next_token_is_valid:
                err_msg = (
                    f"Variable '{variable_name}' of unknown type"
                    f" '{variable_type}'"
                )
                raise SyntaxError(err_msg)
            
            elif previous_token_is_valid_type:
                # If the token is preceeded by a valid type, and followed by a
                # left or right parenthesis, then it is, respectivelly, a
                # function definition or a function parameter -- which are
                # syntatically valid.
                if next_token not in ["(", ")"]:
                    err_msg = (
                        "Syntax error near definition of variable"
                        f" '{variable_name}'"
                    )
                    raise SyntaxError(err_msg)

        except IndexError:
            return tuple()

    def _compute_functions_scopes_limits(
        self,
        symbol_collection: list[str]
    ) -> dict[str, dict[str, int]]:
        """
        Compute the indices that bound each scope in the `symbol_collection`.

        Parameters
        ----------
        symbol_collection : list of str
            The collection of symbols generated by the `split_source` method.

        Returns
        -------
        scopes_limits : dictionary of `<scope_name>` entries
            The start and end indices of each function scope found in the
            `symbol_collection`. Each key is named after its respective
            function. Each key is associated to a nested dictionary similar
            to `{"start_idx": ..., "end_idx": ...}`.
        """

        scopes_limits: dict[str, dict[str, int]] = {}

        for idx, token in enumerate(symbol_collection):
            try:
                if self._is_function_definition(symbol_collection, idx):
                    start_idx = idx - 1
                    end_idx = _find_function_scope_end(symbol_collection, idx)
                    function_name = token

                    scopes_limits[function_name] = {
                        "start_idx": start_idx,
                        "end_idx": end_idx
                    }

            except IndexError:
                continue

        return scopes_limits

    def _is_function_definition(
        self,
        symbol_collection: list[str],
        token_idx: int
    ) -> bool:
        """
        Decide whether given a token is a function definition.

        Parameters
        ----------
        symbol_collection : list of str
            The collection of symbols generated by the `split_source` method.
        token_idx : int
            The index of the current token in the `symbol_collection` list.

        Returns
        -------
        : bool
            True if the token is a function definition, False otherwise.
        """

        previous_token_is_type = symbol_collection[token_idx - 1] in [
            *self.types,
            *self.globals["structs"].keys()
        ]

        next_token_is_left_parenthesis = (
            symbol_collection[token_idx + 1] == "("
        )

        return previous_token_is_type and next_token_is_left_parenthesis


def _find_function_scope_end(symbol_collection: list[str], token_idx: int) -> int:
    curly_brackets_stack = []
    parsing_started = False

    for idx, token in enumerate(symbol_collection[token_idx:]):
        if token == "{":
            parsing_started = True
            curly_brackets_stack.append(1)

        elif token == "}":
            curly_brackets_stack.pop()

        if parsing_started and not len(curly_brackets_stack):
            break

    scope_end = idx + token_idx

    return scope_end
