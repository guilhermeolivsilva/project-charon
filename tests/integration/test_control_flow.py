"""Integration test that checks if the control flow works correctly."""

from src.certificators import BackendCertificator, FrontendCertificator
from src.runner import create_instance


SOURCE_CODE = """
int main() {{
    int i;
    i = {placeholder};

    int x;

    if (i < 5) {{
        x = 23;
    }}
    else {{
        x = 35;
    }}

    return 0;
}}
"""


def test_if() -> None:
    """Test the `if` case."""

    placeholder = 1
    source_code = SOURCE_CODE.format(placeholder=placeholder)

    instance = create_instance(source_code=source_code)
    vm = instance.get_vm()
    vm.run()

    expected_memory = {"0x0": placeholder, "0x4": 23}
    assert vm.get_memory() == expected_memory


def test_else() -> None:
    """Test the `else` case."""

    placeholder = 10
    source_code = SOURCE_CODE.format(placeholder=placeholder)

    instance = create_instance(source_code=source_code)
    vm = instance.get_vm()
    vm.run()

    expected_memory = {"0x0": placeholder, "0x4": 35}
    assert vm.get_memory() == expected_memory


# def test_control_flow_certification() -> None:
#     """Test the front and backend certification."""

#     # The placeholder does not really matter.
#     placeholder = 10
#     source_code = SOURCE_CODE.format(placeholder=placeholder)

#     instance = create_instance(source_code=source_code)

#     ast = instance.get_ast()
#     frontend_certificate = FrontendCertificator(ast=ast).certificate()

#     program = instance.get_program()
#     backend_certificate = BackendCertificator(program=program).certificate()

#     assert frontend_certificate == backend_certificate
