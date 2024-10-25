"""Implement the main function of the Project [C]haron environment."""

import sys

from src.runner import create_instance


def main() -> int:
    """
    Read the source code from the stdin, compile it and run it in the Virtual Machine.

    The variables of the VM are printed after the execution.
    """

    source_code: str = sys.stdin.read()

    instance = create_instance(source_code)

    vm = instance.get_vm()

    frontend_certificator = instance.get_frontend_certificator()
    backend_certificator = instance.get_backend_certificator()

    frontend_certificate = ...
    backend_certificate = ...

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
    vm.print()

    return 0


if __name__ == '__main__':
    main()
