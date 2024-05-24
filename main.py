"""Implement the main function of the Tiny C environment."""

from src.interpreter import create_instance


def main() -> None:
    """
    Input the source code from the stdin and run it in the Virtual Machine.

    The variables of the VM are printed after the execution.
    """

    source_code: str = input()

    instance = create_instance(source_code)

    vm, frontend_certificate, backend_certificate = instance.values()

    print("Frontend certificate:")
    print(frontend_certificate)

    print("Backend certificate:")
    print(backend_certificate)

    try:
        assert frontend_certificate == backend_certificate
        print("Certificates match!")
    except AssertionError:
        print("Certificates don't match. Aborting...")
        return 1

    vm.run()
    print(vm.variables)


if __name__ == '__main__':
    main()
