"""Integration test for a simple `while` statement."""

from src.interpreter import create_instance


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

    instance = create_instance(source_code)

    vm, frontend_certificate, backend_certificate = instance.values()
    assert frontend_certificate == backend_certificate

    vm.run()
    assert vm.variables == {"i": 128}
