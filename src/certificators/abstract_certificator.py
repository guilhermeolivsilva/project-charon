"""Base class for Certificator classes (i.e., back and frontends)."""

from abc import abstractmethod


class AbstractCertificator:
    """Base class for certificator classes."""

    def __init__(self, **kwargs) -> None:
        self.computed_certificate: list[str] = []
        self.initial_prime: int = 2

    @abstractmethod
    def certificate(self, **kwargs) -> str:
        pass

    def get_certificate(self) -> str:
        return self.computed_certificate
