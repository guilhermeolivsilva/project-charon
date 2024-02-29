"""Integration test for the `do/while` statement."""

from src.interpreter import create_virtual_machine


def test_do_while():
    """Test the `do_while` statement."""

    source_code = """
    {
        i = 1;
        do { i = i + 10; }
        while (i < 50); 
    }
    """

    vm = create_virtual_machine(source_code)
    vm.run()

    assert vm.variables == {"i": 51}
