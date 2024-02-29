"""Integration test for a complex `while` statement."""

from src.interpreter import create_virtual_machine


def test_complex_while():
    """Test the `while` statement."""

    source_code = """
    {
        i = 1;
        while ((i = i + 10) < 50);
    }
    """

    vm = create_virtual_machine(source_code)
    vm.run()

    assert vm.variables == {"i": 51}
