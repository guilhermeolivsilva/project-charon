#include "stdio.h"

int int_sum(int a, int b) {
    return a + b;
}

float float_sum(float a, float b) {
    return a + b;
}

short short_sum(short a, short b) {
    return a + b;
}

int main() {
    int i = int_sum(23, 13);
    float f = float_sum(3.14, 2.71);
    short s = short_sum(1, 2);

    printf("%d", (int)(i + f + s));

    // Composition
    short test_short_1 = i + (f + s);
    short test_short_2 = (2 * i * s) * f;

    int test_int_1 = i + (f + s);
    int test_int_2 = (2 * i * s) * f;

    float test_float_1 = i + s;
    float test_float_2 = (2 * i * s);

    return 0;
}
