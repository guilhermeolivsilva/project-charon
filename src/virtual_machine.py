"""Implement a virtual machine that computes generated code."""


class VirtualMachine:
    """Virtual Machine that computes instructions from the `CodeGenerator`."""

    def __init__(self) -> None:
        self.globals = {
            chr(i): 0 for i in range(ord('a'), ord('z') + 1)
        }

        self.stack = []
        self.stack_pointer = 0
