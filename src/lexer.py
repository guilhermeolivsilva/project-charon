"""Implement a lexer for the Tiny C compiler."""

from copy import deepcopy
from typing import Union

from src.ast_nodes.certificate_mapping import TYPE_SYMBOLS_MAP
from src.utils import next_prime, primes_list


class Lexer:
    conditionals: dict[str, str] = {
        "do": "DO_SYM",
        "while": "WHILE_SYM",
        "if": "IF_SYM",
        "else": "ELSE_SYM"
    }

    symbols: dict[str, str] = {
        "{": "LCBRA",
        "}": "RCBRA",
        "[": "LBRA",
        "]": "RBRA",
        "(": "LPAR",
        ")": "RPAR",
        ";": "SEMI",
        ".": "DOT"
    }

    operators: dict[str, str] = {
        "=": "ASSIGN",
        "+": "ADD",
        "-": "SUB",
        "*": "MULT",
        "/": "DIV",
        "%": "MOD",
        "<": "LESS",
        ">": "GREATER",
        "&&": "AND",
        "||": "OR",
        "<<": "LSHIFT",
        ">>": "RSHIFT",
        "&": "BITAND",
        "|": "BITOR",
        "==": "EQUAL",
        "!=": "DIFF",
        "!": "NOT"
    }

    # Map built-in types to pseudonymous
    types: dict[str, str] = {
        _type: TYPE_SYMBOLS_MAP[_type].get("type_symbol")
        for _type in TYPE_SYMBOLS_MAP.keys()
    }

    reserved_words: dict[str, str] = {
        **conditionals,
        **symbols,
        **operators,

        # Additional reserved words that are not in previous categories
        "struct": "STRUCT_DEF",
        "return": "RET_SYM",

        **types
    }

    def __init__(self, source_code: str) -> None:
        """
        Initialize the Lexer object.

        Parameters
        ----------
        source_code : str
            The high-level, [C]haron source code.
        """

        self.source_code: str = source_code
        self.functions: dict[str, dict] = {}
        self.globals: dict[str, dict] = {
            "structs": {},
            "variables": {}
        }

        self.variable_count: int = 0

        # Start at the first prime, 2
        self.struct_prime: int = 2
        self.variable_prime: int = 2

    def parse_source_code(self) -> dict[str, dict]:
        """
        Parse the scopes and functions from the given source code.

        Returns
        -------
        parsed_source_code : dict
            A dictionary containing the metadata of the global scope ("globals"
            key), and the parsed code of each function ("functions" key).

            The `globals` key contains a dictionary such as

            {
                "variables": { 
                    <variable name>: <variable type>,
                    ...
                },
                "structs": {
                    <struct name>: {
                        <attribute name>: <attribute type>,
                        ...
                    }
                }
            }

            where each `scope_name` is either a function or "globals" (for the
            case of the `global` scope). In this context, the `start` and `end`
            indices refer to the position of the tokenized source code where
            the scope lies.

            The `functions` key, on the other hand, contains

            {
                <function_name>: {
                    "type": element of `types` or a `struct` from the global
                            scope,
                    "parameters": list of (attr_type, attr_name) tuples,
                    "statements": list of annotated statements found within
                                  the function.
                },
                ...
            }
        """

        symbol_collection = self.split_source()

        # Annotate constants with their types
        symbol_collection = self._annotate_constants(symbol_collection)

        # Parse the global scope first
        self._parse_globals(symbol_collection)

        # Then, compute the bounding indices of each function, and parse them
        # one by one.
        functions_scopes = self._compute_functions_scopes_limits(
            symbol_collection=symbol_collection
        )

        # Register the functions and its definitions' relative position
        self.functions = {
            func_name: {
                "relative_position": func_relative_position,
                "prime": func_prime
            }
            for func_name, (func_relative_position, func_prime)
            in zip(
                functions_scopes.keys(),
                zip(
                    range(1, len(functions_scopes) + 1),
                    primes_list(len(functions_scopes))
                )
            )
        }

        for function in functions_scopes:
            function_data: dict[str, str] = self._parse_function(
                symbol_collection,
                **functions_scopes.get(function)
            )

            # Extend the registered functions with the parsed function data
            self.functions[function].update(function_data)

        return {
            "globals": self.globals,
            "functions": self.functions
        }

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

        # Replace commas with spaces
        source_code = source_code.replace(",", " ")

        # Tweak braces, parenthesis and semicolons before splitting the string
        # by blank spaces
        tokens_to_tweak = ["(", ")", "{", "}", ";", "[", "]"]
        for token in tokens_to_tweak:
            source_code = source_code.replace(token, f" {token} ")

        # TODO: tweak dot operator

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

    def _annotate_constants(self, symbol_collection: list[str]) -> list[str]:
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
    
    def _parse_globals(self, symbol_collection: list[str]) -> None:
        """
        Parse the struct types and variables to be available globally.

        This method fills the `self.globals` dictionary.

        Parameters
        ----------
        symbol_collection : list of str
            The collection of symbols generated by the `split_source` method.
        """

        curly_brackets_stack: list[int] = []

        for idx, token in enumerate(symbol_collection):
            if token == "{":
                curly_brackets_stack.append(1)
                continue

            elif token == "}":
                curly_brackets_stack.pop()
                continue

            # If the `curly_brackets_stack` is empty, then its a global value
            # We are only interested in structs and variables. Thus, we'll only
            # handle these constructs for now.
            if not len(curly_brackets_stack):

                if token == "struct":
                    struct_name, struct_attributes = self._handle_struct_definition(
                        symbol_collection=symbol_collection,
                        struct_idx=idx
                    )

                    struct_relative_position = len(self.globals["structs"]) + 1
                    struct_prime = self.struct_prime
                    self.struct_prime = next_prime(struct_prime)

                    self.globals["structs"][struct_name] = {
                        "relative_position": struct_relative_position,
                        "prime": struct_prime,
                        "attributes": struct_attributes,
                        "active": False
                    }

                elif token in self.globals["structs"]:
                    continue

                else:
                    definition_metadata = self._handle_variable_definition(
                        symbol_collection=symbol_collection,
                        token_idx=idx,
                        existing_variables=[*self.globals.get("variables").keys()]
                    )

                    # The `_handle_variable_definition` method will return an
                    # empty tuple if the current token is not a variable. Thus,
                    # only add it to the `globals` dict if the returned value is
                    # not valid.
                    if definition_metadata:
                        variable_name, variable_metadata = definition_metadata

                        var_relative_position = self.variable_count + 1
                        var_prime = self.variable_prime
                        variable_metadata["relative_position"] = var_relative_position
                        variable_metadata["prime"] = var_prime
                        self.globals["variables"][variable_name] = variable_metadata

                        self.variable_prime = next_prime(self.variable_prime)
                        self.variable_count += 1

    def _parse_function(
        self,
        symbol_collection: list[str],
        start_idx: int,
        end_idx: int
    ) -> dict[str, str]:
        """
        Parse the scope of a function defined in the source code.

        Parameters
        ----------
        symbol_collection : list of str
            The collection of symbols generated by the `split_source` method.
        start_idx : int
            The starting index of the function scope in the `symbol_collection`.
        end_idx : int
            The ending index of the function scope in the `symbol_collection`.

        Returns
        -------
        function_metadata : dict[str, str]
            The metadata (keys: type, parameters, statements) of the parsed
            function.
        """

        # Internal tracking
        existing_variables: list[str] = [*self.globals.get("variables").keys()]

        # Basic metadata
        function_name = symbol_collection[start_idx + 1]
        function_type = symbol_collection[start_idx]
        parameters = self._extract_parameters(
            symbol_collection=symbol_collection,
            function_idx=start_idx
        )

        # Parse the statements, and initialize the list of statements with a
        # left curly bracket ({ -- `LCBRA`)
        statements: list[tuple[str, dict]] = [("LCBRA", {})]
        statements_start_idx = (
            symbol_collection[start_idx : end_idx].index("{") + 1
        )

        function_symbol_collection = symbol_collection[
            start_idx + statements_start_idx : end_idx
        ]

        idx = 0

        # Make it easier to check if a symbol is used without being defined
        global_variables = deepcopy(self.globals.get("variables"))
        local_variables = deepcopy(parameters)
        available_variables = {
            **global_variables,
            **local_variables
        }

        available_types: list[str] = [
            *self.types,
            *self.globals["structs"]
        ]

        while idx < len(function_symbol_collection):
            curr_token = function_symbol_collection[idx]

            # Simply skip the token if it is a known type
            if curr_token in available_types:
                idx += 1

            elif "cst" in curr_token:
                statements.append(("CST", _handle_constant(curr_token)))
                idx += 1

            elif curr_token in available_variables:
                previous_token = function_symbol_collection[idx - 1]

                if previous_token in available_types:
                    raise SyntaxError(f"Redefinition of variable {curr_token}")

                var_metadata = available_variables[curr_token]
                statements.append(("VAR", var_metadata))
                idx += 1

            # Handle struct attributes
            elif "." in curr_token:
                attribute_access_metadata = self._handle_struct_attribute(
                    token=curr_token,
                    available_variables=available_variables
                )

                statements.extend(attribute_access_metadata)
                idx += 1

            # Handle variables (definition, manipulation) and function calls
            elif curr_token not in self.reserved_words:

                # First, check if it is a variable definition.
                try:
                    variable_name, variable_type = self._handle_variable_definition(
                        symbol_collection=function_symbol_collection,
                        token_idx=idx,
                        existing_variables=existing_variables
                    )
                    existing_variables.append(variable_name)

                    var_relative_position = self.variable_count + 1
                    var_prime = self.variable_prime

                    self.variable_count += 1
                    self.variable_prime = next_prime(self.variable_prime)

                    variable_metadata = {
                        "name": variable_name,
                        "relative_position": var_relative_position,
                        "prime": var_prime,
                        **variable_type
                    }

                    available_variables[variable_name] = variable_metadata
                    statements.append(("VAR_DEF", variable_metadata))

                # If not, check if it is a function call. If it is not either,
                # `_handle_function_call` will raise a SyntaxError
                except (SyntaxError, TypeError):
                    called_function_name, arguments = self._handle_function_call(
                        symbol_collection=function_symbol_collection,
                        available_variables=available_variables,
                        function_call_idx=idx
                    )

                    function_relative_position = (
                        self.functions[called_function_name]["relative_position"]
                    )
                    function_prime = (
                        self.functions[called_function_name]["prime"]
                    )

                    if function_name == called_function_name:
                        function_return_type = function_type
                    else:
                        function_return_type = (
                            self.functions.get(called_function_name)
                                        .get("type")
                        )

                    function_call_metadata = {
                        "function": function_relative_position,
                        "prime": function_prime,
                        "return_type": function_return_type,
                        "arguments": arguments
                    }

                    statements.append(("FUNC_CALL", function_call_metadata))

                    # As the arguments of the function call have already been
                    # accounted for in `function_call_metadata`, we'll skip
                    # their tokens. Thus, increment `idx` by 2 (the number of
                    # parenthesis) plus the number of arguments passed.
                    idx += 2 + len(function_call_metadata["arguments"])

                idx += 1

            # If not any of the above (but syntatically correct), it is a
            # known symbol or reserved word of the language
            else:
                statements.append((self.reserved_words.get(curr_token), {}))
                idx += 1

        # Add a closing right curly bracket (} -- `RCBRA`) to the statements
        # list.
        statements.append(("RCBRA", {}))

        function_metadata = {
            "type": function_type,
            "parameters": parameters,
            "statements": statements
        }

        return function_metadata

    def _handle_struct_definition(
        self,
        symbol_collection: list[str],
        struct_idx: int
    ) -> tuple[str, dict[str, str], int]:
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
            A tuple containing the name of the struct at the first position,
            and the dictionary of its attributes (mapping of
            `attr_name`: `attr_type`).

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

            if attr_name in attributes:
                err_msg = (
                    f"Redefinition of attribute '{attr_name}' in struct"
                    f" '{struct_name}'"
                )
                raise SyntaxError(err_msg)
            
            is_builtin_type = attr_type in self.types
            if not is_builtin_type:
                # Flag the struct type to be `active`, as a variable of its
                # type is being defined
                try:
                    self.globals["structs"][attr_type]["active"] = True
                except KeyError:
                    raise SyntaxError(
                        f"Attribute {attr_name} of struct {struct_name}"
                        + f" is being declared with unknown type {attr_type}."
                    )

            attributes[attr_name] = {
                "type": attr_type,
                "attr_pointer": len(attributes)
            }

            # Expected format: `<attr_type>` `<attr_name>` `;`.
            # Thus, offset 3 tokens
            idx += 3

        # Validate
        # 1. Check if the struct has a valid name
        if struct_name in self.reserved_words:
            err_msg = f"Invalid struct name '{struct_name}'"
            raise SyntaxError(err_msg)

        for attr_name, attr_metadata in attributes.items():
            attr_type = attr_metadata["type"]

            # 2. Check if all the types are valid
            if attr_type not in self.types or attr_type is None:
                err_msg = (
                    f"Unknown type '{attr_type}' of struct attribute"
                    f" '{attr_name}'"
                )
                raise SyntaxError(err_msg)

            # 3. Check if there are attributes named after reserved words
            if attr_name in self.reserved_words:
                err_msg = (
                    f"Invalid name of attribute '{attr_name}' in struct"
                    f" '{struct_name}'"
                )
                raise SyntaxError(err_msg)

        struct_metadata = (struct_name, attributes)

        return struct_metadata

    def _handle_variable_definition(
        self,
        symbol_collection: list[str],
        token_idx: int,
        existing_variables: list[str]
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
        existing_variables : list[str]
            A list containing the names of the currently existing variables.
            This prevents irrestricted variable redefinition.

        Returns
        -------
        : tuple of (`variable_name`, `variable_type`) or empty tuple
            A tuple of the variable metadata. If not a variable, an empty tuple.

        Raises
        ------
        SyntaxError
            Raised if
             - the variable is a redefinition;
             - the variable is of unknown type;
             - the variable is not followed by a valid token (`;`, `(`, `)`,
               `=`, `[`, `]`).
        """

        available_types: list[str] = [
            *self.types,
            *self.globals["structs"]
        ]

        try:
            # First, discard tokens that represent reserved words/symbols or constants
            variable_name = symbol_collection[token_idx]

            if variable_name in self.reserved_words or 'cst' in variable_name:
                return tuple()
            
            if variable_name in existing_variables:
                raise SyntaxError(f"Redefinition of variable {variable_name}")

            previous_token = symbol_collection[token_idx - 1]
            next_token = symbol_collection[token_idx + 1]

            previous_token_is_valid_type = previous_token in [
                *available_types,
                "struct"
            ]
            simple_variable_definition = next_token in [";", "="]
            array_definition = next_token == "["

            variable_type = previous_token

            next_token_is_valid = next_token in [
                "(",
                ")",
                "{",
                "}",
                ";",
                "=",
                "[",
                "]",
                *available_types
            ]

            if not next_token_is_valid:
                err_msg = (
                    "Syntax error near definition of variable"
                    f" '{variable_name}'"
                )
                raise SyntaxError(err_msg)

            if previous_token_is_valid_type:
                is_builtin_type = variable_type in self.types
                if not is_builtin_type:
                    # Flag the struct type to be `active`, as a variable of its
                    # type is being defined
                    try:
                        self.globals["structs"][variable_type]["active"] = True
                    except (KeyError, IndexError):
                        raise SyntaxError(
                            f"Variable {variable_name} is being declared with"
                            + f" unknown type {variable_type}."
                        )

                variable_metadata = {
                    "type": variable_type
                }

                # Export attributes information if it is a struct!
                if variable_type in self.globals["structs"]:
                    variable_metadata = {
                        **variable_metadata,
                        "attributes": self.globals["structs"][variable_type]["attributes"]
                    }

                if simple_variable_definition:
                    return variable_name, variable_metadata
            
                elif array_definition:
                    array_length = _handle_constant(
                        annotated_constant=symbol_collection[token_idx + 2],
                        number_only=True
                    )

                    # Remove the left and right brackets, and the array length
                    # from the `symbol_collection` so array definitions will
                    # not be mistaken with array item accesses.
                    del symbol_collection[token_idx + 1 : token_idx + 4]

                    array_metadata = {
                        **variable_metadata,
                        "length": array_length
                    }

                    return variable_name, array_metadata
            
            elif not previous_token_is_valid_type:
                err_msg = (
                    f"Variable '{variable_name}' of unknown type"
                    f" '{variable_type}'"
                )
                raise SyntaxError(err_msg)

        except IndexError:
            return tuple()
 
    def _handle_struct_attribute(
        self,
        token: str,
        available_variables: dict[str, dict[str, str]]
    ) -> list[str, tuple]:

        struct_var, struct_attr = token.split(".")

        # Check if the variable has been declared
        if struct_var not in available_variables:
            err_msg = f"Invalid access of attribute '{struct_attr}' of unknown"
            err_msg += f" struct variable '{struct_var}'"
            raise SyntaxError(err_msg)

        # Check if the struct type has the attribute of interest
        struct_type = available_variables[struct_var]["type"]
        if struct_attr not in self.globals["structs"][struct_type]["attributes"]:
            err_msg = f"Access of unknown attribute '{struct_attr}' of"
            err_msg += f" variable '{struct_var}'"
            raise SyntaxError(err_msg)

        var_metadata = available_variables[struct_var]
        struct_metadata = self.globals["structs"][struct_type]

        struct_attribute_metadata = {
            **struct_metadata,
            **var_metadata
        }

        attr_pointer = (
            list(self.globals["structs"][struct_type]["attributes"])
                .index(struct_attr)
        )

        return [
            ("VAR", struct_attribute_metadata),
            ("DOT", {}),
            ("CST", {"type": "int", "value": attr_pointer})
        ]

    def _handle_function_call(
        self,
        symbol_collection: list[str],
        available_variables: dict[str, str],
        function_call_idx: int
    ) -> tuple[str, list[dict]]:
        """
        Handle a function call to extract the callee and arguments.

        Parameters
        ----------
        symbol_collection : list of str
            The collection of symbols generated by the `split_source` method.
        available_variables : dict
            A dictionary containing the variables available at the scope where
            the function was called.
        struct_idx : int
            The index of the function call in the `symbol_collection` list.

        Returns
        -------
        function_name : str
            The name of the called function.
        arguments : list[dict]
            List of arguments' metadata.

        Raises
        ------
        SyntaxError
            Raised if the called function is not defined.
        """

        function_name: str = symbol_collection[function_call_idx]

        if function_name not in self.functions.keys():
            raise SyntaxError(f"Use of undefined name '{function_name}'")

        arguments: list[dict] = []

        for token in symbol_collection[function_call_idx + 1:]:
            if token == "(":
                continue

            elif token == ")":
                break

            # Export the variable metadata
            if token in available_variables:
                argument = {
                    "variable": True,
                    **available_variables[token]
                }

            # If not a variable, then it's a constant. Thus, save it to the
            # `arguments` list after extracting its actual value.
            else:
                argument = {
                    "variable": False,
                    **_handle_constant(token)
                }
            
            arguments.append(argument)

        return function_name, arguments

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
                    end_idx = _find_function_bounds(symbol_collection, idx)
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

    def _extract_parameters(
        self,
        symbol_collection: list[str],
        function_idx: int
    ) -> dict[str, str]:
        """
        Extract the parameters from a function.

        The extracted parameters are returned as a dictionary of parameters
        metadata.

        Parameters
        ----------
        symbol_collection : list of str
            The collection of symbols generated by the `split_source` method.
        function_idx : int
            The index of the function name in the `symbol_collection` list.

        Returns
        -------
        parameters : dict
            A mapping of `param_name`: `param_type`. If the function takes no
            parameters, return an empty list.

        Raises
        ------
        SyntaxError
            Raised if
             - the function has malformed parameters (i.e., missing type and/or
               name).
             - a parameter has unknown type.
        """
        
        # Align with the index of the left parenthesis (add 2 to offset).
        curr_idx: int = function_idx + 2
        parameters: dict[str, str] = {}

        try:
            while symbol_collection[curr_idx] != ")":
                curr_token = symbol_collection[curr_idx]

                if curr_token == "(":
                    curr_idx += 1

                elif curr_token == ")":
                    break

                else:
                    param_type = curr_token
                    param_name = symbol_collection[curr_idx + 1]

                    if param_type not in [*self.types, *self.globals["structs"]]:
                        function_name = symbol_collection[function_idx]
                        err_msg = (
                            f"Unknown type '{param_type}' in definition of "
                            + f"function '{function_name}'"
                        )
                        raise SyntaxError(err_msg)

                    parameter_relative_position = self.variable_count + 1
                    parameter_prime = self.variable_prime

                    self.variable_count += 1
                    self.variable_prime = next_prime(self.variable_prime)

                    parameters[param_name] = {
                        "type": param_type,
                        "relative_position": parameter_relative_position,
                        "prime": parameter_prime
                    }
                    curr_idx += 2

        except IndexError:
            function_name = symbol_collection[function_idx]
            err_msg = f"Function '{function_name}' has malformed parameters."
            raise SyntaxError(err_msg)

        return parameters


def _find_function_bounds(symbol_collection: list[str], token_idx: int) -> int: 
    curly_brackets_stack = []
    parsing_started = False
    parsing_ended = False

    for idx, token in enumerate(symbol_collection[token_idx:]):
        if token == "{":
            parsing_started = True
            curly_brackets_stack.append(1)

        elif token == "}":
            curly_brackets_stack.pop()

        if parsing_started and not len(curly_brackets_stack):
            parsing_ended = True
            break

    if not parsing_ended:
        raise SyntaxError("Missing closing curly brace ('}')")

    scope_end = idx + token_idx

    return scope_end


def _handle_constant(
    annotated_constant: str,
    number_only: bool = False
) -> Union[int, float]:
    if "int" in annotated_constant:
        str_to_offset = "int_cst_"

        value = int(annotated_constant[len(str_to_offset):])
        _type = "int"
    
    else:
        str_to_offset = "float_cst_"

        _type = "float"
        value = float(annotated_constant[len(str_to_offset):])

    if number_only:
        return value

    return {
        "type": _type,
        "value": value
    }
