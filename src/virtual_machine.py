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
    stack_size : int, optional (default = 1024)
        The stack size, in positions, to use.
    memory_size : int, optional (default = 1024)
        The memory size, in bytes, to use.
    """

    def __init__(
        self,
        program: dict[str, Union[list, dict]],
        stack_size: int = 1024,
        memory_size: int = 1024
    ) -> None:
        self.program: dict[str, Union[list, dict]] = program

        # Stack
        self.stack: list[Union[int, float]] = []
        self.stack_pointer: int = 0
        self.stack_size: int = stack_size

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

    def __str__(self) -> str:
        """
        Generate a string representation of the VirtualMachine object.

        Returns
        -------
        : str
            The string representation.
        """

        ...

    def print(self) -> None:
        """Print this VirtualMachine object."""

        print(self)

    def run(self) -> None:
        """Run the program on the virtual machine."""

        ...

    def ADD(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `ADD` bytecode.

        This method handles the addition between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs + rhs

    def ALLOC(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `ALLOC` bytecode.

        This method allocates memory for a variable.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Raises
        ------
        MemoryError
            Raised if the memory is full when this method is called, or if the
            available memory is not enough for the variable being allocated.
        """

        if self.memory_pointer >= self.memory_size:
            err_msg: str = "Cannot allocate memory: memory is full"
            err_msg += f"\nInstruction: {instruction_metadata}"
            raise MemoryError(err_msg)

        variable_relative_position = instruction_metadata.get("relative_position")
        self.variables[variable_relative_position] = hex(self.memory_pointer)

        variable_type = instruction_metadata.get("type")
        variable_size = self._get_variable_size(variable_type)
        variable_length = instruction_metadata.get("length", 1)

        updated_memory_pointer: int = self.memory_pointer
        updated_memory_pointer += (variable_size * variable_length)

        if updated_memory_pointer >= self.memory_size:
            err_msg: str = "Not enough memory to allocate a new variable."
            err_msg += f"\nInstruction: {instruction_metadata}"

            raise MemoryError(err_msg)
        
        self.memory_pointer = updated_memory_pointer

    def AND(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `AND` bytecode.

        This method handles the "logical and" operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if Python's evaluation
        of `lhs and rhs` results in anything different from `0`. This is due to
        the fact that the language does not support boolean literals (`True` and
        `False`).
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = (
            1 if (lhs and rhs) > 0 else 0
        )

    def BITAND(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `BITAND` bytecode.

        This method handles the bit-wise "and" operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs & rhs

    def BITOR(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `BITOR` bytecode.

        This method handles the bit-wise "or" operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs | rhs

    def CALL(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `CALL` bytecode.

        This method handles the call to a function.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        ...

    def CONSTANT(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `CONSTANT` bytecode.

        This method saves the constant in some register.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        destination_register: int = instruction_metadata.get("register")
        constant_value: int = instruction_metadata.get("value")

        self.registers[destination_register] = constant_value

    def DIV(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `DIV` bytecode.

        This method handles the division between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = int(lhs / rhs)

    def ELEMENT_PTR(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `ELEMENT_PTR` bytecode.

        This method loads the address of an element from an array or struct
        into a register. It can handle both static (when accessing a struct
        attribute or an array element with a constant index) and dynamic (when
        accessing an array element with a variable as index) accesses.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        offset_mode: str = instruction_metadata.get("offset_mode")
        variable_relative_position: int = instruction_metadata.get("variable_relative_position")
        variable_initial_address: int = int(self.variables[variable_relative_position], 16)

        if offset_mode == "static":
            element_offset: int = instruction_metadata.get("offset_size")

        else:
            index_variable_register: int = instruction_metadata.get("element_register")
            index_variable_value: int = self.registers[index_variable_register]
            variable_type_size: int = instruction_metadata.get("variable_type_size")

            element_offset: int = index_variable_value * variable_type_size

        element_address: str = hex(variable_initial_address + element_offset)

        register_to_write: int = instruction_metadata.get("register")
        self.registers[register_to_write] = element_address

    def EQ(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `EQ` bytecode.

        This method handles the "is equal" comparison between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if the expression
        evaluates to `True`, and `0` other wise. This is due to the fact that
        the language does not support boolean literals (`True` and `False`).
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = int(lhs == rhs)

    def FADD(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FADD` bytecode.

        This method handles the addition between two floating point numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs + rhs

    def FAND(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FAND` bytecode.

        This method handles the "logical and" operation between two floating
        point numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if Python's evaluation
        of `lhs and rhs` results in anything different from `0`. This is due to
        the fact that the language does not support boolean literals (`True` and
        `False`).
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = (
            1 if (lhs and rhs) > 0 else 0
        )

    def FDIV(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FDIV` bytecode.

        This method handles the division between two floating point numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs / rhs

    def FEQ(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FEQ` bytecode.

        This method handles the "is equal" comparison between two floating point
        numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if the expression
        evaluates to `True`, and `0` other wise. This is due to the fact that
        the language does not support boolean literals (`True` and `False`).
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = int(lhs == rhs)

    def FGT(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FGT` bytecode.

        This method handles the "greater than" comparison between two floating
        point numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if the expression
        evaluates to `True`, and `0` other wise. This is due to the fact that
        the language does not support boolean literals (`True` and `False`).
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = int(lhs > rhs)

    def FLT(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FLT` bytecode.

        This method handles the "less than" comparison between two floating
        point numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if the expression
        evaluates to `True`, and `0` other wise. This is due to the fact that
        the language does not support boolean literals (`True` and `False`).
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = int(lhs < rhs)

    def FMULT(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FMULT` bytecode.

        This method handles the multiplication between two floating point
        numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs * rhs

    def FOR(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FOR` bytecode.

        This method handles the "logical or" operation between two floating
        point numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if Python's evaluation
        of `lhs or rhs` results in anything different from `0`. This is due to
        the fact that the language does not support boolean literals (`True` and
        `False`).
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = (
            1 if (lhs or rhs) > 0 else 0
        )

    def FPTOSI(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FPTOSI` bytecode.

        This method type casts a floating point to signed integer. For the sake
        of simplicity, we'll use Python's conversion.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        source_register: int = instruction_metadata.get("source_register")
        destination_register: int = instruction_metadata.get("destination_register")

        self.registers[destination_register] = int(self.registers[source_register])

    def FSUB(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `FSUB` bytecode.

        This method handles the subtraction between two floating point numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs - rhs

    def GT(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `GT` bytecode.

        This method handles the "greater than" comparison between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if the expression
        evaluates to `True`, and `0` other wise. This is due to the fact that
        the language does not support boolean literals (`True` and `False`).
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = int(lhs > rhs)

    def HALT(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `HALT` bytecode.

        This method handles the end of the execution of a program. For this
        instruction, the `instruction_metadata` is ignored.
        """

        return

    def JMP(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `JMP` bytecode.

        This method handles unconditional jumps.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        jump_size: int = instruction_metadata.get("jump_size")
        self.program_counter += jump_size - 1

    def JNZ(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `JNZ` bytecode.

        This method handles conditional jumps: if the evaluated value is not
        zero, jump some amount of instructions.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        condition: int = self.stack.pop()

        if condition:
            jump_size: int = instruction_metadata.get("jump_size")
            self.program_counter += jump_size - 1

    def JZ(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `JZ` bytecode.

        This method handles conditional jumps: if the evaluated value is zero,
        jump some amount of instructions.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        condition: int = self.stack.pop()

        if not condition:
            jump_size: int = instruction_metadata.get("jump_size")
            self.program_counter += jump_size - 1

    def LOAD(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `LOAD` bytecode.

        This method loads the value of a variable into a register.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        # Value represents the variable to load's relative position in the
        # source code.
        variable_to_load: int = instruction_metadata.get("value")
        destination_register: int = instruction_metadata.get("register")

        variable_address: str = self.variables[variable_to_load]

        variable_value: Union[int, float] = self.memory[variable_address]

        self.registers[destination_register] = variable_value

    def LSHIFT(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `LSHIFT` bytecode.

        This method handles the left bit-shift operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs << rhs

    def LT(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `LT` bytecode.

        This method handles the "less than" comparison between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if the expression
        evaluates to `True`, and `0` other wise. This is due to the fact that
        the language does not support boolean literals (`True` and `False`).
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = int(lhs < rhs)

    def MULT(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `MULT` bytecode.

        This method handles the multiplication between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs * rhs

    def PARAM(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `PARAM` bytecode.

        This method handles the passing of arguments to functions.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        ...

    def OR(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `OR` bytecode.

        This method handles the "logical or" operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Notes
        -----
        This method writes `1` in the target `register` if Python's evaluation
        of `lhs or rhs` results in anything different from `0`. This is due to
        the fact that the language does not support boolean literals (`True` and
        `False`).
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = (
            1 if (lhs or rhs) > 0 else 0
        )

    def RET(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `RET` bytecode.

        This method handles the `return` statement of a function.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        ...

    def RSHIFT(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `RSHIFT` bytecode.

        This method handles the right bit-shift operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs >> rhs

    def SIGNEXT(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `SIGNEXT` bytecode.

        This method extends a 16-bit value to 32 bits. As we are dealing with
        registers, and not the memory directly, the value to extend is simply
        copied to the destination register.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        source_register: int = instruction_metadata.get("source_register")
        destination_register: int = instruction_metadata.get("destination_register")

        self.registers[destination_register] = self.registers[source_register]

    def SITOFP(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `SITOFP` bytecode.

        This method type casts a signed integer to floating point. For the sake
        of simplicity, we'll use Python's conversion.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        source_register: int = instruction_metadata.get("source_register")
        destination_register: int = instruction_metadata.get("destination_register")

        self.registers[destination_register] = float(self.registers[source_register])

    def STORE(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
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
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        variable_address: str = self._get_variable_address(instruction_metadata)

        value_to_store_register: int = instruction_metadata.get("rhs_register")
        value_to_store: Union[int, float] = self.registers[value_to_store_register]

        self.memory[variable_address] = value_to_store

    def SUB(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `SUB` bytecode.

        This method handles the subtraction between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs - rhs

    def TRUNC(
        self,
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> None:
        """
        Handle a `TRUNC` bytecode.

        This method truncates a 32-bit value to 16 bits.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.
        """

        source_register: int = instruction_metadata.get("source_register")
        destination_register: int = instruction_metadata.get("destination_register")

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
        instruction_metadata: dict[str, Union[int, float, str]]
    ) -> str:
        """
        Get the address of some variable from the instruction_metadata.

        This method is intended to be used by the `LOAD` and `STORE`
        instruction handlers.

        Parameters
        ----------
        instruction_metadata : dict[str, Union[int, float, str]]
            The bytecode metadata.

        Returns
        -------
        variable_address : str
            The address of the variable in the `self.memory` dictionary.
        """

        lhs_register: int = instruction_metadata.get("lhs_register")
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
