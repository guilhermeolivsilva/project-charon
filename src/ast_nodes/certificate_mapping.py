"""Manage the mapping from symbols to base certificates."""

from src.utils import primes_list


__CERTIFICATE_SYMBOLS = [
    "CST",
    "VAR_DEF",
    "VAR_READ",
    "VAR_WRITE",
    "ELEMENT_VALUE",
    "ELEMENT_ADDRESS",
    "FUNC_CALL",
    "PARAM",
    "RET_SYM",
    "PROG",
    "ASSIGN",
    "ADD",
    "SUB",
    "MULT",
    "DIV",
    "MOD",
    "LESS",
    "GREATER",
    "EQUAL",
    "DIFF",
    "AND",
    "OR",
    "NOT",
    "LSHIFT",
    "RSHIFT",
    "BITAND",
    "BITOR",
    "IF",
    "IFELSE",
    "WHILE",
    "DO"
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
        primes_list(len(__CERTIFICATE_SYMBOLS))
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
