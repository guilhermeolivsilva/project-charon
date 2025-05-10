"""Integration test for a simple function call."""

from src.certificators import BackendCertificator, FrontendCertificator
from src.runner import create_instance


SOURCE_CODE = """
int factorial(int x) {
    int fact;
    fact = 1;

    while(x > 0) {
        fact = fact * x;
        x = x - 1;
    }

    return fact;
}


int main() {
    int i;
    i = factorial(5);

    return 0;
}
"""


def test_function_call():
    """Test a function call."""

    instance = create_instance(source_code=SOURCE_CODE)
    vm = instance.get_vm()
    vm.run()

    expected_memory = {"0x0": 0, "0x4": 120, "0x8": 120}
    assert vm.get_memory() == expected_memory


def test_function_call_certification() -> None:
    """Test the front and backend certification."""

    instance = create_instance(source_code=SOURCE_CODE)

    ast = instance.get_ast()
    frontend_certificate = FrontendCertificator(ast=ast).certificate()

    program = instance.get_program()
    backend_certificate = BackendCertificator(program=program).certificate()

    assert frontend_certificate == backend_certificate
