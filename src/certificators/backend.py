"""Certificator for the frontend representation of [C]haron programs."""

from typing import Union

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

        # self.computed_certificate = "*".join(self.computed_certificate)
        # self.computed_certificate = "*".join(
        #     sorted(
        #         self.computed_certificate.split("*"),
        #         key=lambda x: int(x.split("^")[0])
        #     )
        # )

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
            The bytecode to certificate.
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
            The `CONSTANT` bytecode.
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
            return self.__handle_variable(
                bytecode=bytecode,
                bytecode_idx=bytecode_idx
            )

        # Case 3: passing value to argument
        elif is_argument:
            # TODO
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
    ) -> str:
        """
        Handle a variable use case.

        This method will return the appropriate certificate depending on the
        variable kind (simple, struct/array, or array with dynamic indexing),
        and whether it is being read from or written to.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The initial bytecode that implements this variable usage.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        certificate : str
            The certificate of this variable usage.
        """

        # Speculate if this is an array or struct and compute the exponent and
        # the number of instructions that implemented it based on the following
        # bytecodes
        next_bytecode_idx = bytecode_idx + 1

        exponent, instructions_to_mark_as_done = self.__speculate_data_structure(
            bytecode=bytecode,
            bytecode_idx=bytecode_idx,
        )

        # If not an array or struct, certificate as a simple variable.
        if not all([exponent, instructions_to_mark_as_done]):
            following_bytecode_idx = next_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            context = (
                "value" if following_bytecode["instruction"] in ["LOAD", "LOADF"]
                else "address"
            )
            symbol = get_certificate_symbol(f"VAR_{context.upper()}")
            var_prime = self.__get_variable_prime(bytecode)

            exponent = (
                f"({symbol})"
                + f"^({var_prime})"
                + "^(2)"
                + "^(1)"
            )

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

        certificate = f"{self.current_positional_prime}^({exponent})"

        for idx in range(bytecode_idx, bytecode_idx + instructions_to_mark_as_done):
            bytecode_id = self.bytecode_list[idx]["instruction_id"]
            self.instruction_status[bytecode_id] = True

        # Advance the positional prime
        self.current_positional_prime = next_prime(self.current_positional_prime)

        return certificate
    
    def __get_variable_prime(self, bytecode) -> int:
        """
        Get the prime number that uniquely represents a variable.

        This number is obtained from the certificator environment. This
        environment maps the variable's base address to its unique prime nubmer.

        This method is intended to be used exclusively with `CONSTANT` bytecode.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The `CONSTANT` bytecode. This bytecode contains the base address
            of the variable of interest.

        Returns
        -------
        : int
            The variable prime.
        """

        # The `CONSTANT` bytecode has the variable address as its value.
        var_address = bytecode["metadata"]["value"]

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

        return var_prime
    
    def __speculate_data_structure(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int,
    ) -> tuple[Union[str, None], Union[int, None]]:
        """
        Speculate if this variable is a data structure (array/struct).

        This is an _speculation_ because we can't tell if a variable is actually
        an array or struct beforehand. To do so, we must check if a specific
        sequence of bytecodes is observed near it.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The initial bytecode that implements this variable usage.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        exponent : str or None
            The exponent (that will compose the certificate) of this data
            structure. Returns `None` if this is not a data structure.
        instructions_to_mark_as_done : int or None
            The number of bytecodes, including `bytecode`, that will be marked
            as done in `self.instruction_status`. Returns `None` if this is not
            a data structure.
        """

        following_bytecode_idx = bytecode_idx + 1
        following_bytecode = self.bytecode_list[following_bytecode_idx]

        # The pattern for access to array or struct elements will always begin
        # with `CONSTANT` (`bytecode`, that we already know that it is) + `ADD`
        # (following_bytecode) to get the address of the indexing variable or
        # the index of the element being accessed.
        following_bytecode_is_add = following_bytecode["instruction"] == "ADD"

        # Early return
        if not following_bytecode_is_add:
            return (None, None)
        
        var_prime = self.__get_variable_prime(bytecode)

        # Check if it is an access to a struct attribute or to an array element
        # using a constant for index.
        is_static_array_or_struct = True

        # Prevent the speculation of going out of bounds or accessing an
        # unexisting attribute
        try:
            speculated_base_address_register = bytecode["metadata"]["register"]
            speculated_var_address_register = following_bytecode["metadata"]["register"]

            # Pattern:
            # 1. Following bytecode: `CONSTANT` (it has the offset size)
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            speculated_index_register = following_bytecode["metadata"]["register"]
            speculated_index = following_bytecode["metadata"]["value"]

            is_static_array_or_struct = (
                is_static_array_or_struct
                and following_bytecode["instruction"] == "CONSTANT"
            )
            
            # 2. Following bytecode: `CONSTANT` (it has the type size)
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            speculated_type_size_register = following_bytecode["metadata"]["register"]

            is_static_array_or_struct = (
                is_static_array_or_struct
                and following_bytecode["instruction"] == "CONSTANT"
            )

            # 2. Following bytecode: `MULT` (to compute the memory offset)
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            speculated_offset_register = following_bytecode["metadata"]["register"]

            is_static_array_or_struct = (
                is_static_array_or_struct
                and following_bytecode["instruction"] == "MULT"
                and following_bytecode["metadata"]["lhs_register"] == speculated_index_register
                and following_bytecode["metadata"]["rhs_register"] == speculated_type_size_register
            )

            # 3. Following bytecode: `ADD` (to add the base address from
            # `bytecode` to the `offset`)
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            is_static_array_or_struct = (
                is_static_array_or_struct
                and following_bytecode["instruction"] == "ADD"
                and following_bytecode["metadata"]["lhs_register"] == speculated_var_address_register
                and following_bytecode["metadata"]["rhs_register"] == speculated_offset_register
            )

            # If all the conditions held, return the adequate exponent and
            # number of bytecodes already accounted for
            if is_static_array_or_struct:
                following_bytecode_idx = following_bytecode_idx + 1
                following_bytecode = self.bytecode_list[following_bytecode_idx]

                context = (
                    "value" if following_bytecode["instruction"] in ["LOAD", "LOADF"]
                    else "address"
                )
                symbol = get_certificate_symbol(f"VAR_{context.upper()}")

                exponent = (
                    f"({symbol})"
                    + f"^({var_prime})"
                    + f"^(2)^({speculated_index + 1})"
                )

                # Account for:
                #  - 2 instructions to obtain the variable base address
                #  - 1 instruction to obtain the index
                #  - 1 instruction to obtain the type size
                #  - 2 instructions to compute the element address (`ADD` and `MULT`)
                instructions_to_mark_as_done = 6

                # Account for the `LOAD`, if this is a var. value case.
                if context == "value":
                    instructions_to_mark_as_done += 1

                return (exponent, instructions_to_mark_as_done)

        except (IndexError, KeyError):
            pass

        # Check if it is an access an array element using another variable for
        # index.
        is_dinamically_accessed_array = True

        try:
            # Pattern:
            # 1. First bytecode: `CONSTANT`, with the base address of the array
            following_bytecode_idx = bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            speculated_base_address_register = bytecode["metadata"]["register"]

            # 2. Following bytecode: `ADD`, with `lhs=speculated_base_address_register`
            # and `rhs=zero`
            speculated_var_address_register = following_bytecode["metadata"]["register"]

            is_dinamically_accessed_array = (
                is_dinamically_accessed_array
                and following_bytecode["instruction"] == "ADD"
                and following_bytecode["metadata"]["lhs_register"] == speculated_base_address_register
                and following_bytecode["metadata"]["rhs_register"] == "zero"
            )

            # 3. Following bytecode: `CONSTANT`, with the base address of the
            # indexing variable.
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            # This is the base address
            speculated_index_var_base_address_register = following_bytecode["metadata"]["register"]
            speculated_index_var_prime = self.__get_variable_prime(following_bytecode)

            is_dinamically_accessed_array = (
                is_dinamically_accessed_array
                and following_bytecode["instruction"] == "CONSTANT"
            )

            # 4. Following bytecode: `ADD`, with `lhs=speculated_index_var_base_address_register`
            # and `rhs=zero`
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            # This is the actual address
            speculated_index_var_address_register = following_bytecode["metadata"]["register"]

            is_dinamically_accessed_array = (
                is_dinamically_accessed_array
                and following_bytecode["instruction"] == "ADD"
                and following_bytecode["metadata"]["lhs_register"] == speculated_index_var_base_address_register
                and following_bytecode["metadata"]["rhs_register"] == "zero"
            )

            # 5. Following bytecode: `LOAD`, fetching data from
            # `speculated_index_address_register`
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]
            
            speculated_index_var_value_register = following_bytecode["metadata"]["register"]

            is_dinamically_accessed_array = (
                is_dinamically_accessed_array
                and following_bytecode["instruction"] == "LOAD"
                and following_bytecode["metadata"]["value"] == speculated_index_var_address_register
            )

            # 6. Following bytecode: `CONSTANT` (it has the type size)
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            speculated_type_size_register = following_bytecode["metadata"]["register"]

            is_dinamically_accessed_array = (
                is_dinamically_accessed_array
                and following_bytecode["instruction"] == "CONSTANT"
            )

            # 7. Following bytecode: `MULT` (to compute the memory offset)
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            speculated_offset_register = following_bytecode["metadata"]["register"]

            is_dinamically_accessed_array = (
                is_dinamically_accessed_array
                and following_bytecode["instruction"] == "MULT"
                and following_bytecode["metadata"]["lhs_register"] == speculated_index_var_value_register
                and following_bytecode["metadata"]["rhs_register"] == speculated_type_size_register
            )

            # 8. Following bytecode: `ADD` (to add the base address from
            # `bytecode` to the `offset`)
            following_bytecode_idx = following_bytecode_idx + 1
            following_bytecode = self.bytecode_list[following_bytecode_idx]

            is_dinamically_accessed_array = (
                is_dinamically_accessed_array
                and following_bytecode["instruction"] == "ADD"
                and following_bytecode["metadata"]["lhs_register"] == speculated_var_address_register
                and following_bytecode["metadata"]["rhs_register"] == speculated_offset_register
            )

            # If all the conditions held, return the adequate exponent and
            # number of bytecodes already accounted for
            if is_dinamically_accessed_array:
                following_bytecode_idx = following_bytecode_idx + 1
                following_bytecode = self.bytecode_list[following_bytecode_idx]

                context = (
                    "value" if following_bytecode["instruction"] in ["LOAD", "LOADF"]
                    else "address"
                )
                symbol = get_certificate_symbol(f"VAR_{context.upper()}")
                
                exponent = (
                    f"({symbol})"
                    # + f"^({var_prime})"
                    + f"^(VAR PRIME)"
                    # + f"^(3)^({speculated_index_var_prime})"
                    + f"^(3)^(INDEX VAR PRIME)"
                )

                # Account for:
                #  - 2 instructions to obtain the variable base address
                #  - 3 instructions to load the value from the index variable
                #  - 1 instruction to obtain the type size
                #  - 2 instructions to compute the element address (`ADD` and `MULT`)
                instructions_to_mark_as_done = 8

                # Account for the `LOAD`, if this is a var. value case.
                if context == "value":
                    instructions_to_mark_as_done += 1

                return (exponent, instructions_to_mark_as_done)

        except (IndexError, KeyError):
            return (None, None)

        return (None, None)
   
    def _handle_mov(
        self,
        bytecode: dict[str, dict],
        bytecode_idx: int
    ) -> str:
        """
        Handle a `MOV` bytecode.

        This method will identify what operation it implements and return the
        adequate certificate.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The `MOV` bytecode.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        certificate : str
            The adequate certificate.

        TODO: support arg/func call
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
        Handle a simple bytecode.

        A bytecode is _simple_ if it does not require pattern matching in order
        to identify what operation it implements.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The simple bytecode to certificate.
        bytecode_idx : int
            The index of this `bytecode` in `self.bytecode_list`.

        Returns
        -------
        certificate : str
            The instruction certificate.
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
