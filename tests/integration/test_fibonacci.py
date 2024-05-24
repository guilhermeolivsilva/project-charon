"""
Test if the language correctly computes the 10th element of the Fibonacci sequence.
"""

from src.interpreter import create_instance


def test_fib():
    """
    Test the computation of the 10th element of the Fibonacci sequence.

    The result is stored in the `b` variable.
    """

    source_code = """
    {
        i = 1;
        a = 0;
        b = 1;
        while (i < 10) {
            c = a;
            a = b;
            b = c + a;
            i = i + 1; 
        }
    }
    """

    instance = create_instance(source_code)

    vm, frontend_certificate, backend_certificate = instance.values()
    assert frontend_certificate == backend_certificate

    vm.run()
    assert vm.variables['b'] == 55
