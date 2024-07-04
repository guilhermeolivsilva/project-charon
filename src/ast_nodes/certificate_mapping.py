"""Map each AST Node to a certificate."""


# First symbol is 2 because, if it were 1, any operation using it as the base
# would be an identity.
__STARTING_SYMBOL = 2

__CERTIFICATE_SYMBOLS = [
    "CST",
    "VAR",
    "VAR_DEF",
    "STRUCT_DEF",
    "ELEMENT_ACCESS",
    "FUNC_CALL",
    "RET_SYM",
    "ASSIGN",
    "ADD",
    "SUB",
    "MULT",
    "DIV",
    "LESS",
    "GREATER",
    "AND",
    "OR",
    "LSHIFT",
    "RSHIFT",
    "BITAND",
    "BITOR",
    "EQUAL",
    "IF",
    "IFELSE",
    "WHILE",
    "DOWHILE",
    "PROG",
    "EXPR",
    "SEQ",
    "EMPTY"
]

CERTIFICATE_SYMBOLS_MAP = {
    certificate: str(base)
    for certificate, base in zip(
        __CERTIFICATE_SYMBOLS,
        range(
            __STARTING_SYMBOL,
            __STARTING_SYMBOL + len(__CERTIFICATE_SYMBOLS)
        )
    )
}
