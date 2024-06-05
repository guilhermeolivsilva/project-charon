#include "stdio.h"

int int_sum(int a, int b) {
    return a + b;
}

float float_sum(float a, float b) {
    return a + b;
}

char char_sum(char a, char b) {
    return a + b;
}

long long_sum(long a, long b) {
    return a + b;
}

int main() {
    int ii = int_sum(23, 13);
    float ff = float_sum(3.14, 2.71);
    char cc = char_sum(1, 2);
    long ll = long_sum(123, 321);

    printf("%d", (int)(ii + ff + cc + ll));

    return 0;
}