"""Integration test for a simple `while` statement."""

from src.runner import create_instance



SOURCE_CODE = """
int main() {
    int i;
    i = 1;

    while (i < 100) {
        i = i + i;
    }

    return 0;
}
"""

def test_simple_while() -> None:
    """Test the `while` statement."""

    instance = create_instance(source_code=SOURCE_CODE)
    vm = instance.get("vm")
    vm.run()

    expected_memory = {'0x0': 128}
    assert vm.get_memory() == expected_memory
