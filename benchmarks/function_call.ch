int factorial(int x) {
    int fact;
    fact = 1;

    while(x > 0) {
        fact = fact * x;
        x = x - 1;
    }

    return fact;
}


int main() {
    int i;
    i = factorial(5);

    return 0;
}
