"""Implement a virtual machine that computes generated code."""

from typing import Union


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
        self.memory: dict[str, Union[int, float, None]] = {
            hex(_byte): None
            for _byte in range(memory_size)
        }
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

    def ADD(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `ADD` bytecode.

        This method handles the addition between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs + rhs

    def ALLOC(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `ALLOC` bytecode.

        This method allocates memory for a variable.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        if self.memory_pointer >= len(self.memory):
            raise MemoryError("Cannot allocate memory: memory is full.")

        variable_relative_position = instruction_metadata.get("relative_position")
        self.variables[variable_relative_position] = self.memory_pointer

        variable_type = instruction_metadata.get("type")
        variable_size = self.get_type_size(variable_type)
        variable_length = instruction_metadata.get("length", 1)

        self.memory_pointer += variable_size * variable_length

    def AND(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `AND` bytecode.

        This method handles the "logical and" operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
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

    def BITAND(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `BITAND` bytecode.

        This method handles the bit-wise "and" operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs & rhs

    def BITOR(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `BITOR` bytecode.

        This method handles the bit-wise "or" operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs | rhs

    def CALL(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `CALL` bytecode.

        This method handles the call to a function.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        ...

    def CONSTANT(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `CONSTANT` bytecode.

        This method saves the constant at some register.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        destination_register: int = instruction_metadata.get("register")
        constant_value: int = instruction_metadata.get("value")

        self.registers[destination_register] = constant_value

    def DIV(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `DIV` bytecode.

        This method handles the division between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs / rhs

    def ELEMENT_PTR(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `ELEMENT_PTR` bytecode.

        This method gets the pointer of an array or struct element.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        ...

    def EQ(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `EQ` bytecode.

        This method handles the "is equal" comparison between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
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

    def FADD(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `FADD` bytecode.

        This method handles the addition between two floating point numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs + rhs

    def FAND(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `FAND` bytecode.

        This method handles the "logical and" operation between two floating
        point numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
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

    def FDIV(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `FDIV` bytecode.

        This method handles the division between two floating point numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs / rhs

    def FEQ(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `FEQ` bytecode.

        This method handles the "is equal" comparison between two floating point
        numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
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

    def FGT(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `FGT` bytecode.

        This method handles the "greater than" comparison between two floating
        point numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
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

    def FLT(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `FLT` bytecode.

        This method handles the "less than" comparison between two floating
        point numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
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

    def FMULT(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `FMULT` bytecode.

        This method handles the multiplication between two floating point
        numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs * rhs

    def FOR(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `FOR` bytecode.

        This method handles the "logical or" operation between two floating
        point numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
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

    def FPTOSI(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `FPTOSI` bytecode.

        This method type casts a floating point to signed integer. For the sake
        of simplicity, we'll use Python's conversion.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        source_register: int = instruction_metadata.get("source_register")
        destination_register: int = instruction_metadata.get("destination_register")

        self.registers[destination_register] = int(self.registers[source_register])

    def FSUB(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `FSUB` bytecode.

        This method handles the subtraction between two floating point numbers.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs - rhs

    def GT(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `GT` bytecode.

        This method handles the "greater than" comparison between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
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

    def HALT(self, **kwargs) -> None:
        """
        Handle a `HALT` bytecode.

        This method handles the end of the execution of a program. For this
        instruction, the `instruction_metadata` is ignored.
        """

        return

    def JMP(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `JMP` bytecode.

        This method handles unconditional jumps.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        jump_size: int = instruction_metadata.get("jump_size")
        self.program_counter += jump_size - 1

    def JNZ(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `JNZ` bytecode.

        This method handles conditional jumps: if the evaluated value is not
        zero, jump some amount of instructions.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        condition: int = self.stack.pop()

        if condition:
            jump_size: int = instruction_metadata.get("jump_size")
            self.program_counter += jump_size - 1

    def JZ(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `JZ` bytecode.

        This method handles conditional jumps: if the evaluated value is zero,
        jump some amount of instructions.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        condition: int = self.stack.pop()

        if not condition:
            jump_size: int = instruction_metadata.get("jump_size")
            self.program_counter += jump_size - 1

    def LOAD(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `LOAD` bytecode.

        This method loads the value of a variable into a register.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        # Value represents the variable to load's relative position in the
        # source code.
        variable_to_load: int = instruction_metadata.get("value")
        destination_register: int = instruction_metadata.get("register")

        variable_address: int = self.variables[variable_to_load]

        print(variable_address)

        variable_value: Union[int, float] = self.memory[hex(variable_address)]

        self.registers[destination_register] = variable_value

    def LSHIFT(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `LSHIFT` bytecode.

        This method handles the left bit-shift operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs << rhs

    def LT(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `LT` bytecode.

        This method handles the "less than" comparison between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
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

    def MULT(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `MULT` bytecode.

        This method handles the multiplication between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs * rhs

    def PARAM(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `PARAM` bytecode.

        This method handles the passing of arguments to functions.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        ...

    def OR(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `OR` bytecode.

        This method handles the "logical or" operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
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

    def RET(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `RET` bytecode.

        This method handles the `return` statement of a function.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        ...

    def RSHIFT(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `RSHIFT` bytecode.

        This method handles the right bit-shift operation between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs >> rhs

    def SIGNEXT(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `SIGNEXT` bytecode.

        This method extends a 16-bit value to 32 bits. As we are dealing with
        registers, and not the memory directly, the value to extend is simply
        copied to the destination register.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        source_register: int = instruction_metadata.get("source_register")
        destination_register: int = instruction_metadata.get("destination_register")

        self.registers[destination_register] = self.registers[source_register]

    def SITOFP(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `SITOFP` bytecode.

        This method type casts a signed integer to floating point. For the sake
        of simplicity, we'll use Python's conversion.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        source_register: int = instruction_metadata.get("source_register")
        destination_register: int = instruction_metadata.get("destination_register")

        self.registers[destination_register] = float(self.registers[source_register])

    def STORE(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `STORE` bytecode.

        This method stores some value in a variable.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        variable_relative_position_register: int = instruction_metadata.get("lhs_register")
        variable_address: str = hex(
            self.variables[self.registers[variable_relative_position_register]]
        )

        value_to_store_register: int = instruction_metadata.get("rhs_register")
        value_to_store: Union[int, float] = self.registers[value_to_store_register]

        self.memory[variable_address] = value_to_store

    def SUB(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `SUB` bytecode.

        This method handles the subtraction between two integers.

        `short`-typed values will also use this method.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        lhs = self.registers[instruction_metadata.get("lhs_register")]
        rhs = self.registers[instruction_metadata.get("rhs_register")]

        self.registers[instruction_metadata.get("register")] = lhs - rhs

    def TRUNC(self, instruction_metadata: dict[str, dict]) -> None:
        """
        Handle a `TRUNC` bytecode.

        This method truncates a 32-bit value to 16 bits.

        Parameters
        ----------
        instruction_metadata : dict[str, dict]
            The bytecode metadata.
        """

        source_register: int = instruction_metadata.get("source_register")
        destination_register: int = instruction_metadata.get("destination_register")

        value_to_truncate: int = self.registers[source_register]
        truncated_value: int = value_to_truncate & 0xFFFF

        if truncated_value & 0x8000:
            truncated_value -= 0x100000

        self.registers[destination_register] = truncated_value


    def get_type_size(self, type: str) -> int:
        """
        Get the size of a variable type in bytes.

        Parameters
        ----------
        type : str
            The type of the variable.

        Returns
        -------
        type_size : int
            The size of the variable type, in bytes.
        """

        builtin_types: dict[str, int] = {
            "short": 2,
            "int": 4,
            "float": 4
        }

        type_size: int = 0

        # Case 1: variable is of a built-in type
        if type in builtin_types:
            type_size = builtin_types[type]

            return type_size

        # Case 2: variable is a struct
        struct_types = self.program["structs"][type]

        for attr_type in struct_types:
            type_size += self.get_type_size(attr_type)

        return type_size
