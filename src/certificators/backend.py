"""Certificator for the frontend representation of Tiny C programs."""

from string import ascii_lowercase
from typing import Union

from src.certificators.interface import Interface
from src.utils import next_prime


class BackendCertificator(Interface):
    """
    Certificate the backend representation of some program.

    Parameters
    ----------
    code_collection : list[tuple[str, Node]]

    """

    instructions = [
        "EMPTY",
        "IFETCH",
        "IPUSH",
        "ISTORE",
        "IPOP",
        "IADD",
        "ISUB",
        "ILT",
        "HALT",
        "JZ",
        "JMP",
        "JNZ"
    ]

    variables = ascii_lowercase

    symbols = [
        *variables,
        *instructions
    ]

    def __init__(self, code_collection: list[dict[str, Union[int, str, None]]]) -> None:
        self.code_collection: list[dict[str, Union[int, str, None]]] = [
            {
                "idx": idx,
                **bytecode
            }

            for idx, bytecode in enumerate(code_collection)
        ]

        self.tokens: dict = {
            key: value
            for key, value in zip(
                self.symbols,
                range(1, len(self.symbols) + 1)
            )
        }

    def certificate(self, **kwargs) -> None:
        """
        Certificate the backend code.
        
        This method iterates the code collection and adds the corresponding
        label to the `certificate_label` field of each bytecode.
        """

        ...

    def get_certificate(self) -> list[str]:
        
        ...
