"""General purpose utilities."""

from typing import Union


builtin_types: dict[str, int] = {
    "short": 2,
    "int": 4,
    "float": 4
}


def is_prime(number: int) -> bool:
    """
    Check whether the given `number` is a prime.

    Parameters
    ----------
    number : int
        The number to test.

    Returns
    -------
    : bool
        The verdict.
    """

    if number < 2:
        return False

    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False

    return True


def next_prime(number: int) -> int:
    """
    Compute the next prime immediately after `number`.

    Parameters
    ----------
    number : int
        The reference number.

    Returns
    -------
    next_number : int
        The first prime after `number`.
    """

    next_number = number + 1

    while True:
        if is_prime(next_number):
            return next_number

        next_number += 1


def primes_list(length: int) -> list[int]:
    """
    Compute a list of prime numbers with a given `length`.

    The list always starts at 2.

    Parameters
    ----------
    length : int
        The length of the list.

    Returns
    -------
    primes : list[int]
        A list of integers containing the specified amount of primes.
    """

    _primes: set[int] = set()
    current_number = 1

    while len(_primes) < length:
        _primes.add(next_prime(current_number))
        current_number += 1

    primes = list(_primes)

    return primes


def type_cast(original_type: str, target_type: str, register: int) -> tuple[
    int,
    list[dict[str, str]]
]:
    """
    Compute a type cast instruction from `original_type` to `target_type`.

    Notice that casts from `short` to `float` (and vice-and-versa) are not
    direct. First, we must cast to `int`, and then to the actual `target_type`.
    Thus, the returned `code` list will contain two instructions.

    The other possible casts (`short` to `int`, `int` to `short`, `int` to
    `float`, and `float` to `int`) happen directly, and only generate a single
    instruction. (`code`, in this case, is a list with a single item.)

    Parameters
    ----------
    original_type : str
        The original type, to cast from.
    target_type : str
        The target type, to cast to.
    register : int
        The register to be allocated to this instruction.

    Returns
    -------
    register : int
        The number of the next register available.
    code : list[dict]
        The code metadata of the `TYPECAST` instruction.
    """

    # Direct casts
    _default_metadata = {
        "metadata": {
            "register": register - 1,
            "value": register
        }
    }

    cast_instruction_map: dict[dict, Union[str, dict]] = {
        "short": {
            "int": {
                "instruction": "SIGNEXT",
                **_default_metadata
            }
        },
        "int": {
            "short": {
                "instruction": "TRUNC",
                **_default_metadata
            },
            "float": {
                "instruction": "SITOFP",
                **_default_metadata
            }
        },
        "float": {
            "int": {
                "instruction": "FPTOSI",
                **_default_metadata
            }
        }
    }

    code: list[dict[str, str]] = []

    # Short <-> float is indirect. Thus, use a recursive approach to address
    # the registers numbers
    if original_type == "short" and target_type == "float":
        short_to_int = cast_instruction_map["short"]["int"]
        code.append(short_to_int)

        register, int_to_float = type_cast(
            original_type="int",
            target_type="float",
            register=register + 1
        )
        code.extend(int_to_float)

    elif original_type == "float" and target_type == "short":
        float_to_int = cast_instruction_map["float"]["int"]
        code.append(float_to_int)

        register, int_to_short = type_cast(
            original_type="int",
            target_type="short",
            register=register + 1
        )
        code.extend(int_to_short)

    else:
        direct_cast = cast_instruction_map[original_type][target_type]
        code.append(direct_cast)
        register += 1

    return register, code


def get_variable_size(variable_metadata: dict) -> int:
    """
    Get the size of a variable, in bytes, from its type.

    Parameters
    ----------
    variable_metadata : dict
        Dictionary of variable metadata exported by the Lexer.

    Returns
    -------
    var_size : int
        The size of the variable type, in bytes.
    """

    var_size: int = 0
    var_type: str = variable_metadata["type"]
    var_length: str = variable_metadata.get("length", 1)

    # Case 1: variable is of a built-in type
    if var_type in builtin_types:
        var_size = builtin_types[var_type]

        return var_size * var_length

    # Case 2: variable is a struct
    struct_attr_types = [
        attr["type"] for attr in variable_metadata["attributes"].values()
    ]

    for attr_type in struct_attr_types:
        var_size += get_variable_size({"type": attr_type})

    return var_size * var_length


__NODES = [
    "CST",
    "VAR_DEF",
    "VAR_VALUE",
    "VAR_ADDRESS",
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
    "LSHIFT",
    "RSHIFT",
    "BITAND",
    "BITOR",
    "NOT",
    "IF",
    "IFELSE",
    "WHILE",
    "DO"
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
        builtin_types.keys(),
        primes_list(len(builtin_types.keys()))
    )
}
