"""Integration test for a simple struct manipulation."""

from src.runner import create_instance


SOURCE_CODE = """
struct my_struct {
    int attribute_1;
    float attribute_2;
    short attribute_3;
};

int main() {
    my_struct struct_var;

    struct_var.attribute_1 = 10;
    struct_var.attribute_2 = 13.1 * 23.4 / 30.2;
    struct_var.attribute_3 = (struct_var.attribute_1) * (struct_var.attribute_2);

    return 0;
}
"""

def test_struct():
    """Test a simple struct."""

    instance = create_instance(source_code=SOURCE_CODE)
    vm = instance.get("vm")
    vm.run()

    expected_memory = {'0x0': 10, '0x4': 10.150331125827813, '0x8': 101}

    assert vm.get_memory() == expected_memory
