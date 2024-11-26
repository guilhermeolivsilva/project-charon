"""Certificator for the frontend representation of Tiny C programs."""

from typing_extensions import override

from src.certificators.abstract_certificator import AbstractCertificator
from src.virtual_machine import VirtualMachine
from src.utils import next_prime


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

        self.program = program
        self.register_tracker: dict[int, dict] = {}

    @override
    def certificate(self, **kwargs) -> list[str]:
        """
        Certificate the backend code.
        
        ...
        """

        ...

    def _track_registers(self) -> None:
        """
        ...
        """

        idx = 0
        instruction_list = [
            *self.program["global_vars"],
            *self.program["code"]
        ]

        while idx < len(instruction_list):
            bytecode = instruction_list[idx]

            instruction = bytecode["instruction"]

            # Early stopping
            if instruction == "HALT":
                break

            metadata = bytecode["metadata"]
            register = metadata["register"]

            source_metadata = {
                "source": instruction
            }

            if instruction in [
                *VirtualMachine.constants_instructions,
                *VirtualMachine.variables_instructions
            ]:
                source_metadata["metadata"] = {
                    "value": metadata["value"]
                }

            elif instruction in VirtualMachine.type_cast_instructions:
                source_metadata["metadata"] = {
                    "operand": metadata["value"]
                }

            elif instruction in VirtualMachine.unops_instructions:
                source_metadata["metadata"] = {
                    "operand": self.register_tracker[metadata["value"]]
                }

            elif instruction in VirtualMachine.binops_instructions:
                source_metadata["metadata"] = {
                    "lhs_operand": self.register_tracker[metadata["lhs_register"]],
                    "rhs_operand": self.register_tracker[metadata["rhs_register"]]
                }

            #TODO: add functions (call, return)
            else:
                print(f"Handler for {instruction} has not been implemented yet")
                idx += 1
                continue

            self.register_tracker[register] = source_metadata
            idx += 1