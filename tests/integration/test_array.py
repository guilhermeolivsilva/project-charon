"""Integration test for a simple array manipulation."""

from src.runner import create_instance


SOURCE_CODE = """
int main() {
    int my_array[5];

    int i;
    i = 0;

    while(i < 5) {
        my_array[i] = i << i;
        i = i + 1;
    }

    int j;
    j = (my_array[2]) + 3;

    return 0;
}
"""

def test_array():
    """Test a simple array."""

    instance = create_instance(source_code=SOURCE_CODE)
    vm = instance.get_vm()
    vm.run()

    expected_memory = {
        '0x0': 0,
        '0x4': 2,
        '0x8': 8,
        '0xc': 24,
        '0x10': 64,
        '0x14': 5,
        '0x18': 11
    }

    assert vm.get_memory() == expected_memory
