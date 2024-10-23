"""Base class for Certificator classes (i.e., back and frontends)."""

from abc import abstractmethod


class AbstractCertificator:
    """Base class for certificator classes."""

    def __init__(self, **kwargs) -> None:
        self.computed_certificate: list[str] = []

    @abstractmethod
    def certificate(self, **kwargs) -> list[str]:
        pass

    def get_certificate(self) -> list[str]:
        return self.computed_certificate
