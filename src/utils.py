"""General purpose utilities."""

from typing import Union


builtin_types: dict[str, int] = {"short": 2, "int": 4, "float": 4}


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

    for i in range(2, int(number**0.5) + 1):
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


def previous_prime(number: int) -> int:
    """
    Compute the prime immediately before `number`.

    Parameters
    ----------
    number : int
        The reference number.

    Returns
    -------
    next_number : int
        The first prime before `number`.
    """

    previous_number = number - 1

    while True:
        if is_prime(previous_number):
            return previous_number

        previous_number -= 1


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


def add_variable_to_environment(
    environment: dict[str, dict[int, str]], var_id: int, size: int
) -> dict[str, dict[int, str]]:
    """
    Add a new variable to the environment.

    Parameters
    ----------
    environment : dict[int, str]
        The compiler's environment, that maps variables IDs to memory
        addresses and function IDs to instructions indices.
    var_id : int
        The unique identifier of this variable.
    size : int
        The variable size, in bytes.

    Returns
    -------
    environment : dict[str, dict[int, str]]
        The updated environment.
    """

    # If no variables are defined in the environment, the dict will be empty
    # and we manually set the ID and address.
    variable_count = len(environment["variables"])

    if not variable_count:
        new_var_address = hex(0)
    else:
        last_var_id = list(environment["variables"]).pop()
        last_var_address = environment["variables"][last_var_id]["address"]
        last_var_size = environment["variables"][last_var_id]["size"]
        new_var_address = hex(int(last_var_address, 16) + last_var_size)

    environment["variables"][var_id] = {
        "address": new_var_address,
        "size": size
    }

    return environment


def type_cast(
    original_type: str, target_type: str, register: int
) -> tuple[list[dict[str, str]], int]:
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
    _default_metadata = {"metadata": {"register": register, "value": register - 1}}

    cast_instruction_map: dict[dict, Union[str, dict]] = {
        "short": {"int": {"instruction": "SIGNEXT", **_default_metadata}},
        "int": {
            "short": {"instruction": "TRUNC", **_default_metadata},
            "float": {"instruction": "SITOFP", **_default_metadata},
        },
        "float": {"int": {"instruction": "FPTOSI", **_default_metadata}},
    }

    code: list[dict[str, str]] = []

    # Short <-> float is indirect. Thus, use a recursive approach to address
    # the registers numbers
    if original_type == "short" and target_type == "float":
        short_to_int = cast_instruction_map["short"]["int"]
        code.append(short_to_int)

        int_to_float, register = type_cast(
            original_type="int", target_type="float", register=register + 1
        )
        code.extend(int_to_float)

    elif original_type == "float" and target_type == "short":
        float_to_int = cast_instruction_map["float"]["int"]
        code.append(float_to_int)

        int_to_short, register = type_cast(
            original_type="int", target_type="short", register=register + 1
        )
        code.extend(int_to_short)

    else:
        direct_cast = cast_instruction_map[original_type][target_type]
        code.append(direct_cast)
        register += 1

    return code, register


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


def flatten_list(list_of_lists: list[list], drop_duplicates: bool = True) -> list:
    """
    Flatten a list of lists into a single list.

    Parameters
    ----------
    list_of_lists : list[list]
        The list to be flattened.
    drop_duplicates : bool (optional, default = True)
        Whether or not duplicates should be removed from the final list.

    Returns
    -------
    flattened_list : list
        The flattened list.
    """

    flattened_list = [element for _list in list_of_lists.values() for element in _list]

    if drop_duplicates:
        flattened_list = list(set(flattened_list))

    return flattened_list


__TYPE_CASTS = ["FPTOSI", "SIGNEXT", "SITOFP", "TRUNC"]


__VARIABLES = {"VAR_DEF": ["ALLOC"], "VAR_VALUE": ["LOAD"], "VAR_ADDRESS": ["ADDRESS"]}


__CONSTANTS = {"CST": ["CONSTANT"]}


__UNOPS = {"ASSIGN": ["STORE"], "NOT": ["NOT"]}


__BINOPS = {
    "ADD": ["ADD", "FADD"],
    "SUB": ["SUB", "FSUB"],
    "MULT": ["MULT", "FMULT"],
    "DIV": ["DIV", "FDIV"],
    "MOD": ["MOD"],
    "LESS": ["LT", "FLT"],
    "GREATER": ["GT", "FGT"],
    "EQUAL": ["EQ", "FEQ"],
    "DIFF": ["NEQ", "FNEQ"],
    "AND": ["AND", "FAND"],
    "OR": ["OR", "FOR"],
    "LSHIFT": ["LSHIFT"],
    "RSHIFT": ["RSHIFT"],
    "BITAND": ["BITAND"],
    "BITOR": ["BITOR"],
}

__OPERATIONS = {**__UNOPS, **__BINOPS}


__JUMPS = {
    "FUNC_CALL": ["JAL", "MOV"],
    "RET_SYM": ["MOV", "JR"],
    "IF": ["JZ"],
    "IFELSE": ["JZ"],
    "WHILE": ["JZ"],
}


__FUNCTIONS = {"PARAM": ["ALLOC", "STORE"], "ARG": ["MOV"]}


__MISC = {"PROG": ["HALT"]}


# Nodes kinds and their associated instructions
NODE_TO_INSTRUCTION_MAPPING = {
    **__CONSTANTS,
    **__VARIABLES,
    **__FUNCTIONS,
    **__JUMPS,
    **__UNOPS,
    **__BINOPS,
    **__MISC,
}

INSTRUCTION_OPERATION_TO_NODE_MAPPING = {
    instruction: node
    for node, instructions in __OPERATIONS.items()
    for instruction in instructions
}


INSTRUCTIONS_CATEGORIES = {
    "constants": flatten_list(__CONSTANTS),
    "variables": flatten_list(__VARIABLES),
    "functions": flatten_list(__FUNCTIONS),
    "jumps": flatten_list(__JUMPS),
    "unops": flatten_list(__UNOPS),
    "binops": flatten_list(__BINOPS),
    "misc": flatten_list(__MISC),
    "type_casts": __TYPE_CASTS,
}


SYMBOLS_MAP = {
    certificate: str(base)
    for certificate, base in zip(
        NODE_TO_INSTRUCTION_MAPPING.keys(),
        primes_list(len(NODE_TO_INSTRUCTION_MAPPING.keys())),
    )
}


TYPE_SYMBOLS_MAP = {
    _type: {"type_symbol": base, "enforce": float if _type == "float" else int}
    for _type, base in zip(builtin_types.keys(), primes_list(len(builtin_types.keys())))
}


def get_certificate_symbol(operation) -> str:
    """
    Get the certificate symbol associated with the given operation.

    Parameters
    ----------
    operation : str or Node
        The operation to get the certificate symbol of.

    Returns
    -------
    : str
        The associated certificate symbol.
    """

    # This is ugly.
    if not isinstance(operation, str):
        operation = type(operation).__name__

    # Handle operations instructions
    if operation in INSTRUCTION_OPERATION_TO_NODE_MAPPING.keys():
        operation = INSTRUCTION_OPERATION_TO_NODE_MAPPING.get(operation)

    return SYMBOLS_MAP.get(operation)
