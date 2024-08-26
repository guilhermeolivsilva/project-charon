#include "stdio.h"

int int_sum(int a, int b) {
    return a + b;
}

// Integer plus other types
void int_others() {
    int i;
    short s;
    float f;

    i + s;
    s + i;
    i + f;
    f + i;
}

float float_sum(float a, float b) {
    return a + b;
}

// Float plus other types
void float_others() {
    int i;
    short s;
    float f;

    f + s;
    s + f;
    f + i;
    i + f;
}

short short_sum(short a, short b) {
    return a + b;
}

// Float plus other types
void short_others() {
    int i;
    short s;
    float f;

    s + f;
    f + s;
    s + i;
    i + s;
}

int main() {
    int ii = int_sum(23, 13);
    float ff = float_sum(3.14, 2.71);
    short cc = short_sum(1, 2);

    printf("%d", (int)(ii + ff + cc));

    return 0;
}
