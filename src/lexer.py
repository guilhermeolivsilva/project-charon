"""Implement a lexer for the Tiny C compiler."""


class Lexer:
    @classmethod
    def parse_source_code(cls, source_code: str) -> list:
        """
        Parse the reserved words first, and then character by character.

        Parameters
        ----------
        source_code : str
            The source code to parse.

        Returns
        -------
        parsed_source_code : list
            List of symbols that represent the source code.
        """

        parsed_source_code = list(
            map(Lexer.parse_word, Lexer.preprocess_source_code(source_code))
        )

        parsed_source_code.append(("EOI", None))

        return parsed_source_code

    @classmethod
    def parse_word(cls, word: str) -> tuple[str, int]:
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

        symbol_map = {
            "do": "DO_SYM",
            "while": "WHILE_SYM",
            "if": "IF_SYM",
            "else": "ELSE_SYM",
            "{": "LBRA",
            "}": "RBRA",
            "(": "LPAR",
            ")": "RPAR",
            "+": "PLUS",
            "-": "MINUS",
            "<": "LESS",
            ";": "SEMI",
            "=": "EQUAL",
        }

        value = None

        try:
            symbol = symbol_map[word]
        except KeyError:
            if (word >= "0") and (word <= "9"):
                symbol = "INT"
                value = int(word)
            elif (word >= "a") and (word <= "z"):
                symbol = "ID"
                value = word
            else:
                raise SyntaxError("The given input is not supported.")

        return (symbol, value)
    
    @classmethod
    def preprocess_source_code(cls, source_code: str) -> list[str]:
        """
        Preprocess the source code and return its of words and characters.

        This method is intended to handle reserved words, spaces, line breaks
        and other style-related issues.

        Parameters
        ----------
        source_code : str
            The source code to preprocess.

        Returns
        -------
        preprocessed_source_code : list of str
            A list of words and individual characters obtained from the source
            code.
        """

        # Remove line breaks
        source_code = source_code.replace("\n", "")

        # Tweak braces, parenthesis and semicolons before splitting the string
        # by blank spaces
        tokens_to_tweak = ["(", ")", "{", "}", ";"]
        for token in tokens_to_tweak:
            source_code = source_code.replace(token, f" {token} ")

        # Split the code word by word (or character by character)
        source_code = source_code.split(" ")

        # Remove empty tokens
        preprocessed_source = list(
            filter(
                lambda x: x if len(x) > 0 else None,
                source_code
            )
        )

        return preprocessed_source
