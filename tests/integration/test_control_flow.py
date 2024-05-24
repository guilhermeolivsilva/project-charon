"""Integration test that checks if the control flow works correctly."""

from src.interpreter import create_instance


SOURCE_CODE = """
{{
    i = {placeholder};
    if (i < 5) {{
        x = 1;
    }}
    else {{
        y = 2;
    }}
}}
"""


def test_if():
    """Test the `if` case."""

    placeholder = 1

    instance = create_instance(SOURCE_CODE.format(**{"placeholder": placeholder}))

    vm, frontend_certificate, backend_certificate = instance.values()
    assert frontend_certificate == backend_certificate

    vm.run()
    assert vm.variables == {"i": placeholder, "x": 1}


def test_else():
    """Test the `else` case."""

    placeholder = 10

    instance = create_instance(SOURCE_CODE.format(**{"placeholder": placeholder}))

    vm, frontend_certificate, backend_certificate = instance.values()
    assert frontend_certificate == backend_certificate

    vm.run()
    assert vm.variables == {"i": placeholder, "y": 2}
