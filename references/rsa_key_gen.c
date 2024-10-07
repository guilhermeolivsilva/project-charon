#include <stdio.h>

int seed;

int myRand() {
    seed = ((1103515245 * seed) + 12345) & ((1 << 31) - 1);
    return seed;
}

int gcd(int a, int b) {
    int temp;

    while (b != 0) {
        temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int modInverse(int e, int phi) {
    int t;
    t = 0;
    
    int new_t;
    new_t = 1;

    int r;
    r = phi;

    int new_r;
    new_r = e;

    int quotient;
    int temp_t;
    int temp_r;

    while (new_r != 0) {
        quotient = (r / new_r);
        temp_t = new_t;

        new_t = t - (quotient * new_t);
        t = temp_t;

        temp_r = new_r;
        new_r = r - (quotient * new_r);
        r = temp_r;
    }
    if (r > 1) {
        return -1;
    }
    if (t < 0) {
        t = t + phi;
    }
    return t;
}

int main() {
    seed = 1;

    int p;
    p = 47;

    int q;
    q = 31;

    int n;
    n = p * q;

    int phi;
    phi = (p - 1) * (q - 1);

    int e;
    do {
        e = (myRand() % (phi - 1));
        e = e + 1;
    } while ((gcd(e, phi)) != 1);

    int d;
    d = modInverse(e, phi);

    printf("RSA Key Generation Complete:\n");
    printf("Prime p: %d\n", p);
    printf("Prime q: %d\n", q);
    printf("n = p * q: %d\n", n);
    printf("ϕ(n): %d\n", phi);
    printf("Public Key (n, e): (%d, %d)\n", n, e);
    printf("Private Key (n, d): (%d, %d)\n", n, d);

    return 0;
}