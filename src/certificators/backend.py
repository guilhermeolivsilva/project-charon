"""Certificator for the frontend representation of Tiny C programs."""

from typing_extensions import override

from src.certificators.abstract_certificator import AbstractCertificator
from src.utils import get_certificate_symbol, next_prime, INSTRUCTIONS_CATEGORIES


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
        self.bytecode_list = [
            *self.program["global_vars"],
            *self.program["code"]
        ]

        # Track the certificates and metadata associated with each register
        self.register_tracker: dict[int, dict] = {}

        self.variable_prime_tracker: dict[int, int] = {}

        self.current_positional_prime = self.initial_prime
        self.current_variable_prime = self.initial_prime
        self.current_function_prime = self.initial_prime

        # Tell whether an instruction has been accounted for in the
        # certification process or not. Maps the ID of `instruction_list` to
        # `True` if already certificated, or `False` otherwise.
        self.instruction_status: dict[int, bool] = {
            bytecode["instruction_id"]: False
            for bytecode in self.bytecode_list
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

            # Skip instructions that have already been certificated.
            if self.instruction_status[bytecode_id]:
                continue

            instruction = bytecode["instruction"]

            if instruction == "HALT":
                break

            certificate = self._certificate_instruction(bytecode=bytecode)

            if certificate:
                self.computed_certificate.append(certificate)

            self.current_positional_prime = next_prime(
                self.current_positional_prime
            )
            self.instruction_status[bytecode_id] = True

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

        # Corner case instructions – i.e., instructions that have a particular
        # design and need to be treated individually.
        special_instructions_handlers: dict[str, dict] = {
            "ALLOC": self._handle_alloc_instruction,
            "STORE": self._handle_store_instruction,
            "MOV": self._handle_mov_instruction
        }

        grouped_instructions_handlers: dict[str, dict] = {
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

            # Type casts
            **{
                _instruction: self._handle_type_casts
                for _instruction in INSTRUCTIONS_CATEGORIES["type_casts"]
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

        try:
            if instruction in special_instructions_handlers:
                handler = special_instructions_handlers[instruction]

            else:
                handler = grouped_instructions_handlers[instruction]
                
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
            + f"^({symbol})"
            + f"^({self.current_variable_prime})"
            + f"^({allocated_size})"
        )

        register_metadata = {
            "source": source,
            "metadata": {
                "certificate": certificate,
                "prime": self.current_variable_prime
            }
        }

        self.register_tracker[register] = register_metadata
        self.variable_prime_tracker[metadata["id"]] = self.current_variable_prime

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

        
        instruction = bytecode["instruction"]
        metadata = bytecode["metadata"]

        register = metadata["register"]

        source_metadata = {
            "source": instruction,
            "metadata": {
                "lhs_operand": self.register_tracker[register],
                "rhs_operand": self.register_tracker[metadata["value"]]
            }
        }

        self.register_tracker[register] = source_metadata

        ...

    def _handle_mov_instruction(self, bytecode: dict[str, dict]) -> str:
        """
        Handle a `MOV` instruction.

        `MOV` instructions have three use cases:

        1. Moving values from a general use register to the `arg` register, when
        setting up a function call;
        2. Moving the value from a general use register to the `ret_value`
        register, when returning from a function.
        3. Moving the returned value stored in the `ret_value` register to a
        general use register, right after the `JAL` instruction.

        Parameters
        ----------
        bytecode : dict[str, dict]
            The instruction and its bytecode metadata.

        Returns
        -------
        certificate : str
            The `MOV` instruction certificate.
        """

        ...
    
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
            # TODO
            indexing = f"^(3^{...})"

        # If not, then it might be an array accessed with a constant for index,
        # a struct attribute, or a "simple" variable. For either case, we'll
        # use `offset + 1` (`offset` = 0 for "simple" variables).
        else:
            offset_size = metadata.get("offset_size", 0)
            indexing = f"^(2^{offset_size + 1})"

        certificate = (
            f"{self.current_positional_prime}"
            + f"^({symbol})"
            + f"^({variable_prime})"
            + indexing
        )

        register_metadata = {
            "source": instruction,
            "metadata": {
                "certificate": certificate,
                "prime": variable_prime
            }
        }

        self.register_tracker[register] = register_metadata
    
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
            f"({symbol})"
            + f"^({_constant_value_exponent})"
        )

        register_metadata = {
            "source": "CONSTANT",
            "metadata": {
                "value": constant_value,
                "certificate": certificate
            }
        }

        self.register_tracker[register] = register_metadata

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
        original_value_certificate = self.register_tracker[original_value_register]

        source_metadata = {
            "source": instruction,
            "metadata": {
                "operand": original_value_register,
                "certificate": original_value_certificate
            }
        }

        self.register_tracker[register] = source_metadata
    
    def _handle_operations(self, bytecode: dict[str, dict]) -> str:
        """
        ...
        """

        instruction = bytecode["instruction"]
        metadata = bytecode["metadata"]
        register = metadata["register"]

        if instruction in INSTRUCTIONS_CATEGORIES["unops"]:
                keys = ["operand"]
                metadata_keys = ["value"]

        else:
                keys = ["lhs_operand", "rhs_operand"]
                metadata_keys = ["lhs_register", "rhs_register"]

        source_metadata = {
            "source": instruction,
            "metadata": {
                key: self.register_tracker[metadata[metadata_key]]
                for key, metadata_key in zip(keys, metadata_keys)
            }
        }

        self.register_tracker[register] = source_metadata

        ...


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

    
    def __identify_jz(self, bytecode: dict[str, dict], index: int) -> str:
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
        index : int
            The index of `instruction` in `self.bytecode_list`.

        Returns
        -------
        : str (values="IF", "IFELSE", "WHILE", "DO")
            The semantics of the conditional jump.
        """

        _jump_size: int = bytecode["metadata"]["jump_size"]
        
        _instruction_right_before_jump_target_idx = index + _jump_size - 1

        _jumps_forward = self.__is_jump_forward(index)
        _lands_on_instruction_preceeded_by_unconditional_jump = self.__is_unconditional_jump(
            _instruction_right_before_jump_target_idx
        )

        if _jumps_forward:
            if _lands_on_instruction_preceeded_by_unconditional_jump:
                _preceeding_unconditional_jump_is_forward = self.__is_jump_forward(
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

    def __is_jump_forward(self, bytecode_idx: int) -> bool:
        """
        Tell whether a jump instruction goes forward or backwards.

        Parameters
        ----------
        bytecode_idx : int
            The index of the jump instruction in `self.bytecode_list`.

        Returns
        -------
        : bool
            True if the jump is forward (`jump_size` > 0), False otherwise.
        """

        instruction = self.bytecode_list[bytecode_idx]

        return (
            "jump_size" in instruction["metadata"]
            and instruction["metadata"]["jump_size"] > 0
        )

    def __is_unconditional_jump(self, bytecode_idx: int) -> bool:
        """
        Tell whether a conditional jump actually implements an unconditional one.
        
        Such jumps are `JZ` instructions that use the `zero` register as the
        condition. This register will always contain `0`, and thus the jump
        always occur.

        Parameters
        ----------
        bytecode_idx : int
            The index of the jump bytecode in `self.bytecode_list`.

        Returns
        -------
        : bool
            True if the jump is unconditional, False otherwise.
        """

        bytecode = self.bytecode_list[bytecode_idx]

        return (
            "conditional_register" in bytecode["metadata"]
            and bytecode["metadata"]["conditional_register"] == "zero"
        )
