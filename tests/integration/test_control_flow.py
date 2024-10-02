"""Integration test that checks if the control flow works correctly."""

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
    vm = instance.get("vm")
    vm.run()

    expected_memory = {'0x0': placeholder, '0x4': 23}
    assert vm.get_memory() == expected_memory


def test_else() -> None:
    """Test the `else` case."""

    placeholder = 10
    source_code = SOURCE_CODE.format(placeholder=placeholder)

    instance = create_instance(source_code=source_code)
    vm = instance.get("vm")
    vm.run()

    expected_memory = {'0x0': placeholder, '0x4': 35}
    assert vm.get_memory() == expected_memory
