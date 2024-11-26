"""Implement a virtual machine that computes generated code."""

from typing import Union


class VirtualMachine:
    """
    Virtual Machine that computes instructions from the `CodeGenerator`.

    Parameters
    ----------
    program : dict[str, Union[list, dict]]
        The program generated by the `CodeGenerator.generate_code` method.
    memory_size : int, optional (default = 1024)
        The memory size, in bytes, to use.
    """

    variables_instructions: list[str] = [
        "ADDRESS",
        "LOAD"
    ]

    constants_instructions: list[str] = ["CONSTANT"]

    type_cast_instructions: list[str] = [
        "FPTOSI",
        "SIGNEXT",
        "SITOFP",
        "TRUNC"
    ]

    unops_instructions: list[str] = [
        "NOT",
        "STORE"
    ]

    binops_instructions: list[str] = [
        "ADD",
        "AND",
        "BITAND",
        "BITOR",
        "DIV",
        "EQ",
        "FADD",
        "FAND",
        "FDIV",
        "FEQ",
        "FGT",
        "FLT",
        "FMULT",
        "FNEQ",
        "FOR",
        "FSUB",
        "GT",
        "LSHIFT",
        "MOD",
        "MULT",
        "NEQ",
        "OR",
        "RSHIFT",
        "SUB"
    ]

    def __init__(
        self,
        program: dict[str, Union[list, dict]],
        memory_size: int = 1024
    ) -> None:
        self.program: dict[str, Union[list, dict]] = program

        # Memory (i.e., storage for variables)
        self.memory: dict[str, Union[int, float, str, None]] = {
            hex(_byte): None
            for _byte in range(memory_size)
        }
        self.memory_size: int = memory_size
        self.memory_pointer: int = 0x0

        # Program execution variables
        self.program_counter: int = 0
        self.registers: dict[Union[int, str], Union[int, float]] = {
            "arg": [],
            "ret_address": [],
            "ret_value": [],
            "zero": 0
        }
        self.variables: dict[int, str] = {}

    def __eq__(self, other: "VirtualMachine") -> bool:
        """
        Implement the equality comparison between VirtualMachine instances.

        Parameters
        ----------
        other : VirtualMachine
            The right hand side VirtualMachine of the comparison.

        Returns
        -------
        is_equal : bool
            `True` if all the attributes are equal, `False` otherwise.
        """

        is_equal: bool = (
            self.program == other.program
            and self.memory == other.memory
            and self.memory_pointer == other.memory_pointer
            and self.program_counter == other.program_counter
            and self.registers == other.registers
            and self.variables == other.variables
        )

        return is_equal

    def __str__(self) -> str:
        """
        Generate a string representation of the VirtualMachine object.

        Returns
        -------
        : str
            The string representation.
        """

        _str: str = ""

        # Internal variables
        _str += "Internal Variables:"
        _str += f"\n  Program Counter: {self.program_counter}"
        _str += f"\n  Memory Pointer: {self.memory_pointer}"

        _str += "\n\n"

        # Program variables: values and addresses
        variables_info = {
            variable_id: {
                "address": variable_value
            }

            for variable_id, variable_value
            in self.variables.items()
        }

        for key, value in variables_info.items():
            address = value["address"]
            variables_info[key]["value"] = self.memory[address]

        _str += "Variables:\n  "
        _str += "\n  ".join(
            f"ID: {id}\n  Data: {data}\n"
            for id, data in variables_info.items()
        )

        return _str

    def get_memory(self) -> dict[str, Union[int, float, str]]:
        """
        Get the `self.memory` dictionary.

        This method only returns valid memory addresses: i.e., addresses that
        do not contain `None`.

        Returns
        -------
        memory : dict[str, Union[int, float, str]]
            The memory dictionary, filtered out of `None` elements.
        """

        memory = {
            address: value
            for address, value in self.memory.items()
            if value is not None
        }

        return memory

    def print(self) -> None:
        """Print this VirtualMachine object."""

        print(self)

    def run(self) -> None:
        """Run the program on the virtual machine."""

        # Run the instructions related to global vars (that are stored in a
        # different section of the program text)
        for global_var_instruction in self.program["global_vars"]:
            instruction = global_var_instruction["instruction"]
            instruction_params = global_var_instruction["metadata"]

            instruction_handler = getattr(self, instruction)
            instruction_handler(instruction_params)

        # Set the `program_counter` to the beginning of the `main` function
        try:
            self.program_counter = self.program["functions"]["main"]["start"]
        except KeyError:
            raise SyntaxError("No main function found. Execution aborted.")

        # Run the actual program
        while True:
            code_metadata = self.program["code"][self.program_counter]

            instruction = code_metadata[("instruction")]
            instruction_params = code_metadata[("metadata")]

            if instruction == "HALT":
                break

            self.program_counter += 1

            instruction_handler = getattr(self, instruction)

            try:
                instruction_handler(instruction_params)
            except Exception as e:
                print("Bad instruction:", instruction, instruction_params)
                raise e

    def ADD(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `ADD` bytecode.

        This method handles the addition between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = lhs + rhs

    def ADDRESS(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `ADDRESS` bytecode.

        This method loads the address of a variable into a register.

        If an array or struct, it will load the address of the first element/
        attribute to the register.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        # Value represents the variable to load's ID in the
        # source code.
        variable_to_load: int = instruction_params["value"]
        variable_address: int = int(self.variables[variable_to_load], 16)

        offset_size: int = instruction_params.get("offset_size", 0)
        offset_register: Union[int, None] = instruction_params.get("offset_register")

        offset = offset_size
        if offset_register:
            offset *= self.registers[offset_register]

        variable_address += offset
        destination_register: int = instruction_params["register"]
        self.registers[destination_register] = hex(variable_address)

    def ALLOC(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `ALLOC` bytecode.

        This method allocates memory for a variable.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Raises
        ------
        MemoryError
            Raised if the memory is full when this method is called, or if the
            available memory is not enough for the variable being allocated.
        """

        if self.memory_pointer >= self.memory_size:
            err_msg: str = "Cannot allocate memory: memory is full"
            err_msg += f"\nInstruction: {instruction_params}"
            raise MemoryError(err_msg)
        
        variable_address: str = hex(self.memory_pointer)

        variable_id: int = instruction_params["id"]
        variable_size: int = instruction_params["size"]
        variable_address_register: int = instruction_params["register"]

        updated_memory_pointer: int = self.memory_pointer + variable_size

        if updated_memory_pointer >= self.memory_size:
            err_msg: str = "Not enough memory to allocate a new variable."
            err_msg += f"\nInstruction: {instruction_params}"
            err_msg += f"\nMemory dump:\n{str(self)}"

            raise MemoryError(err_msg)

        self.registers[variable_address_register] = variable_address
        self.variables[variable_id] = variable_address
        self.memory_pointer = updated_memory_pointer

    def AND(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `AND` bytecode.

        This method handles the "logical and" operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if Python's evaluation
        of `lhs and rhs` results in anything different from `0`. This is due to
        the fact that the language does not support boolean literals (`True` and
        `False`).
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = (
            1 if (lhs and rhs) > 0 else 0
        )

    def BITAND(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `BITAND` bytecode.

        This method handles the bit-wise "and" operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = lhs & rhs

    def BITOR(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `BITOR` bytecode.

        This method handles the bit-wise "or" operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = lhs | rhs

    def CONSTANT(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `CONSTANT` bytecode.

        This method saves the constant in some register.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        destination_register: int = instruction_params["register"]
        constant_value: int = instruction_params["value"]

        self.registers[destination_register] = constant_value

    def DIV(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `DIV` bytecode.

        This method handles the division between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = int(lhs / rhs)

    def EQ(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `EQ` bytecode.

        This method handles the "is equal" comparison between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if the expression
        evaluates to `True`, and `0` other wise. This is due to the fact that
        the language does not support boolean literals (`True` and `False`).
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = int(lhs == rhs)

    def FADD(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FADD` bytecode.

        This method handles the addition between two floating point numbers.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = lhs + rhs

    def FAND(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FAND` bytecode.

        This method handles the "logical and" operation between two floating
        point numbers.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if Python's evaluation
        of `lhs and rhs` results in anything different from `0`. This is due to
        the fact that the language does not support boolean literals (`True` and
        `False`).
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = (
            1 if (lhs and rhs) > 0 else 0
        )

    def FDIV(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FDIV` bytecode.

        This method handles the division between two floating point numbers.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = lhs / rhs

    def FEQ(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FEQ` bytecode.

        This method handles the "is equal" comparison between two floating point
        numbers.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if the expression
        evaluates to `True`, and `0` other wise. This is due to the fact that
        the language does not support boolean literals (`True` and `False`).
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = int(lhs == rhs)

    def FGT(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FGT` bytecode.

        This method handles the "greater than" comparison between two floating
        point numbers.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if the expression
        evaluates to `True`, and `0` other wise. This is due to the fact that
        the language does not support boolean literals (`True` and `False`).
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = int(lhs > rhs)

    def FLT(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FLT` bytecode.

        This method handles the "less than" comparison between two floating
        point numbers.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if the expression
        evaluates to `True`, and `0` other wise. This is due to the fact that
        the language does not support boolean literals (`True` and `False`).
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = int(lhs < rhs)

    def FMULT(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FMULT` bytecode.

        This method handles the multiplication between two floating point
        numbers.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = lhs * rhs

    def FNEQ(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FNEQ` bytecode.

        This method handles the "is not equal" comparison between two floating
        point numbers.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if the expression
        evaluates to `True`, and `0` other wise. This is due to the fact that
        the language does not support boolean literals (`True` and `False`).
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = int(lhs != rhs)

    def FOR(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FOR` bytecode.

        This method handles the "logical or" operation between two floating
        point numbers.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if Python's evaluation
        of `lhs or rhs` results in anything different from `0`. This is due to
        the fact that the language does not support boolean literals (`True` and
        `False`).
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = (
            1 if (lhs or rhs) > 0 else 0
        )

    def FPTOSI(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FPTOSI` bytecode.

        This method type casts a floating point to signed integer. For the sake
        of simplicity, we'll use Python's conversion.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        source_register: int = instruction_params["source_register"]
        destination_register: int = instruction_params["destination_register"]

        self.registers[destination_register] = int(self.registers[source_register])

    def FSUB(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FSUB` bytecode.

        This method handles the subtraction between two floating point numbers.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = lhs - rhs

    def GT(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `GT` bytecode.

        This method handles the "greater than" comparison between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if the expression
        evaluates to `True`, and `0` other wise. This is due to the fact that
        the language does not support boolean literals (`True` and `False`).
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = int(lhs > rhs)

    def HALT(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `HALT` bytecode.

        This method handles the end of the execution of a program. For this
        instruction, the `instruction_params` is ignored.
        """

        return

    def JAL(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `JAL` bytecode.

        This method handles jump-and-link instructions.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        # Handle the `program_counter` for it to point to the function code
        called_function_id: int = instruction_params["value"]
        called_function_name: str = (
            list(self.program["functions"].keys())[called_function_id - 1]
        )
        called_function_start: int = (
            self.program["functions"][called_function_name]["start"]
        )

        # Set the return address
        self.registers["ret_address"].append(self.program_counter)
        self.program_counter = called_function_start

    def JR(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `JR` bytecode.

        This method jumps to an address stored in a register.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        register_with_address: Union[int, str] = instruction_params["register"]
        address_to_jump_to: int = self.registers[register_with_address]

        # Handle lists
        if isinstance(address_to_jump_to, list):

            # Handle the `return` statement from the end of the program: when
            # reaching the final `return`, there won't be an address to jump
            # to at `registers["ret_address"]`. Thus, jump to the last
            # instruction.
            if address_to_jump_to:
                address_to_jump_to = address_to_jump_to.pop()
            else:
                address_to_jump_to = len(self.program["code"]) - 1

        self.program_counter = address_to_jump_to

    def JZ(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `JZ` bytecode.

        This method handles conditional jumps: if the evaluated value is zero,
        jump some amount of instructions.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        conditional_register: int = instruction_params["conditional_register"]
        condition: int = self.registers[conditional_register]

        if not condition:
            jump_size: int = instruction_params["jump_size"]
            self.program_counter += jump_size - 1

    def LOAD(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `LOAD` bytecode.

        This method loads the value of a variable into a register.

        If an array or struct, it will load the value of the first element/
        attribute to the register -- which is not a problem at all, as
        `self.ELEMENT_ADDRESS` will handle this later.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        # Value represents the variable to load's ID in the
        # source code.
        variable_to_load: int = instruction_params["value"]
        variable_address: int = int(self.variables[variable_to_load], 16)

        offset_size: int = instruction_params.get("offset_size", 0)
        offset_register: Union[int, None] = instruction_params.get("offset_register")

        offset = offset_size
        if offset_register:
            offset *= self.registers[offset_register]

        variable_address += offset
        variable_value: Union[int, float] = self.memory[hex(variable_address)]

        destination_register: int = instruction_params["register"]
        self.registers[destination_register] = variable_value

    def LSHIFT(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `LSHIFT` bytecode.

        This method handles the left bit-shift operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = lhs << rhs

    def LT(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `LT` bytecode.

        This method handles the "less than" comparison between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if the expression
        evaluates to `True`, and `0` other wise. This is due to the fact that
        the language does not support boolean literals (`True` and `False`).
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = int(lhs < rhs)

    def MOD(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `MOD` bytecode.

        This method handles the module operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = lhs % rhs

    def MOV(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `MOV` bytecode.

        This method copies the value of one register into another.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs_register: Union[int, str] = instruction_params["register"]
        rhs_register: Union[int, str] = instruction_params["value"]

        # Always insert at the beginning of the list! Appending to the end
        # causes parameter handling to receive arguments in inverted order.
        if lhs_register == "arg":
            self.registers["arg"].insert(0, self.registers[rhs_register])
        elif lhs_register == "ret_value":
            self.registers["ret_value"].append(self.registers[rhs_register])

        else:
            self.registers[lhs_register] = self.registers["ret_value"].pop()

    def MULT(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `MULT` bytecode.

        This method handles the multiplication between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = lhs * rhs

    def NEQ(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `NEQ` bytecode.

        This method handles the "is not equal" comparison between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if the expression
        evaluates to `True`, and `0` other wise. This is due to the fact that
        the language does not support boolean literals (`True` and `False`).
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = int(lhs != rhs)

    def NOT(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `NOT` bytecode.

        This method handles the "logical not" of an integer.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if the expression
        evaluates to `False`, and `0` other wise. This is due to the fact that
        the language does not support boolean literals (`True` and `False`).
        """

        expression = self.registers[instruction_params["expression_register"]]

        self.registers[instruction_params["register"]] = int(not expression)

    def OR(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `OR` bytecode.

        This method handles the "logical or" operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if Python's evaluation
        of `lhs or rhs` results in anything different from `0`. This is due to
        the fact that the language does not support boolean literals (`True` and
        `False`).
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = (
            1 if (lhs or rhs) > 0 else 0
        )

    def RSHIFT(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `RSHIFT` bytecode.

        This method handles the right bit-shift operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = lhs >> rhs

    def SIGNEXT(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `SIGNEXT` bytecode.

        This method extends a 16-bit value to 32 bits. As we are dealing with
        registers, and not the memory directly, the value to extend is simply
        copied to the destination register.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        source_register: int = instruction_params["source_register"]
        destination_register: int = instruction_params["destination_register"]

        self.registers[destination_register] = self.registers[source_register]

    def SITOFP(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `SITOFP` bytecode.

        This method type casts a signed integer to floating point. For the sake
        of simplicity, we'll use Python's conversion.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        source_register: int = instruction_params["source_register"]
        destination_register: int = instruction_params["destination_register"]

        self.registers[destination_register] = float(self.registers[source_register])

    def STORE(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `STORE` bytecode.

        This method stores some value into a memory address.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        variable_address: str = self._get_variable_address(instruction_params)

        value_to_store_register: Union[int, str] = instruction_params["value"]

        if value_to_store_register == "arg":
            value_to_store: Union[int, float] = self.registers["arg"].pop()
        else:
            value_to_store: Union[int, float] = self.registers[value_to_store_register]

        self.memory[variable_address] = value_to_store

    def SUB(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `SUB` bytecode.

        This method handles the subtraction between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_params["lhs_register"]]
        rhs = self.registers[instruction_params["rhs_register"]]

        self.registers[instruction_params["register"]] = lhs - rhs

    def TRUNC(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `TRUNC` bytecode.

        This method truncates a 32-bit value to 16 bits.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        source_register: int = instruction_params["source_register"]
        destination_register: int = instruction_params["destination_register"]

        value_to_truncate: int = self.registers[source_register]
        truncated_value: int = value_to_truncate & 0xFFFF

        if truncated_value & 0x8000:
            truncated_value -= 0x100000

        self.registers[destination_register] = truncated_value

    def _get_variable_address(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> str:
        """
        Get the address of some variable from the instruction_params.

        This method is intended to be used by the `STORE` instruction handler.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Returns
        -------
        variable_address : str
            The address of the variable in the `self.memory` dictionary.
        """

        lhs_register: int = instruction_params["register"]
        lhs_register_contents: Union[int, str] = self.registers[lhs_register]

        # Case 1: writing to some simple variable (i.e., the `lhs_register`
        # contains its `id`)
        if isinstance(lhs_register_contents, int):
            variable_address: str = self.variables[lhs_register_contents]

        # Case 2: writing to an element of an array or struct (i.e., the
        # `lhs_register` contains the address of the element to write to)
        else:
            variable_address: str = lhs_register_contents

        return variable_address
