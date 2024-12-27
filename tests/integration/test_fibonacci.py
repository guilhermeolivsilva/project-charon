"""
Test if the language correctly computes the 10th element of the Fibonacci sequence.
"""

from src.certificators import BackendCertificator, FrontendCertificator
from src.runner import create_instance


SOURCE_CODE = """
int main() {
    int i;
    i = 1;

    int a;
    a = 0;

    int b;
    b = 1;

    int c;

    while (i < 10) {
        c = a;
        a = b;
        b = c + a;
        i = i + 1; 
    }

    return 0;
}
"""

def test_fib() -> None:
    """
    Test the computation of the 10th element of the Fibonacci sequence.

    The result is stored in the `b` variable (at 0x8).
    """

    instance = create_instance(source_code=SOURCE_CODE)
    vm = instance.get_vm()
    vm.run()

    expected_memory = {'0x0': 10, '0x4': 34, '0x8': 55, '0xc': 21}
    assert vm.get_memory() == expected_memory


def test_array_certification() -> None:
    """Test the front and backend certification."""

    instance = create_instance(source_code=SOURCE_CODE)

    ast = instance.get_ast()
    frontend_certificate = FrontendCertificator(ast=ast).certificate()

    program = instance.get_program()
    backend_certificate = BackendCertificator(program=program).certificate()

    assert frontend_certificate == backend_certificate
