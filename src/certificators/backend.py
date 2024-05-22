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

    instructions = {
        'SEQ': 27,
        'IFETCH': 28,
        'IPUSH': 29,
        'ISTORE': 30,
        'IPOP': 31,
        'IADD': 32,
        'ISUB': 33,
        'ILT': 34,
        'HALT': 35,
        'JNZ': 39
    }

    variables = {
        char: idx + 1
        for idx, char in enumerate(ascii_lowercase)
    }

    def __init__(self, code_collection: list[dict[str, Union[int, str, None]]]) -> None:
        self.code_collection: list[dict[str, Union[int, str, None]]] = [
            {
                "idx": idx,
                **bytecode,
                "certified": False
            }

            for idx, bytecode in enumerate(code_collection)
        ]

        self.tokens: dict[str, int] = {
            **self.variables,
            **self.instructions
        }

        self.computed_certificate: list[str] = []

    def certificate(self, **kwargs) -> None:
        """
        Certificate the backend code.
        
        This method iterates the code collection and adds the corresponding
        label to the `certificate_label` field of each bytecode.
        """

        curr_prime = 1

        for code_metadata in self.code_collection:
            instruction = code_metadata.get("instruction")

            try:
                handler = getattr(self, instruction.lower())
            except AttributeError:
                handler = self.default_handler

            instruction_certificate = handler(curr_prime, **code_metadata)

            if instruction_certificate is None:
                continue

            self.computed_certificate.append(instruction_certificate)

            curr_prime = next_prime(curr_prime)

    def default_handler(self, curr_prime: int, instruction: str, **kwargs) -> str:

        return f"{curr_prime}^({self.tokens.get(instruction)})"
    
    def empty(self, curr_prime: int, **kwargs) -> None:

        return
    
    def ifetch(self, curr_prime: int, value: int, **kwargs) -> str:

        return self._handle_instruction_with_value(
            curr_prime=curr_prime,
            instruction="IFETCH",
            value=value
        )
    
    def ipush(self, curr_prime: int, value: int, **kwargs) -> str:

        return f"{curr_prime}^({self.tokens.get('IPUSH')}^{value})"
    
    def istore(self, curr_prime: int, value: int, **kwargs) -> str:

        return self._handle_instruction_with_value(
            curr_prime=curr_prime,
            instruction="ISTORE",
            value=value
        )

    def jmp(self, curr_prime: int, **kwargs) -> None:

        return

    def jz(self, curr_prime: int, id: int, value: int, **kwargs) -> str:

        exponent = self._classify_conditional_jump(
            conditional_jump_id=id,
            conditional_jump_target_id=value
        )

        return f"{curr_prime}^({exponent})"

    def get_certificate(self) -> list[str]:
        
        return self.computed_certificate

    def _handle_instruction_with_value(self, curr_prime: int, instruction: str, value: int) -> str:

        return f"{curr_prime}^({self.tokens.get(instruction)}^{self.tokens.get(value)})"

    def _classify_conditional_jump(self, conditional_jump_id: int, conditional_jump_target_id: int) -> str:
        # find the index of the jump target
        for code_metadata in self.code_collection:
            curr_idx = code_metadata.get("idx")
            curr_id = code_metadata.get("id")

            found_instruction_id = (
                curr_id == conditional_jump_target_id
                and curr_idx != conditional_jump_id
            )

            if found_instruction_id:
                conditional_jump_target_idx = curr_idx
                break

        # IFELSE/WHILE has unconditional jump pointing to a forward/backward
        # instruction. for both IFELSE and WHILE, the jump points to EMPTY
        # that comes immediately after a JMP
        jmp_before_empty = (
            self.code_collection[conditional_jump_target_idx - 1].get("instruction") == "JMP"
        )

        if jmp_before_empty:
            unconditional_jump_idx = conditional_jump_target_idx - 1
            self.code_collection[conditional_jump_target_idx]["certified"] = True
            return self._classify_unconditional_jump(unconditional_jump_idx)
        
        # IF: has no unconditional jump
        else:
            return "36"

    def _classify_unconditional_jump(self, unconditional_jump_idx: int) -> str:
        unconditional_jump_target = self.code_collection[unconditional_jump_idx].get("value")

        for code_metadata in self.code_collection:
            idx = code_metadata.get("idx")
            id = code_metadata.get("id")

            if id == unconditional_jump_target and idx != unconditional_jump_idx:
                unconditional_jump_target_idx = idx
                break

        if unconditional_jump_idx < unconditional_jump_target_idx:
            symbol = "37"
        else:
            symbol = "38"

        self.code_collection[unconditional_jump_idx]["certified"] = True

        return symbol
