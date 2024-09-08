"""General purpose utilities."""

from typing import Union


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
    Compute a TYPECAST instruction from some `original_type` to a `target_type`.

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
    code : dict
        The code metadata of the `TYPECAST` instruction.

    TODO
    ----
    Implement the actual type cast instructions:

    from short
    - to int: signext i16 to i32
    - to float: signext i16 to i32, sitofp

    from int
    - to short: trunc i32 to i16
    - to float: sitofp

    from float
    - to short: fptosi float to i16
    - to int: fptosi float to i32
    """

    code: dict[str, Union[str, dict]] = {
        "instruction": "TYPECAST",
        "metadata": {
            "original_register": register - 1,
            "original_type": original_type,
            "target_register": register,
            "target_type": target_type
        }
    }

    return register + 1, [code]
