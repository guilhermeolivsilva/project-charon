"""Implement the base class for the certificate inverter."""

from abc import abstractmethod
from typing import Union


class BaseInverter:
    """
    Invert a certificate to retrieve the original program in canonical form.

    Parameters
    ----------
    certificate : str
        The certificate produced from a `Certificator` class.
    """

    def __init__(self, certificate: str) -> None:
        self.original_certificate: str = certificate
        self.certificate: list[list[int]] = self.preprocess_certificate(certificate)

    def preprocess_certificate(self, certificate: str) -> list[dict[str, Union[int, list[int]]]]:
        """
        Preprocess a certificate to split positional primes and symbols.

        The result is returned as a list of dictionaries. Each dictionary has
        three fields: `positional_prime`, `symbol`, and `additional_info`. The
        former two will always have contents, while the latter might not.

        Parameters
        ----------
        certificate : str
            The certificate to process.

        Returns
        -------
        preprocessed_certificate : list[dict[str, Union[int, list[int]]]]
            The preprocessed certificate, as a list of dictionaries.
        """

        # Sort the certificate based on positional primes (i.e., the first
        # element right before the first `^`).
        sorted_certificate = sorted(
            certificate.split("*"),
            key=lambda x: int(x.split("^")[0])
        )

        split_certificate = [
            list(map(int, token.replace("(", "").replace(")", "").split("^")))
            for token in sorted_certificate
        ]

        preprocessed_certificate = [
            {
                "positional_prime": positional_prime,
                "symbol": symbol,
                "additional_info": additional_info
            }
            for positional_prime, symbol, *additional_info in split_certificate
        ]
        
        return preprocessed_certificate
    
    @abstractmethod
    def invert_certificate(self) -> Union[str, dict[str, dict]]:
        """
        Invert the certificate to retrieve the original program.

        The original program is generated in its canonical form.
        """

        raise NotImplementedError
