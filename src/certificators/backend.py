"""Certificator for the frontend representation of [C]haron programs."""

from typing_extensions import override

from src.certificators.abstract_certificator import AbstractCertificator
from src.utils import (
    get_certificate_symbol,
    next_prime,
    previous_prime,
    primes_list,
    INSTRUCTIONS_CATEGORIES,
)


class BackendCertificator(AbstractCertificator):
    """
    Certificate the backend representation of some program.

    Parameters
    ----------
    program : dict[str, dict]
        A dictionary with bytecodes and struct metadata generated from some
        Abstract Syntax Tree representation of a program.
    """

    def __init__(self, program: dict[str, dict]) -> None:
        super().__init__()

        # Input
        self.program = program
        self.bytecode_list = self.program["code"]

        self.current_positional_prime = self.initial_prime
        self.current_variable_prime = self.initial_prime

        _functions_ids = range(1, len(program["functions"]) + 1)
        self.functions_primes: dict[int, int] = {
            function_id: prime
            for function_id, prime in zip(
                _functions_ids, primes_list(len(_functions_ids))
            )
        }

        # Tell whether an instruction has been accounted for in the
        # certification process or not. Maps the ID of `instruction_list` to
        # `True` if already certificated, or `False` otherwise.
        self.instruction_status: dict[int, bool] = {
            bytecode["instruction_id"]: False
            for bytecode in self.bytecode_list
        }

    @override
    def certificate(self, **kwargs) -> str:
        """
        Certificate the backend code.

        This method iterates over the machine code and annotate each instruction
        with its relative position and contents.

        Returns
        -------
        computed_certificate : str
            The computed certificate.
        """

        for bytecode in self.bytecode_list:
            bytecode_id = bytecode["instruction_id"]

            # Skip instructions that have already been certificated.
            if self.instruction_status[bytecode_id]:
                continue

            certificate = self._certificate_instruction(bytecode=bytecode)

            if certificate:
                self.computed_certificate.append(certificate)

            self.current_positional_prime = next_prime(self.current_positional_prime)

        # Assert all the instructions have been accounted for
        _err_msg = "Certification failed: there are uncertificated instructions."
        assert all(self.instruction_status.values()), _err_msg

        self.computed_certificate = "*".join(self.computed_certificate)
        self.computed_certificate = "*".join(
            sorted(
                self.computed_certificate.split("*"),
                key=lambda x: int(x.split("^")[0])
            )
        )

        return self.computed_certificate

    def _certificate_instruction(self, bytecode: dict[str, dict]) -> str:
        """
        Compute the certificate of an instruction.

        This method dispatches the adequate certification method for the given
        instruction.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.

        Returns
        -------
        certificate : str
            The instruction certificate.
        """

        instruction = bytecode["instruction"]

        try:
            certificate = ...

        except KeyError as e:
            print(f"Handler for {instruction} has not been implemented yet")
            print(bytecode)
            print(e)
            raise e

        return certificate
