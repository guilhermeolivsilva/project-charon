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

        # Input
        self.program = program
        self.instruction_list = [
            *self.program["global_vars"],
            *self.program["code"]
        ]

        # Track the origin of a register's contents
        self.register_tracker: dict[int, dict] = {}

        # Tell whether an instruction has been accounted for in the
        # certification process or not. Maps the index of `instruction_list`
        # to `True` if already certified, or `False` otherwise.
        self.instruction_status: dict[int, bool] = {}

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

        while idx < len(self.instruction_list):
            bytecode = self.instruction_list[idx]

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
        Tell the semantics of a conditional jump.

        Conditional jumps are used to implement four control flow constructs:
        `if`, `if/else`, `while`, and `do/while`. As the certification considers
        what kind of control flow is being used, this method aims to identify
        the construct based on the pattern of its context.

        Parameters
        ----------
        instruction : dict[str, dict]
            The instruction and its bytecode metadata.
        index : int
            The index of `instruction` in `self.instruction_list`.

        Returns
        -------
        : str (values="IF", "IFELSE", "WHILE", "DO")
            The semantics of the conditional jump.
        """

        _jump_size: int = instruction["metadata"]["jump_size"]
        
        _instruction_right_before_jump_target_idx = index + _jump_size - 1

        _jumps_forward = self._is_jump_forward(index)
        _lands_on_instruction_preceeded_by_unconditional_jump = self._is_unconditional_jump(
            _instruction_right_before_jump_target_idx
        )

        if _jumps_forward:
            if _lands_on_instruction_preceeded_by_unconditional_jump:
                _preceeding_unconditional_jump_is_forward = self._is_jump_forward(
                    _instruction_right_before_jump_target_idx
                )
                
                if _preceeding_unconditional_jump_is_forward:
                    return "IFELSE"
                else:
                    return "WHILE"
            else:
                return "IF"
        else:
            return "DO"

    def _is_jump_forward(self, instruction_idx: int) -> bool:
        """
        Tell whether a jump instruction goes forward or backwards.

        Parameters
        ----------
        instruction_idx : int
            The index of the jump instruction in `self.instruction_list`.

        Returns
        -------
        : bool
            True if the jump is forward (`jump_size` > 0), False otherwise.
        """

        instruction = self.instruction_list[instruction_idx]

        return (
            "jump_size" in instruction["metadata"]
            and instruction["metadata"]["jump_size"] > 0
        )

    def _is_unconditional_jump(self, instruction_idx: int) -> bool:
        """
        Tell whether a conditional jump actually implements an unconditional one.
        
        Such jumps are `JZ` instructions that use the `zero` register as the
        condition. This register will always contain `0`, and thus the jump
        always occur.

        Parameters
        ----------
        instruction_idx : int
            The index of the jump instruction in `self.instruction_list`.

        Returns
        -------
        : bool
            True if the jump is unconditional, False otherwise.
        """

        instruction = self.instruction_list[instruction_idx]

        return (
            "conditional_register" in instruction["metadata"]
            and instruction["metadata"]["conditional_register"] == "zero"
        )