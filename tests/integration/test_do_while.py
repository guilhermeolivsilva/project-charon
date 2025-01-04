"""Integration test for the `do/while` statement."""

from src.certificators import BackendCertificator, FrontendCertificator
from src.runner import create_instance


SOURCE_CODE = """
int main() {
    int i;
    i = 1;

    do {
        i = i + 10;
    }
    while (i < 50); 

    return 0;
}
"""


def test_do_while() -> None:
    """Test the `do/while` statement."""

    instance = create_instance(source_code=SOURCE_CODE)
    vm = instance.get_vm()
    vm.run()

    expected_memory = {"0x0": 51}
    assert vm.get_memory() == expected_memory


def test_do_while_certification() -> None:
    """Test the front and backend certification."""

    instance = create_instance(source_code=SOURCE_CODE)

    ast = instance.get_ast()
    frontend_certificate = FrontendCertificator(ast=ast).certificate()

    program = instance.get_program()
    backend_certificate = BackendCertificator(program=program).certificate()

    assert frontend_certificate == backend_certificate
