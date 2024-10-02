"""Test if the language correctly computes the Greatest Common Divisor (GCD)."""

from src.runner import create_instance

SOURCE_CODE = """
int main() {
    int i;
    i = 125;

    int j;
    j = 100;

    while (i - j) {
        if (i < j) {
            j = j - i;
        }
        else {
            i = i - j;
        }
    }

    return 0;
}
"""


def test_gcd() -> None:
    """Test the computation of the GCD between 100 and 125."""

    instance = create_instance(source_code=SOURCE_CODE)
    vm = instance.get("vm")
    vm.run()

    expected_memory = {'0x0': 25, '0x4': 25}
    assert vm.get_memory() == expected_memory
