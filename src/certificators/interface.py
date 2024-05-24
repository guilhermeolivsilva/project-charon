"""Base class for Certificator classes (i.e., back and frontends)."""

from abc import abstractmethod


class Interface:
    """Interface for certificator classes."""

    def __init__(self, **kwargs) -> None:
        self.computed_certificate: list[str] = []

    @abstractmethod
    def certificate(self, **kwargs) -> None:
        pass

    @abstractmethod
    def get_certificate(self) -> list[str]:
        pass
