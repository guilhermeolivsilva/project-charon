"""Integration test to showcase expressions."""

from src.certificators import BackendCertificator, FrontendCertificator
from src.runner import create_instance


SOURCE_CODE = """
int main() {
    int i;
    i = 3 + 10 * 2;

    int j;
    j = (i << 1) / 5 % 2 + 15 * 3;

    int k;
    k = !(i | j & 1);

    return 0;
}
"""


def test_expression():
    """Test multiple expressions."""

    instance = create_instance(source_code=SOURCE_CODE)
    vm = instance.get_vm()
    vm.run()

    expected_memory = {"0x0": 23, "0x4": 46, "0x8": 0}
    assert vm.get_memory() == expected_memory


def test_expressions_certification() -> None:
    """Test the front and backend certification."""

    instance = create_instance(source_code=SOURCE_CODE)

    ast = instance.get_ast()
    frontend_certificate = FrontendCertificator(ast=ast).certificate()

    program = instance.get_program()
    backend_certificate = BackendCertificator(program=program).certificate()

    assert frontend_certificate == backend_certificate
