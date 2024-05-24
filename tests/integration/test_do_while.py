"""Integration test for the `do/while` statement."""

from src.interpreter import create_instance


def test_do_while():
    """Test the `do_while` statement."""

    source_code = """
    {
        i = 1;
        do { i = i + 10; }
        while (i < 50); 
    }
    """

    instance = create_instance(source_code)

    vm, frontend_certificate, backend_certificate = instance.values()
    assert frontend_certificate == backend_certificate

    vm.run()
    assert vm.variables == {"i": 51}
