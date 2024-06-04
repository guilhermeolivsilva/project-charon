"""Implement a lexer for the Tiny C compiler."""

from string import ascii_lowercase


class Lexer:
    reserved_words = {
        # Types
        "int": "INT_TYPE",
        "float": "FLOAT_TYPE",
        "struct": "STRUCT_DEF",

        # Conditionals
        "do": "DO_SYM",
        "while": "WHILE_SYM",
        "if": "IF_SYM",
        "else": "ELSE_SYM",

        # Functions
        "return": "RET_SYM"
    }

    symbols = {
        "{": "LCBRA",
        "}": "RCBRA",
        "[": "LBRA",
        "]": "RBRA",
        "(": "LPAR",
        ")": "RPAR",
        "+": "PLUS",
        "-": "MINUS",
        "<": "LESS",
        ";": "SEMI",
        "=": "EQUAL",
        ".": "DOT"
    }

    lexer_tokens = {
        **reserved_words,
        **symbols
    }

    def __init__(self, source_code: str) -> None:
        self.source_code: str = source_code
        self.user_defined: dict[str, set] = {
            "structs": set(),
            "functions": set(),
            "variables": set()
        }

    def parse_source_code(self) -> list:
        """
        Parse the source code and generate tokens from it.

        Returns
        -------
        parsed_source_code : list of (str, str | int | float | None) tuples
            List of tokens that represent the source code. This list has been
            validated, and is syntactically correct.
        """

        tokenized_source_code = list(
            map(
                self.parse_word,
                self.tokenize_source_code()
            )
        )

        postprocessed_source_code = self.postprocess_source_code(
            tokenized_source_code=tokenized_source_code
        )

        self.validate_source_code_syntax(postprocessed_source_code)

        return postprocessed_source_code

    def parse_word(self, word: str) -> tuple[str, int]:
        """
        Parse a word and return its corresponding symbol.

        Parameters
        ----------
        word : str
            The word to parse.

        Returns
        -------
        symbol : str
            The corresponding symbol to the given word.
        value : int or None
            The associated value, if any.

        Raises
        ------
        SyntaxError
            Raised if the input does not correspond to a supported symbol.
        """

        value = None

        # Try parsing the word as a known symbol or reserved word. If the
        # attempt fails, then pattern match the function/variable
        if word in self.lexer_tokens.keys():
            symbol = self.lexer_tokens[word]

        elif "func_" in word:
            symbol = "FUNC"
            value = word[5:]

        elif "var_" in word:
            symbol = "ID"
            value = word[4:]

        elif "float_" in word:
            symbol = "FLOAT"
            value = float(word[6:])

        elif "int_" in word:
            symbol = "INT"
            value = int(word[4:])

        elif "struct_" in word:
            symbol = "STRUCT"
            value = word[7:]

        else:
            raise SyntaxError(f"Syntax error at '{word}'.")

        return (symbol, value)

    def tokenize_source_code(self) -> list[str]:
        """
        Tokenize the source code.

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

        # Tweak braces, parenthesis and semicolons before splitting the string
        # by blank spaces
        tokens_to_tweak = ["(", ")", "{", "}", ";"]
        for token in tokens_to_tweak:
            source_code = source_code.replace(token, f" {token} ")

        # Split the code word by word (or character by character)
        source_code = source_code.split(" ")

        # Remove empty tokens
        tokenized_source = list(
            filter(lambda x: x if len(x) > 0 else None, source_code)
        )

        # Add preffixes to variables and functions
        for idx, word in enumerate(tokenized_source):
            if word in Lexer.lexer_tokens.keys():
                continue

            try:
                _ = int(word)
                tokenized_source[idx] = "int_" + word
            except ValueError:
                try:
                    _ = float(word)
                    tokenized_source[idx] = "float_" + word
                except ValueError:
                    try:
                        is_followed_by_par = tokenized_source[idx + 1] == "("
                        is_preceeded_by_struct = tokenized_source[idx - 1] == "struct"

                        if is_followed_by_par:
                            tokenized_source[idx] = "func_" + word
                            self.user_defined["functions"].add(word)
                        elif is_preceeded_by_struct:
                            tokenized_source[idx] = "struct_" + word
                            self.user_defined["structs"].add(word)
                        else:
                            tokenized_source[idx] = "var_" + word
                            self.user_defined["variables"].add(word)
                    except IndexError:
                        continue

        return tokenized_source

    def postprocess_source_code(self, tokenized_source_code: list) -> list:
        """
        Post-process the source code to handle user defined types (structs).

        Parameters
        ----------
        tokenized_source_code : list of (str, str | int | float | None) tuples
            The list of tokens generated from mapping all the words to the
            `parse_word` method.

        Returns
        -------
        postprocessed_source_code : list of (str, str | int | float | None) tuples
            The post-processed source code.
        """

        postprocessed_source_code = tokenized_source_code

        for idx, token in enumerate(postprocessed_source_code):
            symbol, value = token

            # Move the struct name to the STRUCT_DEF token
            if symbol == "STRUCT_DEF":
                struct_symbol, struct_name = postprocessed_source_code[idx + 1]

                try:
                    assert struct_symbol == "STRUCT"
                except AssertionError:
                    raise ValueError("Missing name in struct declaration.")
                
                new_token = (symbol, struct_name)
                postprocessed_source_code[idx] = new_token
                del postprocessed_source_code[idx + 1]

            # Correct the symbol for used defined variables
            elif symbol == "ID" and value in self.user_defined["structs"]:
                new_token = ("STRUCT_TYPE", value)
                postprocessed_source_code[idx] = new_token

        return postprocessed_source_code

    def validate_source_code_syntax(self, post_processed_source_code: list) -> None:
        """
        Validate the tokenized source code syntax.

        This method validates if variables and functions are typed, and if it
        doesn't use any reserved words as its names.

        Parameters
        ----------
        post_processed_source_code : list of (str, str | int | float | None) tuples
            The source code after being post-processed.
        """

        for idx, token in enumerate(post_processed_source_code):
            symbol, _ = token
            err_msg = ""

            # Check if there are variables or functions named after reserved words
            if "TYPE" in symbol:
                try:
                    next_symbol, _ = post_processed_source_code[idx + 1]

                    if next_symbol == "STRUCT_TYPE":
                        err_msg = "Variable named after user-defined struct."

                    if next_symbol in self.lexer_tokens.values():
                        err_msg = (
                            "Variable or function named after reserved word or"
                            + " symbol."
                        )

                except KeyError:
                    # If it raises a KeyError, then the current symbol is the
                    # last symbol of the tokenized source. Thus, it is invalid
                    err_msg = "Missing variable or function name after type."

            # Check if two variables appear in a row, without any operators
            # in between.
            if symbol == "ID":
                try:
                    next_symbol, _ = post_processed_source_code[idx + 1]

                    if next_symbol == "ID":
                        err_msg = (
                            "Multiple variables in a row without operator in"
                            + " between."
                        )

                except IndexError:
                    continue

            if err_msg:
                raise SyntaxError(err_msg)
