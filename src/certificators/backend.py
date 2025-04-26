"""Certificator for the frontend representation of [C]haron programs."""

from typing_extensions import override

from src.certificators.abstract_certificator import AbstractCertificator
from src.utils import (
    get_certificate_symbol,
    next_prime,
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

        self.environment = {
            "variables": {},
        }

        # Tell whether an instruction has been accounted for in the
        # certification process or not. Maps the ID of `instruction_list` to
        # `True` if already certificated, or `False` otherwise.
        self.instruction_status: dict[int, bool] = {
            bytecode["instruction_id"]: False
            for bytecode in self.bytecode_list
        }

        self.bytecode_handlers = {
            # Instructions that might implement more than 1 operation
            "CONSTANT": self._handle_constant,
            "MOV": self._handle_mov,

            # 1:1 instructions
            **{
                binop: self._handle_simple_instruction
                for binop in INSTRUCTIONS_CATEGORIES["binops"]
            },
            **{
                unop: self._handle_simple_instruction
                for unop in INSTRUCTIONS_CATEGORIES["unops"]
            },
            **{
                misc: self._handle_simple_instruction
                for misc in INSTRUCTIONS_CATEGORIES["misc"]
            },
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

        for idx, bytecode in enumerate(self.bytecode_list):
            bytecode_id = bytecode["instruction_id"]

            # Skip instructions that have already been certificated.
            if self.instruction_status[bytecode_id]:
                continue

            certificate = self._certificate_instruction(
                bytecode=bytecode,
                bytecode_idx=idx
            )

            self.computed_certificate.append(certificate)

        # Assert all the instructions have been accounted for
        _err_msg = "Certification failed: there are uncertificated instructions."
        if not(all(self.instruction_status.values())):
            print(_err_msg)
            print("Instruction IDs with missing certificates:")
            print([
                instruction_id
                for instruction_id, status in self.instruction_status.items()
                if not status
            ])

        self.computed_certificate = "*".join(self.computed_certificate)
        self.computed_certificate = "*".join(
            sorted(
                self.computed_certificate.split("*"),
                key=lambda x: int(x.split("^")[0])
            )
        )

        return self.computed_certificate

    def _certificate_instruction(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> str:
        """
        Compute the certificate of an instruction.

        This method dispatches the adequate certification method for the given
        instruction.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        certificate : str
            The instruction certificate.
        """

        instruction = bytecode["instruction"]

        try:
            bytecode_handler = self.bytecode_handlers[instruction]
            certificate = bytecode_handler(
                bytecode=bytecode,
                bytecode_idx=bytecode_idx
            )

        except KeyError as e:
            print(f"Handler for {instruction} has not been implemented yet")
            print(bytecode)
            print(e)
            raise e

        return certificate

    def _handle_constant(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> str:
        """
        Handle a `CONSTANT` bytecode.

        This bytecode might mean 4 things:

        1. If followed by `ADD r_add r_constant zero; LOAD(F) r_var r_add`, it
        is loading the value of a variable into a register;
        2. If followed by `ADD r_add r_constant zero`, it is loading the address
        of a variable into a register;
        3. If followed by `STORE(F) r_constant arg`, it is passing the value of
        an argument to a function parameter;
        4. It is a simple constant that will be used in an expression.

        So we must handle it accordingly.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The `CONSTANT` instruction bytecode.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        certificate : str
            The certificate of operation this `CONSTANT` implements.
        """

        # Figure out what operation it implements
        next_bytecode = self.bytecode_list[bytecode_idx + 1]
        next_bytecode_idx = bytecode_idx + 1

        # Cases 1 or 2: variable value/address
        is_variable = (
            next_bytecode["instruction"] == "ADD"
            and next_bytecode["metadata"]["rhs_register"] == "zero"
        )

        is_argument = (
            next_bytecode["instruction"] in ["STORE", "STOREF"]
            and next_bytecode["metadata"]["value"] == "arg"
        )

        if is_variable:
            following_bytecode = self.bytecode_list[next_bytecode_idx + 1]

            is_variable_value = (
                following_bytecode["instruction"] in ["LOAD", "LOADF"]
            )

            return self.__handle_variable(
                bytecode=bytecode,
                bytecode_idx=bytecode_idx,
                context="value" if is_variable_value else "address"
            )

        # Case 3: passing value to argument
        elif is_argument:
            return ...
        
        # Case 4: just a constant
        constant_value = bytecode["metadata"]["value"] + 1 # Avoid exp. identity
        symbol = get_certificate_symbol("CST")
        certificate = (
            f"{self.current_positional_prime}^("
            + f"({symbol})"
            + f"^({constant_value}))"
        )

        # Post-certification steps
        # Mark the involved instruction as done.
        self.instruction_status[bytecode["instruction_id"]] = True

        # Advance the positional prime
        self.current_positional_prime = next_prime(self.current_positional_prime)

        return certificate

    def __handle_variable(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int,
        context: str
    ) -> str:
        """
        TODO: docstring.
        TODO: handle structs/arrays.
        """

        # The `CONSTANT` instruction has the variable address as its value.
        var_address = bytecode["metadata"]["value"]

        # Produce the certificate
        symbol = get_certificate_symbol(f"VAR_{context.upper()}")

        # Get (and, possibly, set) the variable prime.
        if var_address in self.environment["variables"]:
            var_prime = self.environment["variables"][var_address]["prime"]
        else:
            var_prime = self.current_variable_prime
            self.environment["variables"][var_address] = {
                "prime": var_prime
            }

            self.current_variable_prime = next_prime(
                self.current_variable_prime
            )

        exponent = (
            f"({symbol})"
            + f"^({var_prime})"
            + "^(2)"
            + "^(1)"
        )

        certificate = f"{self.current_positional_prime}^({exponent})"

        # Post-certification steps
        # Mark the involved instructions as done.
        if context == "address":
            # Mark `CONSTANT` and `ADD` as done.
            instructions_to_mark_as_done = 2

        else:
            # Mark `CONSTANT`, `ADD`, and `LOAD` as done.
            instructions_to_mark_as_done = 3

            # If this variable is `short`-typed, also mark the type cast as done.
            if self.bytecode_list[bytecode_idx + 3]["instruction"] == "TRUNC":
                instructions_to_mark_as_done += 1

        for idx in range(bytecode_idx, bytecode_idx + instructions_to_mark_as_done):
            bytecode_id = self.bytecode_list[idx]["instruction_id"]
            self.instruction_status[bytecode_id] = True

        # Advance the positional prime
        self.current_positional_prime = next_prime(self.current_positional_prime)

        return certificate
    
    def _handle_mov(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> str:
        """
        TODO: docstring
        TODO: arg/func call
        """

        # Case 1: it is a `return` statement
        is_return = (bytecode["metadata"]["register"] == "ret_value")

        if is_return:
            return self.__handle_return(
                bytecode=bytecode,
                bytecode_idx=bytecode_idx
            )
        
    def __handle_return(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> str:

        # Produce the certificate
        symbol = get_certificate_symbol("RET_SYM")
        exponent = f"({symbol})"
        certificate = f"{self.current_positional_prime}^({exponent})"

        # Post-certification steps
        # Mark this instruction and the next -- `JR` -- as done.
        current_instruction_id = bytecode["instruction_id"]
        self.instruction_status[current_instruction_id] = True

        next_instruction_id = self.bytecode_list[bytecode_idx + 1]["instruction_id"]
        self.instruction_status[next_instruction_id] = True

        # Advance the positional prime
        self.current_positional_prime = next_prime(self.current_positional_prime)

        return certificate

    def _handle_simple_instruction(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> str:
        """
        TODO: docstring
        TODO: handle type casts
        """

        instruction = bytecode["instruction"]

        # Produce the certificate
        symbol = get_certificate_symbol(instruction)
        certificate = f"{self.current_positional_prime}^({symbol})"

        # Post-certification steps
        # Mark this instruction as done.
        instruction_id = bytecode["instruction_id"]
        self.instruction_status[instruction_id] = True

        # Advance the positional prime
        self.current_positional_prime = next_prime(self.current_positional_prime)

        return certificate
