"""Implement the main function of the Tiny C environment."""

from src.interpreter import create_virtual_machine


def main() -> None:
    """
    Input the source code from the stdin and run it in the Virtual Machine.

    The variables of the VM are printed after the execution.
    """

    source_code: str = input()

    vm = create_virtual_machine(source_code)

    vm.run()
    print(vm.variables)


if __name__ == '__main__':
    main()
