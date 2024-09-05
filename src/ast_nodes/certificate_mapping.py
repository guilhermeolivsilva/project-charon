"""Manage the mapping from symbols to base certificates."""

from src.utils import primes_list

# First symbol is 2 because, if it were 1, any operation using it as the base
# would be an identity.
__STARTING_SYMBOL = 2

__CERTIFICATE_SYMBOLS = [
    "CST",
    "EXPR",
    "SEQ",
    "VAR_DEF",
    "STRUCT_DEF",
    "VAR",
    "ELEMENT_ACCESS",
    "FUNC_CALL",
    "RET_SYM",
    "PROG",
    "ASSIGN",
    "ADD",
    "SUB",
    "MULT",
    "DIV",
    "LESS",
    "GREATER",
    "EQUAL",
    "AND",
    "OR",
    "LSHIFT",
    "RSHIFT",
    "BITAND",
    "BITOR",
    "IF",
    "IFELSE",
    "WHILE",
    "DO",
    "EMPTY",
]

__TYPES_SYMBOLS = [
    "short",
    "int",
    "float"
]


NODE_SYMBOLS_MAP = {
    certificate: str(base)
    for certificate, base in zip(
        __CERTIFICATE_SYMBOLS,
        range(__STARTING_SYMBOL, __STARTING_SYMBOL + len(__CERTIFICATE_SYMBOLS)),
    )
}


TYPE_SYMBOLS_MAP = {
    _type: {
        "type_symbol": base,
        "enforce": float if _type == "float" else int
    }

    for _type, base in zip(
        __TYPES_SYMBOLS,
        primes_list(len(__TYPES_SYMBOLS))
    )
}
