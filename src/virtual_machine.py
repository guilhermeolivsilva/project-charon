"""Implement a virtual machine that computes generated code."""

from typing import Union

from src.utils import builtin_types


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
        self.registers: dict[int, Union[int, float]] = {}
        self.variables: dict[int, str] = {}

        # Functions
        self.function_call_parameters: list[Union[int, float]] = []
        self.return_program_counter: list[int] = []
        self.return_value_register: list[int] = []

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
            and self.function_call_parameters == other.function_call_parameters
            and self.return_program_counter == other.return_program_counter
            and self.return_value_register == other.return_value_register
        )

        return bool

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
            variable_relative_position: {
                "address": variable_value
            }

            for variable_relative_position, variable_value
            in self.variables.items()
        }

        for key, value in variables_info.items():
            address = value["address"]
            variables_info[key]["value"] = self.memory[address]

        _str += "Variables:\n  "
        _str += "\n  ".join(
            f"Relative position: {relative_position}\n  Data: {data}\n"
            for relative_position, data in variables_info.items()
        )

        return _str

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
        self.program_counter = self.program["functions"]["main"]["start"]

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

        # Value represents the variable to load's relative position in the
        # source code.
        variable_to_load: int = instruction_params["value"]
        variable_address: str = self.variables[variable_to_load]

        destination_register: int = instruction_params["register"]
        self.registers[destination_register] = variable_address

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

        variable_relative_position = instruction_params["relative_position"]

        variable_type = instruction_params["type"]
        variable_size = self._get_variable_size(variable_type)
        variable_length = instruction_params.get("length", 1)

        updated_memory_pointer: int = self.memory_pointer
        updated_memory_pointer += (variable_size * variable_length)

        if updated_memory_pointer >= self.memory_size:
            err_msg: str = "Not enough memory to allocate a new variable."
            err_msg += f"\nInstruction: {instruction_params}"

            raise MemoryError(err_msg)
        
        self.variables[variable_relative_position] = hex(self.memory_pointer)
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

    def CALL(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `CALL` bytecode.

        This method handles the call to a function.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        # Handle the `program_counter` for it to point to the function code
        called_function_relative_position: int = instruction_params["value"]
        called_function_name: str = (
            list(self.program["functions"].keys())[called_function_relative_position - 1]
        )
        called_function_start: int = (
            self.program["functions"][called_function_name]["start"]
        )

        # Save the parameters, if any, to the `function_call_parameters` register
        parameters_registers: list[int] = reversed(
            instruction_params["parameters_registers"]
        )
        for parameter_register in parameters_registers:
            parameter_value = self.registers[parameter_register]
            self.function_call_parameters.append(parameter_value)

        # Save the current state (i.e., the `program_counter` and `registers`)
        self.return_program_counter.append(self.program_counter)
        self.program_counter = called_function_start

        # And, finally, save the register to write the call result
        return_value_register: int = instruction_params["register"]
        self.return_value_register.append(return_value_register)

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

    def ELEMENT_PTR(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `ELEMENT_PTR` bytecode.

        This method loads the address of an element from an array or struct
        into a register. It can handle both static (when accessing a struct
        attribute or an array element with a constant index) and dynamic (when
        accessing an array element with a variable as index) accesses.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        offset_mode: str = instruction_params["offset_mode"]
        variable_relative_position: int = instruction_params["variable_relative_position"]
        variable_initial_address: int = int(self.variables[variable_relative_position], 16)

        if offset_mode == "static":
            element_offset: int = instruction_params["offset_size"]

        else:
            index_variable_register: int = instruction_params["element_register"]
            index_variable_value: int = self.registers[index_variable_register]
            variable_type_size: int = instruction_params["variable_type_size"]

            element_offset: int = index_variable_value * variable_type_size

        element_address: str = hex(variable_initial_address + element_offset)

        register_to_write: int = instruction_params["register"]
        self.registers[register_to_write] = element_address

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

    def JMP(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `JMP` bytecode.

        This method handles unconditional jumps.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        jump_size: int = instruction_params["jump_size"]
        self.program_counter += jump_size - 1

    def JNZ(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `JNZ` bytecode.

        This method handles conditional jumps: if the evaluated value is not
        zero, jump some amount of instructions.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        conditional_register: int = instruction_params["conditional_register"]
        condition: int = self.registers[conditional_register]

        if condition:
            jump_size: int = instruction_params["jump_size"]
            self.program_counter += jump_size - 1

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
        `self.ELEMENT_PTR` will handle this later.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        # Value represents the variable to load's relative position in the
        # source code.
        variable_to_load: int = instruction_params["value"]
        variable_address: str = self.variables[variable_to_load]
        variable_value: Union[int, float] = self.memory[variable_address]

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

    def PARAM(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `PARAM` bytecode.

        This method handles the passing of arguments to functions.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        I hate this design. It does too much.
        """

        if self.memory_pointer >= self.memory_size:
            err_msg: str = "Cannot allocate memory: memory is full"
            err_msg += f"\nInstruction: {instruction_params}"
            raise MemoryError(err_msg)

        parameter_relative_position = instruction_params["relative_position"]
        parameter_type = instruction_params["type"]
        parameter_size = self._get_variable_size(parameter_type)
        parameter_length = instruction_params.get("length", 1)

        parameter_address: str = hex(self.memory_pointer)
        updated_memory_pointer: int = self.memory_pointer + (parameter_size * parameter_length)

        if updated_memory_pointer >= self.memory_size:
            err_msg: str = "Not enough memory to allocate a new variable."
            err_msg += f"\nInstruction: {instruction_params}"

            raise MemoryError(err_msg)

        self.variables[parameter_relative_position] = parameter_address
        self.memory_pointer = updated_memory_pointer

        parameter_value: Union[int, float] = self.function_call_parameters.pop()
        self.memory[parameter_address] = parameter_value

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

    def RET(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `RET` bytecode.

        This method handles the `return` statement of a function.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        # Save the returned value to the appropriate register, if any
        if self.return_value_register:
            register_with_value_to_return: int = instruction_params["register"]
            return_value_register: int = self.return_value_register.pop()

            self.registers[return_value_register] = self.registers[register_with_value_to_return]

        # Restore the `program_counter`
        if self.return_program_counter:
            self.program_counter = self.return_program_counter.pop()

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

        This method stores some value into a variable.

        There are two possible cases when storing data in a variable: the
        variable is a simple variable, or the variable is an array or struct.
        In the first case, the `lhs_register` will contain an integer -- the
        variable identifier (i.e., its `relative_position`, that indexes the
        `self.variables` dict); in the second case, it will contain the address
        to the memory position to be written to.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        variable_address: str = self._get_variable_address(instruction_params)

        value_to_store_register: int = instruction_params["rhs_register"]
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

    def _get_variable_size(self, type: str) -> int:
        """
        Get the size of a variable, in bytes, from its type.

        Parameters
        ----------
        type : str
            The type of the variable.

        Returns
        -------
        type_size : int
            The size of the variable type, in bytes.
        """

        type_size: int = 0

        # Case 1: variable is of a built-in type
        if type in builtin_types:
            type_size = builtin_types[type]

            return type_size

        # Case 2: variable is a struct
        struct_types = self.program["structs"][type]

        for attr_type in struct_types:
            type_size += self._get_variable_size(attr_type)

        return type_size
    
    def _get_variable_address(
        self,
        instruction_params: dict[str, Union[int, float, str]]
    ) -> str:
        """
        Get the address of some variable from the instruction_params.

        This method is intended to be used by the `LOAD` and `STORE`
        instruction handlers.

        Parameters
        ----------
        instruction_params : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Returns
        -------
        variable_address : str
            The address of the variable in the `self.memory` dictionary.
        """

        lhs_register: int = instruction_params["lhs_register"]
        lhs_register_contents: Union[int, str] = self.registers[lhs_register]

        # Case 1: writing to some simple variable (i.e., the `lhs_register`
        # contains its `relative_position`)
        if isinstance(lhs_register_contents, int):
            variable_address: str = self.variables[lhs_register_contents]

        # Case 2: writing to an element of an array or struct (i.e., the
        # `lhs_register` contains the address of the element to write to)
        else:
            variable_address: str = lhs_register_contents

        return variable_address
