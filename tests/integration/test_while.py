"""Integration test for a simple `while` statement."""

from src.interpreter import create_virtual_machine


def test_simple_while():
    """Test the `while` statement."""

    source_code = """
    {
        i = 1;
        while (i < 100) {
            i = i + i;
        }
    }
    """

    vm = create_virtual_machine(source_code)
    vm.run()

    assert vm.variables == {"i": 128}
