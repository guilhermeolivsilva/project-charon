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
        self.scopes: dict[str, dict] = {
            "globals": {
                "start_idx": 0,
                "end_idx": 0,
                "variables": [],
                "structs": []
            }
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

        scopes = _compute_scopes_limits(symbol_collection)

        for scope in scopes:
            if scopes == "global":
                self.parse_global_scope(symbol_collection, **scopes.get("global"))
            else:
                self.parse_function_scope(symbol_collection, **scopes.get(scope))

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
    
    def parse_scope(
        self,
        symbol_collection: list[str],
        start_idx: int,
        end_idx: int
    ) -> None:
        """
        Parse the struct types and variables to be available globally.

        This method fills the `self.scopes["globals"]` dictionary.

        Parameters
        ----------
        symbol_collection : list of str
            The collection of symbols generated by the `split_source` method.
        start_idx : int
            The starting index of the global scope in the `symbol_collection`.
        end_idx : int
            The ending index of the global scope in the `symbol_collection`.
        """

        ...

    def parse_function_scope(
        self,
        symbol_collection: list[str],
        start_idx: int,
        end_idx: int
    ) -> None:
        """
        Parse the scope of a function declared in the source code.

        This method fills the `self.scopes` dictionary key of the function.

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


def _compute_scopes_limits(
    symbol_collection: list[str]
) -> dict[str, tuple[int, int]]:
    """
    Compute the indices that bound each scope in the `symbol_collection`.

    Parameters
    ----------
    symbol_collection : list of str
        The collection of symbols generated by the `split_source` method.

    Returns
    -------
    scopes_limits : dictionary of `<scope_name>` entries
        The start and end of each scope found in the `symbol_collection`. This
        dictionary always contains the `globals` (even if there are no global
        variables) and `main` keys, and every other scope is named after its
        respective function. Each key is associated to a nested dictionary
        similar to `{"start_idx": ..., "end_idx": ...}`.
    """

    scopes_limits: dict[str, dict[str, int]] = {
        "globals": ...,
        "main": ...
    }

    return scopes_limits


def _handle_struct(symbol_collection: list[str], struct_idx: int) -> dict[str, dict]:
    """
    Handle a struct definition.

    The extracted attributes are returned as a list of (param_type, param_name)
    tuples. This method also returns the type name of the struct.

    Parameters
    ----------
    symbol_collection : list of str
        The collection of symbols generated by the `split_source` method.
    struct_idx : int
        The index of the `struct` keyword in the `symbol_collection` list.

    Returns
    -------
    struct_metadata : dict
        A dictionary with the following content:
        {
            "struct_name": name of the structure,
            "attributes": list of (`attr_type`, `attr_name`) tuples.
        }

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
    attributes: list[tuple[str, str]] = []

    # Offset of three tokens: `struct`, `<struct name>` and `{`
    struct_start: int = struct_idx + 3
    subset: list[str] = symbol_collection[struct_start:]

    idx: int = 0

    # Extract
    while idx < len(subset):
        if subset[idx] == "}":
            break

        attr_type, attr_name = subset[idx:idx + 2]
        attributes.append((attr_type, attr_name))

        # Expected format: `<attr_type>` `<attr_name>` `;`.
        # Thus, offset 3 tokens
        idx += 3

    # Validate
    # 1. Check if the struct has a valid name
    if struct_name in Lexer.reserved_words:
        err_msg = f"Invalid struct name '{struct_name}'"
        raise SyntaxError(err_msg)

    unique_attr_names = set()
    for attr_type, attr_name in attributes:

        # 2. Check if all the types are valid
        if attr_type not in Lexer.types:
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
        if attr_name in Lexer.reserved_words:
            err_msg = (
                f"Invalid name of attribute '{attr_name}' in struct"
                f"' {struct_name}'"
            )
            raise SyntaxError(err_msg)

    return {
        "struct_name": struct_name,
        "attributes": attributes
    }
