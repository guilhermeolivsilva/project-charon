"""Certificator for the frontend representation of Tiny C programs."""

from typing_extensions import override

from src.certificators.abstract_certificator import AbstractCertificator
from src.utils import next_prime, INSTRUCTIONS_CATEGORIES


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

            try:
                if instruction in [
                    *INSTRUCTIONS_CATEGORIES["constants"],
                    *INSTRUCTIONS_CATEGORIES["variables"]
                ]:
                    source_metadata["metadata"] = {
                        "value": metadata["value"]
                    }

                elif instruction in INSTRUCTIONS_CATEGORIES["type_casts"]:
                    source_metadata["metadata"] = {
                        "operand": metadata["value"]
                    }

                elif instruction in INSTRUCTIONS_CATEGORIES["unops"]:
                    source_metadata["metadata"] = {
                        "operand": self.register_tracker[metadata["value"]]
                    }

                elif instruction in INSTRUCTIONS_CATEGORIES["binops"]:
                    source_metadata["metadata"] = {
                        "lhs_operand": self.register_tracker[metadata["lhs_register"]],
                        "rhs_operand": self.register_tracker[metadata["rhs_register"]]
                    }

            except KeyError:
                print(f"Handler for {instruction} has not been implemented yet")
                idx += 1
                continue

            self.register_tracker[register] = source_metadata
            idx += 1

    def _identify_jz(self, instruction: dict[str, dict], index: int) -> str:
        """
        TODO
        """

        _jump_size: int = instruction["metadata"]["jump_size"]
        
        _instruction_right_before_jump_target_idx = index + _jump_size - 1

        _jumps_forward = self._is_jump_forward(index)
        _lands_on_instruction_preceeded_by_unconditional_jump = self._is_unconditional_jump(_instruction_right_before_jump_target_idx)

        if _jumps_forward:
            if _lands_on_instruction_preceeded_by_unconditional_jump:
                _preceeding_unconditional_jump_is_forward = self._is_jump_forward(_instruction_right_before_jump_target_idx)
                
                if _preceeding_unconditional_jump_is_forward:
                    return "if else"
                else:
                    return "while"
            else:
                return "if"
        else:
            return "do while"

    def _is_jump_forward(self, instruction_idx: int) -> bool:
        """
        TODO
        """

        instruction = self.program["code"][instruction_idx]

        return (
            "jump_size" in instruction["metadata"]
            and instruction["metadata"]["jump_size"] > 0
        )

    def _is_unconditional_jump(self, instruction_idx: int) -> bool:
        """
        TODO
        """

        instruction = self.program["code"][instruction_idx]

        return (
            "conditional_register" in instruction["metadata"]
            and instruction["metadata"]["conditional_register"] == "zero"
        )