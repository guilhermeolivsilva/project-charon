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
        : list
            List of symbols that represent the source code.
        """

        return list(map(Lexer.parse_word, source_code))

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
            " ": "",
            "\n": "",
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
