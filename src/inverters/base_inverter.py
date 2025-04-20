"""Implement the base class for the certificate inverter."""

from abc import abstractmethod
from typing import Union

from src.utils import INVERTED_SYMBOLS_MAP


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
        self.certificate: list[dict[str, Union[str, dict]]] = self._preprocess_certificate()
        self.ir: list[dict[str, Union[str, dict]]] = self._get_intermediate_representation()

    def _preprocess_certificate(self) -> list[dict[str, Union[int, list[int]]]]:
        """
        Preprocess a certificate to split positional primes and symbols.

        The result is returned as a list of dictionaries. Each dictionary has
        three fields: `positional_prime`, `symbol`, and `additional_info`. The
        former two will always have contents, while the latter might not.

        Returns
        -------
        preprocessed_certificate : list[dict[str, Union[int, list[int]]]]
            The preprocessed certificate, as a list of dictionaries.
        """

        # Sort the certificate based on positional primes (i.e., the first
        # element right before the first `^`).
        sorted_certificate = sorted(
            self.original_certificate.split("*"),
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
    
    def _get_intermediate_representation(self) -> list[dict[str, Union[str, dict]]]:
        """
        Get an Intermediate Representation (IR) for the encoded program.

        The IR uses a series of more verbose tokens to represent the program.

        Returns
        -------
        ir : list[dict[str, Union[str, dict]]]
            The Intermediate Representation.
        """

        ir = []

        op_handlers = {
            "CST": self.__handle_constant,
            "VAR_DEF": self.__handle_variable_definition,
            "VAR_ADDRESS": self.__handle_variable,
            "VAR_VALUE": self.__handle_variable,
        }

        for certificate_token in self.certificate:
            op = INVERTED_SYMBOLS_MAP[certificate_token["symbol"]]

            # Handle symbols that contain additional parameters
            if op in op_handlers:
                op_handler = op_handlers[op]
                op_metadata = op_handler(certificate_token)

            else:
                op_metadata = {}

            ir.append({"operation": op, "metadata": op_metadata})

        return ir

    def __handle_constant(self, certificate_token: dict[str, Union[str, dict]]) -> dict[str, Union[str, dict]]:
        """Handle a certificate token that represents a constant."""

        constant_value = certificate_token["additional_info"].pop()

        # Constants are always added with 1 to prevent the exponentiation identity
        constant_value -= 1

        return {
            "value": constant_value
        }

    def __handle_variable_definition(self, certificate_token: dict[str, Union[str, dict]]) -> dict[str, Union[str, dict]]:
        """Handle a certificate token that represents a variable definition."""

        # TODO: handle types
        variable_prime, size = certificate_token["additional_info"]

        return {
            "variable_prime": variable_prime,
            "size": size
        }

    def __handle_variable(self, certificate_token: dict[str, Union[str, dict]]) -> dict[str, Union[str, dict]]:
        """Handle a certificate token that represents a variable."""

        (
            variable_prime,
            _access_type,
            _access_offset_or_var
        ) = certificate_token["additional_info"]

        # Static access (i.e., array indexed with constant or struct)
        if _access_type == 2:
            access_type = "static"

            # Offset is added with 1 to prevent the exponentiation identity
            offset = _access_offset_or_var - 1

            return {
                "variable_prime": variable_prime,
                "access_type": access_type,
                "offset": offset
            }

        # Dynamic access (i.e., array indexed with variable)
        access_type = "dynamic"
        indexing_variable_prime = _access_offset_or_var

        return {
            "variable_prime": variable_prime,
            "access_type": access_type,
            "indexing_variable_prime": indexing_variable_prime
        }

    @abstractmethod
    def get_program(self) -> Union[str, dict[str, dict]]:
        """Get the canonical form of the program."""

        raise NotImplementedError
