"""Implement a virtual machine that computes generated code."""

from typing import Union


class VirtualMachine:
    """
    Virtual Machine that computes instructions from the `CodeGenerator`.

    Parameters
    ----------
    code_collection : list
        List of tuples generated by the `CodeGenerator`.
    """

    def __init__(
        self,
        code_collection: list[dict[str, Union[int, str, None]]],
        stack_size: int = 1000
    ) -> None:

        self.variables: dict[str, str] = {}
        self.stack: list[Union[int, str, None]] = [None for _ in range(0, stack_size)]
        self.code_collection: list[dict[str, Union[int, str, None]]] = code_collection
        self.stack_pointer: int = 0
        self.program_counter: int = 0

    def __str__(self) -> str:
        """
        Generate a string representation of the VirtualMachine object.

        Returns
        -------
        : str
            The string representation.
        """

        _stack_str = ', '.join(str(item) for item in self.stack if item is not None)
        stack_info = f"Stack (`None` is omitted): [{_stack_str}]"

        _variables_str = str(self.variables)
        variables_info = f"Variables: {_variables_str}"

        return stack_info + "\n" + variables_info

    def run(self) -> None:
        """Run the program on the virtual machine."""

        while True:
            code_metadata = self.code_collection[self.program_counter]
            instruction = code_metadata.get("instruction")

            if instruction == "HALT":
                break

            instruction_handler = getattr(self, instruction.lower())
            instruction_handler(**code_metadata)

            self.program_counter += 1

    def ifetch(self, value: str, **kwargs) -> None:
        """
        Fetch the contents of a variable and push it to the stack.

        Parameters
        ----------
        value : str
            The name of the variable to fetch.
        """

        self.stack[self.stack_pointer] = self.variables[value]
        self.stack_pointer += 1

    def istore(self, value: str, **kwargs) -> None:
        """
        Store the (n-1)th element of the stack in a variable.

        Parameters
        ----------
        value : str
            The name of the variable to store at.
        """

        self.variables[value] = self.stack[self.stack_pointer - 1]

    def ipush(self, value: int, **kwargs) -> None:
        """
        Push an integer to the top of the stack.

        Parameters
        ----------
        value : int
            The integer to push to the stack.
        """

        self.stack[self.stack_pointer] = value
        self.stack_pointer += 1

    def ipop(self, **kwargs) -> None:
        """Pop a value from the stack and discard it."""

        self.stack[self.stack_pointer] = None
        self.stack_pointer -= 1

    def iadd(self, **kwargs) -> None:
        """
        Add the contents of the (n-1)th and (n-2)th elements of the stack.
        """

        self.stack[self.stack_pointer - 2] += self.stack[self.stack_pointer - 1]
        self.stack_pointer -= 1

    def isub(self, **kwargs) -> None:
        """
        Subtract the contents of the (n-1)th and (n-2)th elements of the stack.
        """

        self.stack[self.stack_pointer - 2] -= self.stack[self.stack_pointer - 1]
        self.stack_pointer -= 1

    def ilt(self, **kwargs) -> None:
        """
        Check whether the (n-2)th element of the stack is less than the (n-1)th.
        """

        self.stack[self.stack_pointer - 2] = (
            self.stack[self.stack_pointer - 2] < self.stack[self.stack_pointer - 1]
        )
        self.stack_pointer -= 1

    def jmp(self, value: int, **kwargs) -> None:
        """
        Point the program counter to the instruction referenced by an ID.

        Parameters
        ----------
        value : int
            The ID of the target instruction to jump to.
        """

        initial_program_couter = self.program_counter

        # Look forward (i.e., after the current instruction)
        for code_metadata in self.code_collection[initial_program_couter + 1:]:
            if code_metadata["id"] == value:
                return

            self.program_counter += 1
            
        self.program_counter = 0

        # Look backwards (i.e., before the instruction that triggered this)
        for code_metadata in self.code_collection[:initial_program_couter]:
            if code_metadata["id"] == value:
                # Offset the default PC incrementer, to avoid dealignment
                self.program_counter -= 1
                return

            self.program_counter += 1

    def jz(self, value: int, **kwargs) -> None:
        """
        Compute the next block of code if the parenthesis expression evaluates to `True`.

        If it is `False`, then jump to the node of reference (i.e., `node`).

        Parameters
        ----------
        value : int
            The ID of the target instruction to jump to.
        """

        if self.stack[self.stack_pointer - 1]:
            return
        else:
            self.jmp(value)

    def jnz(self, value: int, **kwargs) -> None:
        """
        Compute the next block of code if the parenthesis expression evaluates to `False`.

        If it is `True`, then jump to the node of reference (i.e., `node`).

        Parameters
        ----------
        value : int
            The ID of the target instruction to jump to.
        """

        if not self.stack[self.stack_pointer - 1]:
            return
        else:
            self.jmp(value)

    def seq(self, **kwargs) -> None:
        """
        Do nothing.

        This simply marks there is a sequence of commands following this
        instruction.
        """

        return

    def empty(self, **kwargs) -> None:
        """
        Do nothing.
        
        Useful when creating "code holes".
        """

        return
