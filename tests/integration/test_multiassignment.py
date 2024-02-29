"""Test if the language correctly assigns values to variables."""

from src.interpreter import create_virtual_machine


def test_gcd():
    """Test the assignement of multiple variables."""

    source_code = """
    {
        a = 1;
        c = 3 < 2;
        b = c;
    }
    """

    vm = create_virtual_machine(source_code)
    vm.run()

    assert vm.variables == {"a": 1, "b": False, "c": False}
