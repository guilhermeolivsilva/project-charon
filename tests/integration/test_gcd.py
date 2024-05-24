"""Test if the language correctly computes the Greatest Common Divisor."""

from src.interpreter import create_instance


def test_gcd():
    """Test the computation of the GCD between 100 and 125."""

    source_code = """
    {
        i = 125;
        j = 100;
        while (i - j) {
            if (i < j) {
                j = j - i;
            }
            else {
                i = i - j;
            }
        } 
    }
    """

    instance = create_instance(source_code)

    vm, frontend_certificate, backend_certificate = instance.values()
    assert frontend_certificate == backend_certificate

    vm.run()
    assert vm.variables == {"i": 25, "j": 25}
