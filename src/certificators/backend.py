"""Certificator for the frontend representation of Tiny C programs."""

from string import ascii_lowercase
from typing import Union

from src.certificators.abstract_certificator import AbstractCertificator
from src.utils import next_prime


class BackendCertificator(AbstractCertificator):
    """
    Certificate the backend representation of some program.

    Parameters
    ----------
    code_collection : list[dict]
        A list of instructions generated by the CodeGenerator. Refer to this
        class for more details.
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
        super().__init__()

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

    def certificate(self, **kwargs) -> None:
        """
        Certificate the backend code.
        
        This method iterates the code collection to compute the corresponding
        certificate of each instruction, and sets the `certified` field of
        the code metadata to True.
        """

        curr_prime = 1

        for code_metadata in self.code_collection:
            instruction = code_metadata.get("instruction")

            try:
                handler = getattr(self, instruction.lower())
            except AttributeError:
                handler = self.default_handler

            instruction_certificate = handler(curr_prime=curr_prime, **code_metadata)

            # The only instructions that doesn't have its own certificates
            # are EMPTY and JMP, as these are part of some language constructs
            # (namely, WHILE, IF and IF/ELSE).
            if instruction_certificate is None:
                continue

            self.computed_certificate.append(instruction_certificate)
            code_metadata["certified"] = True

            curr_prime = next_prime(curr_prime)

    def get_certificate(self) -> list[str]:
        """
        Get the complete certificate of the frontend code.

        Returns
        -------
        : list[str]
            A list of containing all of the certification labels of the virtual
            machine instructions.
        """
        
        return self.computed_certificate

    def default_handler(self, curr_prime: int, instruction: str, **kwargs) -> str:
        """
        Handle most instructions that doesn't have additional complications.

        Parameters
        ----------
        curr_prime : int
            The current prime being used in the certification process.
        instruction : str
            The instruction. Duh.

        Returns
        -------
        : str
            The certificate of the given instruction.
        """

        return f"{curr_prime}^({self.tokens.get(instruction)})"
    
    def empty(self, **kwargs) -> None:
        """
        Handle the EMPTY instruction.

        Simply, do nothing, because such instructions doesn't have its own
        certificate -- these are part of WHILE, IF or IFELSE constructs.
        """

        return
    
    def ifetch(self, curr_prime: int, value: int, **kwargs) -> str:
        """
        Handle the IFETCH instruction.

        Parameters
        ----------
        curr_prime : int
            The current prime being used in the certification process.
        value : int
            The value associated with the instruction.

        Returns
        -------
        : str
            The certificate of the IFETCH instruction.
        """

        return self._handle_instruction_with_value(
            curr_prime=curr_prime,
            instruction="IFETCH",
            value=value
        )
    
    def ipush(self, curr_prime: int, value: int, **kwargs) -> str:
        """
        Handle the IPUSH instruction.

        Parameters
        ----------
        curr_prime : int
            The current prime being used in the certification process.
        value : int
            The value associated with the instruction.

        Returns
        -------
        : str
            The certificate of the IPUSH instruction.
        """

        return f"{curr_prime}^({self.tokens.get('IPUSH')}^{value})"
    
    def istore(self, curr_prime: int, value: int, **kwargs) -> str:
        """
        Handle the ISTORE instruction.

        Parameters
        ----------
        curr_prime : int
            The current prime being used in the certification process.
        value : int
            The value associated with the instruction.

        Returns
        -------
        : str
            The certificate of the ISTORE instruction.
        """

        return self._handle_instruction_with_value(
            curr_prime=curr_prime,
            instruction="ISTORE",
            value=value
        )

    def jmp(self, **kwargs) -> None:
        """
        Handle the JMP instruction.

        Simply, do nothing, because such instructions doesn't have its own
        certificate -- these are part of WHILE, IF or IFELSE constructs.
        """

        return

    def jz(self, curr_prime: int, idx: int, value: int, **kwargs) -> str:
        """
        Handle the JZ instruction.

        As the JZ instruction is used for many different constructs -- namely,
        WHILE, IF or IFELSE –-, we first identify the semantics of the
        construct, and then certificate it accordingly.

        Parameters
        ----------
        curr_prime : int
            The current prime being used in the certification process.
        idx : int
            The index of the JZ instruction in the `code_collection` list.
        value : int
            The value associated with the instruction.

        Returns
        -------
        : str
            The certificate of the ISTORE instruction.
        """

        exponent = self._identify_conditional_jump(
            conditional_jump_idx=idx,
            conditional_jump_target_id=value
        )

        return f"{curr_prime}^({exponent})"

    def _handle_instruction_with_value(
        self,
        curr_prime: int,
        instruction: str,
        value: int
    ) -> str:
        """
        Handle the instructions with associated values.

        Currently, only IFETCH and ISTORE instructions are handled with this
        method.

        Parameters
        ----------
        curr_prime : int
            The current prime being used in the certification process.
        instruction : str
            The instruction being handled.
        value : int
            The value associated with the instruction.

        Returns
        -------
        : str
            The certificate of the IPUSH instruction.
        """

        base = f"{curr_prime}^"

        exponent = f"({self.tokens.get(instruction)}^{self.tokens.get(value)})"

        return base + exponent

    def _identify_conditional_jump(
        self,
        conditional_jump_idx: int,
        conditional_jump_target_id: int
    ) -> str:
        """
        Identify the semantics of a conditional jump (JZ).

        conditional_jump_idx : int
            The index of the conditional jump instruction.
        conditional_jump_target_id : int
            The ID of the jump target.

        Returns
        -------
        : str
            The certificate of the JZ instruction.
        """

        # find the index of the jump target
        for code_metadata in self.code_collection:
            curr_idx = code_metadata.get("idx")
            curr_id = code_metadata.get("id")

            found_instruction_id = (
                curr_id == conditional_jump_target_id
                and curr_idx != conditional_jump_idx
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
            return self._identify_unconditional_jump(unconditional_jump_idx)
        
        # IF: has no unconditional jump
        else:
            return "36"

    def _identify_unconditional_jump(self, unconditional_jump_idx: int) -> str:
        """
        Identify the semantics of an unconditional jump (JMP).

        This is an auxiliary method used by `_identify_conditional_jump` in
        order to decide whether a JMP is part of WHILE or IFELSE construct.

        unconditional_jump_idx : int
            The index of the unconditional jump instruction.

        Returns
        -------
        : str
            The corresponding symbol of the identified construct.
        """

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
