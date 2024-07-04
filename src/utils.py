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
