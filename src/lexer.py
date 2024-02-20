"""Implement a lexer for the Tiny C compiler."""


class Lexer:
    @classmethod
    def parse_character(cls, character: str) -> tuple[str, int]:
        """
        Parse a character and return its corresponding symbol.

        Parameters
        ----------
        character : str
            The character to be parsed. Must be a string with unit length.

        Returns
        -------
        symbol : str
            The corresponding symbol to the given character.
        value : int or None
            The value, if any.

        Raises
        ------
        SyntaxError
            Raised if the input does not correspond to a supported symbol.
        """
        if len(character) > 1:
            return ""

        symbol_map = {
            " ": "",
            "\n": "",
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
            symbol = symbol_map[character]
        except KeyError:
            if (character >= "0") and (character <= "9"):
                symbol = "INT"
                value = int(character)
            elif (character >= "a") and (character <= "z"):
                symbol = "ID"
            else:
                raise SyntaxError("The given input is not supported.")

        return (symbol, value)
