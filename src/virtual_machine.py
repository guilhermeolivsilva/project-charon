"""Implement a virtual machine that computes generated code."""

from src.node import Node


class VirtualMachine:
    """
    Virtual Machine that computes instructions from the `CodeGenerator`.

    Parameters
    ----------
    code_collection : list
        List of tuples generated by the `CodeGenerator`.
    """

    def __init__(self, code_collection: list, stack_size: int = 1000) -> None:

        self.variables = {}
        self.stack = [None for _ in range(0, stack_size)]
        self.code_collection = code_collection
        self.stack_pointer = 0
        self.program_counter = 0

    def run(self) -> None:
        """Run the program on the virtual machine."""

        while True:
            instruction, node = self.code_collection[self.program_counter]

            if instruction == "HALT":
                break

            instruction_handler = getattr(self, instruction.lower())
            instruction_handler(node=node)

            self.program_counter += 1

    def ifetch(self, node: Node, **kwargs) -> None:
        """
        Fetch the contents of a variable and push it to the stack.

        Parameters
        ----------
        node : Node
            The node that references the variable to be fetched.
        """

        self.stack[self.stack_pointer] = self.variables[node.value]
        self.stack_pointer += 1

    def istore(self, node: Node, **kwargs) -> None:
        """
        Store the (n-1)th element of the stack in a variable.

        Parameters
        ----------
        node : Node
            The node that references the variable to store in.
        """

        self.variables[node.value] = self.stack[self.stack_pointer - 1]

    def ipush(self, node: Node, **kwargs) -> None:
        """
        Push the contents of a node to the top of the stack.

        Parameters
        ----------
        node : Node
            The node whose contents will be pushed to the top of the stack.
        """

        self.stack[self.stack_pointer] = node.value
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

    def jmp(self, node: Node, **kwargs) -> None:
        """
        Point the program counter to the instruction referenced by a node.

        Parameters
        ----------
        node : Node
            The node of reference.
        """

        initial_program_couter = self.program_counter

        # Look forward (i.e., after the current instruction)
        for _, other_node in self.code_collection[initial_program_couter + 1:]:
            if other_node == node:
                return

            self.program_counter += 1
            
        self.program_counter = 0

        # Look backwards (i.e., before the instruction that triggered this)
        for _, other_node in self.code_collection[:initial_program_couter]:
            if other_node == node:
                # Offset the default PC incrementer, to avoid dealignment
                self.program_counter -= 1
                return

            self.program_counter += 1

    def jz(self, node: Node) -> None:
        """
        Compute the next block of code if the parenthesis expression evaluates to `True`.

        If it is `False`, then jump to the node of reference (i.e., `node`).

        Parameters
        ----------
        node : Node
            The node of reference.
        """

        if self.stack[self.stack_pointer - 1]:
            return
        else:
            self.jmp(node)


    def jnz(self, node: Node) -> None:
        """
        Compute the next block of code if the parenthesis expression evaluates to `False`.

        If it is `True`, then jump to the node of reference (i.e., `node`).

        Parameters
        ----------
        node : Node
            The node of reference.
        """

        if not self.stack[self.stack_pointer - 1]:
            return
        else:
            self.jmp(node)

    def empty(self, **kwargs) -> None:
        """
        Do nothing.
        
        Useful when creating "code holes".
        """

        return 
