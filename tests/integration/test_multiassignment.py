"""Test if the language correctly assigns values to variables."""

from src.interpreter import create_instance


def test_gcd():
    """Test the assignement of multiple variables."""

    source_code = """
    {
        a = 1;
        c = 3 < 2;
        b = c;
    }
    """

    instance = create_instance(source_code)

    vm, frontend_certificate, backend_certificate = instance.values()
    assert frontend_certificate == backend_certificate

    vm.run()
    assert vm.variables == {"a": 1, "b": False, "c": False}
