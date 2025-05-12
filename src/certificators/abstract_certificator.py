"""Base class for Certificator classes (i.e., back and frontends)."""

from abc import abstractmethod


class AbstractCertificator:
    """Base class for certificator classes."""

    def __init__(self, **kwargs) -> None:
        self.computed_certificate: list[str] = []
        self.current_prime: int = 2

        # The environment maps variables primes to symbols that represents their
        # associated types. `int x[2]` will be mapped to [3, 3], and
        # `struct { int x; float y; }` will be mapped to [3, 5]. (3 represents
        # integers, and 5 represents floating point numbers.)
        self.environment: dict[int, int] = {}

    @abstractmethod
    def certificate(self, **kwargs) -> str:
        pass

    def get_certificate(self) -> str:
        return self.computed_certificate
