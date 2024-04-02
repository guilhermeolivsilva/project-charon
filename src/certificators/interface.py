"""Base class for Certificator classes (i.e., back and frontends)."""

from abc import abstractmethod
from string import ascii_lowercase


class Interface:
    """Interface for certificator classes."""

    variables = ascii_lowercase
    literals = [str(literal) for literal in range(0, 10)]

    basic_symbols = [
        *variables,
        *literals
    ]

    @abstractmethod
    def __init__(self, code) -> None:
        pass

    @abstractmethod
    def certificate(self, **kwargs) -> None:
        pass
