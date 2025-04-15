"""Implement a certificate inverter."""


class Inverter:
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

    @staticmethod
    def preprocess_certificate(certificate: str) -> list[list[int]]:
        """
        TODO
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
