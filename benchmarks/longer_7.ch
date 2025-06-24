int func_1(int x, int y) {
    return x / y;
}

int func_2(int x, int y) {
    return func_1(x, y) / func_1(x, y);
}

int main() {
    int i;
    int x;
    int avg;
    int scaled;
    int factor;

    factor = 1;

    avg = (72 + 85 + 90 + 60 + 88) / 5;
    scaled = avg / factor;

    i = 0;
    while (i < 5) {
        x = func_2(i, avg);
        i = i + 1;
    }

    return 0;
}
