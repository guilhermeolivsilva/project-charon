"""
Annotate statements and instructions with unique IDs.

Statements and instructions that implement the same semantics must have the
same ID. However, no pair of statements must have the same ID -- and the same
goes for instructions.
"""

from string import ascii_lowercase

from src.abstract_syntax_tree import AbstractSyntaxTree
from src.code_generator import CodeGenerator
from src.lexer import Lexer
from src.node import Node


def get_range_of_primes(range_length: int) -> list[int]:
    """
    Generate a list with the first `range_length`-th prime numberbers.

    This function uses D. Eppstein's implementation of the Sieve of
    Eratosthenes to achieve its goal.

    Parameters
    ----------
    range_length : int
        The amount of prime numberbers to generate.

    Returns
    -------
    primes : list[int]
        List with the first `range_length` prime numberbers.
    """

    primes = []

    cache = {}
    current_integer = 2

    while len(primes) <= range_length:
        if current_integer not in cache:
            primes.append(current_integer)
            cache[current_integer * current_integer] = [current_integer]
        else:
            for cached_element in cache[current_integer]:
                cache.setdefault(cached_element + current_integer, []).append(
                    cached_element
                )
            del cache[current_integer]

        current_integer += 1

    return primes


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


class Certificator:
    """
    Certificator that attests whether a frontend source code is correctly
    implemented by its corresponding backend code.

    This Certificator generates unique IDs for each instruction using Gödel's
    numberbering system for both the frontend and backend codes. If the generated
    representations match, then the backend correctly implements the frontend.

    Parameters
    ----------
    frontend_code : AbstractSyntaxTree
        The Abstract Syntax Tree that represents the frontend code.
    backend_code : list[tuple]
        A list of tuples of the backend source code generated by the Tiny-C
        Code Generator.
    """

    variables = ascii_lowercase
    literals = [str(literal) for literal in range(0, 10)]

    frontend_symbols = [
        *AbstractSyntaxTree.node_kinds,
        *variables,
        *literals
    ]

    backend_symbols = [
        *CodeGenerator.instructions,
        *variables,
        *literals
    ]

    def __init__(
        self, frontend_code: AbstractSyntaxTree, backend_code: list[tuple]
    ) -> None:
        self.frontend_code = frontend_code.root
        self.backend_code = backend_code

        self.frontend_tokens = {
            key: value
            for key, value in zip(
                self.frontend_symbols,
                get_range_of_primes(len(self.frontend_symbols))
            )
        }

        self.backend_tokens = {
            key: value
            for key, value in zip(
                self.backend_symbols,
                get_range_of_primes(len(self.backend_symbols))
            )
        }

    def traverse_ast(self):
        """Traverse the AST and annotate each node with its relative position."""

        # Using a list to avoid issues with variable scoping in nested function
        current_prime = [1]

        def traverse(node: Node) -> None:
            if node is None:
                return

            for child in node.children:
                traverse(child)

            current_prime[0] = next_prime(current_prime[0])
            
            node.set_position_in_tree(current_prime[0])

        traverse(self.frontend_code)