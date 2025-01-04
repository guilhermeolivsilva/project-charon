"""Certificator for the frontend representation of Tiny C programs."""

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
        self.bytecode_list = [*self.program["global_vars"], *self.program["code"]]

        # Track the certificates and metadata associated with each register
        self.register_tracker: dict[int, dict] = {}

        self.variable_prime_tracker: dict[int, int] = {}

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
            bytecode["instruction_id"]: False for bytecode in self.bytecode_list
        }

        # Corner case instructions – i.e., instructions that have a particular
        # design and need to be treated individually.
        self.special_instructions_handlers: dict[str, dict] = {
            "ALLOC": self._handle_alloc_instruction,
            "STORE": self._handle_store_instruction,
            "MOV": self._handle_mov_instruction,
            "JZ": self._handle_jump,
            "JAL": self._handle_function_call,
            "HALT": self._handle_halt,
        }

        self.grouped_instructions_handlers: dict[str, dict] = {
            # Variables
            **{
                _instruction: self._handle_variables
                for _instruction in INSTRUCTIONS_CATEGORIES["variables"]
            },
            # Constants
            **{
                _instruction: self._handle_constants
                for _instruction in INSTRUCTIONS_CATEGORIES["constants"]
            },
            # Unary operations
            **{
                _instruction: self._handle_operations
                for _instruction in INSTRUCTIONS_CATEGORIES["unops"]
            },
            # Binary operations
            **{
                _instruction: self._handle_operations
                for _instruction in INSTRUCTIONS_CATEGORIES["binops"]
            },
        }

        self.type_cast_handlers = {
            _instruction: self._handle_type_casts
            for _instruction in INSTRUCTIONS_CATEGORIES["type_casts"]
        }

    @override
    def certificate(self, **kwargs) -> list[str]:
        """
        Certificate the backend code.

        This method iterates over the machine code and annotate each instruction
        with its relative position and contents.

        Returns
        -------
        computed_certificate : list[str]
            The list of labels that compose the computed certificate.
        """

        for bytecode in self.bytecode_list:
            bytecode_id = bytecode["instruction_id"]

            # print("current id:", bytecode_id)

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
            if instruction in self.special_instructions_handlers:
                handler = self.special_instructions_handlers[instruction]

            elif instruction in self.type_cast_handlers:
                handler = self._handle_type_casts

                # Offset the `current_position_prime` increment made by the type
                # casts handler
                self.current_positional_prime = previous_prime(
                    self.current_positional_prime
                )

            else:
                handler = self.grouped_instructions_handlers[instruction]

            # print(f"certificating {instruction} (id: {bytecode['instruction_id']}) with {handler}")
            # print(f"current prime: {self.current_positional_prime}")
            # print("")

            certificate = handler(bytecode)

        except KeyError as e:
            print(f"Handler for {instruction} has not been implemented yet")
            print(bytecode)
            print(e)
            raise e

        return certificate

    def _handle_alloc_instruction(self, bytecode: dict[str, dict]) -> str:
        """
        Handle a `ALLOC` instruction.

        This instruction has two uses cases: defining "regular" variables, or
        being used together with `STORE` in order to handle paremeters inside
        a function. As each case use a different certificate, we handle them
        separetely.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.

        Returns
        -------
        certificate : str
            The `ALLOC` instruction certificate.
        """

        metadata = bytecode["metadata"]
        register = metadata["register"]
        allocated_size = metadata["size"]

        is_param, next_bytecode = self.__is_param(bytecode)

        if is_param:
            # If handling a parameter, the next instruction (a `STORE`) must
            # also be tagged as "certificated"
            store_id = next_bytecode["instruction_id"]
            self.instruction_status[store_id] = True
            source = "PARAM"
            symbol = get_certificate_symbol("PARAM")
        else:
            symbol = get_certificate_symbol("VAR_DEF")
            source = "ALLOC"

        certificate = (
            f"{self.current_positional_prime}"
            + f"^(({symbol})"
            + f"^({self.current_variable_prime})"
            + f"^({allocated_size}))"
        )

        register_metadata = {
            "source": source,
            "metadata": {
                "certificate": certificate,
                "prime": self.current_variable_prime,
                "positional_prime": self.current_positional_prime,
            },
        }

        self.register_tracker[register] = register_metadata
        self.variable_prime_tracker[metadata["id"]] = self.current_variable_prime
        self.instruction_status[bytecode["instruction_id"]] = True

        self.current_variable_prime = next_prime(self.current_variable_prime)

        return certificate

    def _handle_store_instruction(self, bytecode: dict[str, dict]) -> str:
        """
        Handle a `STORE` instruction.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.

        Returns
        -------
        certificate : str
            The `STORE` instruction certificate.
        """

        metadata = bytecode["metadata"]

        lhs_metadata = self.register_tracker[metadata["register"]]
        lhs_certificate = lhs_metadata["metadata"]["certificate"]

        rhs_metadata = self.register_tracker[metadata["value"]]
        rhs_certificate = rhs_metadata["metadata"]["certificate"]

        # Remove `rhs_certificate` from `computed_certificate` to avoid
        # adding it twice, if applicable
        self.__remove_duplicate(certificate=rhs_certificate)

        symbol = get_certificate_symbol("ASSIGN")
        certificate = (
            f"{self.current_positional_prime}"
            + f"^({symbol})"
            + f"*{lhs_certificate}"
            + f"*{rhs_certificate}"
        )

        source_metadata = {
            "source": "STORE",
            "metadata": {
                "certificate": certificate,
                "lhs_operand": lhs_metadata,
                "rhs_operand": rhs_metadata,
                "positional_prime": self.current_positional_prime,
            },
        }

        self.register_tracker[metadata["register"]] = source_metadata
        self.instruction_status[bytecode["instruction_id"]] = True

        return certificate

    def _handle_mov_instruction(self, bytecode: dict[str, dict]) -> str:
        """
        Handle a `MOV` instruction.

        `MOV` instructions have two use cases:

        1. Function call: there are `MOV` instructions for both moving the
        arguments values to the `arg` register (i.e., to move data from a
        general use register to the `arg` register), and to retrieve the value
        the call returned (i.e., to move data from the `ret_value` register to a
        general use register).
        2. Function return: the `MOV` instruction moves the value to return from
        a function, stored in a general use register, to the `ret_value`
        register.

        This method dispatches the correct handler for each case.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.

        Returns
        -------
        certificate : str
            The `MOV` instruction certificate.
        """

        if self.__is_function_return(bytecode):
            return self._handle_return(bytecode)
        else:
            return self._handle_function_call(bytecode)

    def _handle_function_call(self, bytecode: dict[str, dict]) -> str:
        """
        Handle a function call.

        Function calls are composed by a sequence of zero or more `MOV`
        instructions that moves data from general use registers to `arg`, and a
        pair `JAL` + `MOV` that moves data from `ret_value` to a general use
        register.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.

        Returns
        -------
        certificate : str
            The function call certificate.
        """

        current_bytecode = bytecode
        current_bytecode_idx = bytecode["instruction_id"] - 1

        next_bytecode = self.bytecode_list[current_bytecode_idx + 1]

        # Iterate over the instructions until we find the `JAL` + `MOV` pair,
        # certificating the bytecodes we find along the way
        args_certificates = []

        while not self.__is_function_call(
            bytecode_pair=(current_bytecode, next_bytecode)
        ):
            # Get the "final" certificate of the argument, as it has already
            # been computed
            if current_bytecode["instruction"] == "MOV":
                source_register = current_bytecode["metadata"]["value"]
                _arg_base_certificate = self.register_tracker[source_register][
                    "metadata"
                ]["certificate"]

                _arg_certificate_symbol = get_certificate_symbol("ARG")
                _arg_certificate = (
                    f"{self.current_positional_prime}"
                    + f"^({_arg_certificate_symbol})"
                    + f"*{_arg_base_certificate}"
                )

                args_certificates.append(_arg_certificate)
                self.current_positional_prime = next_prime(
                    self.current_positional_prime
                )

            # Compute the argument certificate. We don't really care about this
            # value right now, so we ignore it. We only need to add it to
            # `self.register_tracker` – so it can be retrieved by the code block
            # above
            else:
                # This `_handlers` is just to pool together `type_cast_handlers`
                # and `grouped_instructions_handlers`.
                _handlers = {
                    **self.type_cast_handlers,
                    **self.grouped_instructions_handlers,
                }

                current_instruction = current_bytecode["instruction"]
                handler = _handlers[current_instruction]
                _ = handler(current_bytecode)

                self.current_positional_prime = next_prime(
                    self.current_positional_prime
                )

            self.instruction_status[current_bytecode["instruction_id"]] = True

            # ...and move the sliding window to the next pair
            current_bytecode = next_bytecode
            current_bytecode_idx += 1
            next_bytecode = self.bytecode_list[current_bytecode_idx + 1]

        # Once we find the function call pair, produce the final certificate
        # `current_bytecode` -> JAL
        # `next_bytecode` -> MOV
        function_id = current_bytecode["metadata"]["value"]
        function_prime = self.functions_primes[function_id]
        function_register = next_bytecode["metadata"]["register"]

        symbol = get_certificate_symbol("FUNC_CALL")

        certificate = (
            f"{self.current_positional_prime}^" + f"(({symbol})^({function_prime}))"
        )

        if args_certificates:
            certificate += f"*{'*'.join(args_certificates)}"

        register_metadata = {
            "source": "FUNC_CALL",
            "metadata": {
                "certificate": certificate,
                "prime": function_prime,
                "positional_prime": self.current_positional_prime,
            },
        }

        self.register_tracker[function_register] = register_metadata

        # Tag both of the instructions associated with the function call as
        # certificated
        self.instruction_status[current_bytecode["instruction_id"]] = True
        self.instruction_status[next_bytecode["instruction_id"]] = True

        return certificate

    def _handle_return(self, bytecode: dict[str, dict]) -> str:
        """
        Handle a function return.

        Function returns are composed by a pair of `MOV` that moves data from
        general use registers to `ret_value`, and a `JR` that jumps to an
        instruction whose index is stored in some general use register.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.

        Returns
        -------
        certificate : str
            The function return certificate.
        """

        current_bytecode = bytecode
        current_bytecode_idx = bytecode["instruction_id"] - 1
        next_bytecode_idx = current_bytecode_idx + 1

        next_bytecode = self.bytecode_list[next_bytecode_idx]

        # Just to be sure it is a `MOV` + `JR` pair.
        self.__assert_is_return(bytecode_pair=(current_bytecode, next_bytecode))

        # Build the certificate
        symbol = get_certificate_symbol("RET_SYM")

        # Get the returned value certificate
        returned_value_data = self.register_tracker[
            current_bytecode["metadata"]["value"]
        ]
        returned_value_certificate = returned_value_data["metadata"]["certificate"]

        self.__remove_duplicate(certificate=returned_value_certificate)

        certificate = (
            f"{self.current_positional_prime}"
            + f"^({symbol})"
            + f"*{returned_value_certificate}"
        )

        self.instruction_status[current_bytecode["instruction_id"]] = True
        self.instruction_status[next_bytecode["instruction_id"]] = True

        return certificate

    def _handle_jump(self, bytecode: dict[str, dict]) -> str:
        """
        Handle a jump.

        This method only handles `JZ` jumps. For `JR`, see `self._handle_return`.
        For `JAL`, see `self._handle_function_call`.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.

        Returns
        -------
        certificate : str
            The jump certificate.
        """

        # Identify the jump: `IF`, `IFELSE`, `WHILE`, `DO`
        jump_kind = self.__identify_jz(bytecode)

        # Build the certificate
        symbol = get_certificate_symbol(jump_kind)
        certificate = f"{self.current_positional_prime}" + f"^({symbol})"

        self.instruction_status[bytecode["instruction_id"]] = True

        return certificate

    def _handle_variables(self, bytecode: dict[str, dict]) -> None:
        """
        Handle variable use cases.

        `ADDRESS` and `LOAD` instructions define such cases.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.
        """

        instruction = bytecode["instruction"]
        metadata = bytecode["metadata"]
        register = metadata["register"]

        if instruction == "ADDRESS":
            symbol = get_certificate_symbol("VAR_ADDRESS")
        else:
            symbol = get_certificate_symbol("VAR_VALUE")

        variable_prime = self.variable_prime_tracker[metadata["id"]]

        # If there's `offset_register` in the metadata, then its accessing an
        # array using a variable for index.
        if metadata.get("offset_register"):
            _indexing_variable = self.register_tracker[metadata["offset_register"]]
            _indexing_variable_prime = _indexing_variable["metadata"]["prime"]
            indexing = f"^(3)^({_indexing_variable_prime}))"

            # Use the previous prime because the `LOAD` instruction regarding
            # the index prime is already being accounted for by this certificate
            self.current_positional_prime = previous_prime(
                self.current_positional_prime
            )

        # If not, then it might be an array accessed with a constant for index,
        # a struct attribute, or a "simple" variable. For either case, we'll
        # use `offset + 1` (`offset` = 0 for "simple" variables).
        else:
            offset_size = metadata.get("offset_size", 0)
            indexing = f"^(2)^({offset_size + 1}))"

        certificate = (
            f"{self.current_positional_prime}"
            + f"^(({symbol})"
            + f"^({variable_prime})"
            + indexing
        )

        register_metadata = {
            "source": instruction,
            "metadata": {
                "certificate": certificate,
                "prime": variable_prime,
                "positional_prime": self.current_positional_prime,
            },
        }

        self.register_tracker[register] = register_metadata
        self.instruction_status[bytecode["instruction_id"]] = True

    def _handle_halt(self, bytecode: dict[str, dict]) -> str:
        """
        Handle the program ending instruction.

        Programs are ended by `HALT`.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.
        """

        symbol = get_certificate_symbol("PROG")
        certificate = f"{self.current_positional_prime}" + f"^({symbol})"

        self.instruction_status[bytecode["instruction_id"]] = True

        return certificate

    def _handle_constants(self, bytecode: dict[str, dict]) -> None:
        """
        Handle constants.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.
        """

        metadata = bytecode["metadata"]
        register = metadata["register"]

        constant_value = metadata["value"]

        # This will be used as an exponent. So, we avoid 0 with this ternary
        _constant_value_exponent = (
            constant_value + 1 if constant_value >= 0 else constant_value
        )

        symbol = get_certificate_symbol("CST")

        certificate = (
            f"{self.current_positional_prime}"
            + f"^(({symbol})"
            + f"^({_constant_value_exponent}))"
        )

        register_metadata = {
            "source": "CONSTANT",
            "metadata": {
                "certificate": certificate,
                "value": constant_value,
                "positional_prime": self.current_positional_prime,
            },
        }

        self.register_tracker[register] = register_metadata
        self.instruction_status[bytecode["instruction_id"]] = True

    def _handle_type_casts(self, bytecode: dict[str, dict]) -> None:
        """
        Handle type casts.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.
        """

        instruction = bytecode["instruction"]
        metadata = bytecode["metadata"]
        register = metadata["register"]

        original_value_register = metadata["value"]
        original_value_certificate = self.register_tracker[original_value_register][
            "metadata"
        ]["certificate"]

        source_metadata = {
            "source": instruction,
            "metadata": {
                "operand": original_value_register,
                "certificate": original_value_certificate,
                "positional_prime": self.current_positional_prime,
            },
        }

        self.register_tracker[register] = source_metadata
        self.instruction_status[bytecode["instruction_id"]] = True

    def _handle_operations(self, bytecode: dict[str, dict]) -> str:
        """
        Handle unary and binary operations.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.

        Returns
        -------
        certificate : str
            The operation certificate.
        """

        instruction = bytecode["instruction"]
        metadata = bytecode["metadata"]
        register = metadata["register"]

        # Handle a corner case: `NOT` followed by `JZ`, where `JZ` is identified
        # to be a `DO` operation (DO/WHILE operations are built with a `NOT` +
        # `JZ` instructions pair)
        current_instruction_index = bytecode["instruction_id"] - 1
        next_instruction_index = current_instruction_index + 1

        next_bytecode = self.bytecode_list[next_instruction_index]
        next_instruction = next_bytecode["instruction"]

        if instruction == "NOT" and next_instruction == "JZ":
            _jump_kind = self.__identify_jz(next_bytecode)

            if _jump_kind == "DO":
                # If it indeed is a `DO` operation, tag the current bytecode
                # as certificated and handle the following jump
                self.instruction_status[bytecode["instruction_id"]] = True
                return self._handle_jump(next_bytecode)

        if instruction in INSTRUCTIONS_CATEGORIES["unops"]:
            keys = ["operand"]
            metadata_keys = ["value"]

        else:
            keys = ["lhs_operand", "rhs_operand"]
            metadata_keys = ["lhs_register", "rhs_register"]

        # Build the certificate
        symbol = get_certificate_symbol(instruction)
        operands_certificates = []

        for metadata_key in metadata_keys:
            _operand_metadata = self.register_tracker[metadata[metadata_key]]
            _operand_certificate = _operand_metadata["metadata"]["certificate"]
            operands_certificates.append(_operand_certificate)

            # Pop `_operand_certificate` from `computed_certificate` to avoid
            # adding it twice, if applicable
            self.__remove_duplicate(certificate=_operand_certificate)

        certificate = (
            f"{self.current_positional_prime}"
            + f"^({symbol})"
            + f"*{'*'.join(operands_certificates)}"
        )

        source_metadata = {
            "source": instruction,
            "metadata": {
                "certificate": certificate,
                "positional_prime": self.current_positional_prime,
            },
        }
        source_metadata["metadata"].update(
            {
                key: self.register_tracker[metadata[metadata_key]]
                for key, metadata_key in zip(keys, metadata_keys)
            }
        )

        self.register_tracker[register] = source_metadata
        self.instruction_status[bytecode["instruction_id"]] = True

        return certificate

    def __is_param(self, bytecode: dict[str, dict]) -> tuple[bool, dict[str, dict]]:
        """
        Tell whether a `ALLOC` instruction is a parameter handler.

        For it to be a parameter handler, the next instruction must be `STORE`
        where the right-hand side register is `arg`.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.

        Returns
        -------
        verdict : bool
            `True` if it is a parameter handler, `False` otherwise.
        next_bytecode : dict[str, dict]
            The next instruction and its bytecode metadata.
        """

        current_instruction_index = bytecode["instruction_id"] - 1
        next_instruction_index = current_instruction_index + 1

        next_bytecode = self.bytecode_list[next_instruction_index]
        next_instruction = next_bytecode["instruction"]

        if next_instruction != "STORE":
            return (False, next_bytecode)

        rhs_register = next_bytecode["metadata"]["value"]
        return (rhs_register == "arg", next_bytecode)

    def __is_function_return(self, bytecode: dict[str, dict]) -> bool:
        """
        Tell whether a `MOV` instruction is handling a function return.

        For it to handle a function return, it must move data from a general use
        register to the `ret_value` register. Also, the following instruction
        must be `JR`.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.

        Returns
        -------
        : bool
            `True` if it is a function return, `False` otherwise.
        """

        current_bytecode_idx = bytecode["instruction_id"] - 1
        next_bytecode = self.bytecode_list[current_bytecode_idx + 1]

        return (
            bytecode["metadata"]["register"] == "ret_value"
            and next_bytecode["instruction"] == "JR"
        )

    def __is_function_call(self, bytecode_pair: tuple[dict, dict]) -> bool:
        """
        Tell whether a pair of bytecodes handle a function call.

        For it to handle a function call, the first bytecode must contain a
        `JAL` instruction, and the second, a `MOV` instruction that moves data
        from `ret_value` to a general use register.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.

        Returns
        -------
        : bool
            `True` if it is a function call, `False` otherwise.
        """

        first_bytecode, second_bytecode = bytecode_pair

        return (
            first_bytecode["instruction"] == "JAL"
            and second_bytecode["instruction"] == "MOV"
            and second_bytecode["metadata"]["value"] == "ret_value"
        )

    def __assert_is_return(self, bytecode_pair: tuple[dict, dict]) -> None:
        """
        Assert a pair of bytecodes handle a function return.

        For it to handle a function return, the first bytecode must contain a
        `MOV` instruction that moves data from a general use register to
        `ret_value`, and the second, a `JR` instruction.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.

        Raises
        ------
        ValueError
            Raised if the assertion fails.
        """

        first_bytecode, second_bytecode = bytecode_pair

        is_return = (
            first_bytecode["instruction"] == "MOV"
            and first_bytecode["metadata"]["register"] == "ret_value"
            and second_bytecode["instruction"] == "JR"
        )

        if not is_return:
            raise ValueError("Malformed return pair.")

    def __identify_jz(self, bytecode: dict[str, dict]) -> str:
        """
        Tell the semantics of a conditional jump.

        Conditional jumps are used to implement four control flow constructs:
        `if`, `if/else`, `while`, and `do/while`. As the certification considers
        what kind of control flow is being used, this method aims to identify
        the construct based on the pattern of its context.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.

        Returns
        -------
        : str (values="IF", "IFELSE", "WHILE", "DO")
            The semantics of the conditional jump.
        """

        bytecode_idx = bytecode["instruction_id"] - 1
        _jump_size: int = bytecode["metadata"]["jump_size"]

        _instruction_right_before_jump_target_idx = bytecode_idx + _jump_size - 1
        _instruction_right_before_jump_target = self.bytecode_list[
            _instruction_right_before_jump_target_idx
        ]

        _jumps_forward = self.__is_jump_forward(bytecode)
        _lands_on_instruction_preceeded_by_unconditional_jump = (
            self.__is_unconditional_jump(_instruction_right_before_jump_target)
        )

        if _jumps_forward:
            if _lands_on_instruction_preceeded_by_unconditional_jump:
                _preceeding_unconditional_jump_is_forward = self.__is_jump_forward(
                    _instruction_right_before_jump_target
                )

                # Tag the unconditional jump as certificated
                _instruction_right_before_jump_target_id = (
                    _instruction_right_before_jump_target["instruction_id"]
                )
                self.instruction_status[_instruction_right_before_jump_target_id] = True

                if _preceeding_unconditional_jump_is_forward:
                    return "IFELSE"
                else:
                    return "WHILE"
            else:
                return "IF"
        else:
            return "DO"

    def __is_jump_forward(self, bytecode: dict[str, dict]) -> bool:
        """
        Tell whether a jump instruction goes forward or backwards.

        Parameters
        ----------
        bytecode_idx : int
            The jump bytecode.

        Returns
        -------
        : bool
            True if the jump is forward (`jump_size` > 0), False otherwise.
        """

        return (
            "jump_size" in bytecode["metadata"]
            and bytecode["metadata"]["jump_size"] > 0
        )

    def __is_unconditional_jump(self, bytecode: dict[str, dict]) -> bool:
        """
        Tell whether a conditional jump actually implements an unconditional one.

        Such jumps are `JZ` instructions that use the `zero` register as the
        condition. This register will always contain `0`, and thus the jump
        always occur.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The jump bytecode.

        Returns
        -------
        : bool
            True if the jump is unconditional, False otherwise.
        """

        return (
            "conditional_register" in bytecode["metadata"]
            and bytecode["metadata"]["conditional_register"] == "zero"
        )

    def __remove_duplicate(self, certificate: str) -> None:
        """
        Remove an entry from `self.computed_certificate` to avoid duplicates.

        Parameters
        ----------
        certificate : str
            The certificate to remove from `self.computed_certificate`.
        """

        try:
            certificate_idx = self.computed_certificate.index(certificate)
            self.computed_certificate.pop(certificate_idx)
        except ValueError:
            pass
