"""Manage the mapping from symbols to base certificates."""

from src.utils import primes_list


__NODES = [
    "CST",
    "VAR_DEF",
    "VAR_VALUE",
    "VAR_ADDRESS",
    "ELEMENT_VALUE",
    "ELEMENT_ADDRESS",
    "FUNC_CALL",
    "PARAM",
    "ARG",
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

__BUILTIN_TYPES = [
    "short",
    "int",
    "float"
]


NODE_SYMBOLS_MAP = {
    certificate: str(base)
    for certificate, base in zip(
        __NODES,
        primes_list(len(__NODES))
    )
}


TYPE_SYMBOLS_MAP = {
    _type: {
        "type_symbol": base,
        "enforce": float if _type == "float" else int
    }

    for _type, base in zip(
        __BUILTIN_TYPES,
        primes_list(len(__BUILTIN_TYPES))
    )
}
