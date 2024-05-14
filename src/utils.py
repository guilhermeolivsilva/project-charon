"""General purpose utilities."""


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


def get_variable_name_symbol(variable_name: str) -> str:
    """
    Get the symbol associated with a variable name.

    Parameters
    ----------
    variable_name : str
        The variable name to get its associated symbol.

    Returns
    -------
    : str
        The symbol associated with the given variable.
    """

    symbol_map = {
        "a": "1",
        "b": "2",
        "c": "3",
        "d": "4",
        "e": "5",
        "f": "6",
        "g": "7",
        "h": "8",
        "i": "9",
        "j": "10",
        "k": "11",
        "l": "12",
        "m": "13",
        "n": "14",
        "o": "15",
        "p": "16",
        "q": "17",
        "r": "18",
        "s": "19",
        "t": "20",
        "u": "21",
        "v": "22",
        "w": "23",
        "x": "24",
        "y": "25",
        "z": "26"
    }

    return symbol_map.get(variable_name)