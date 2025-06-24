int print_result(int a, int b, int c) {
    return 0;
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
        x = print_result(i, avg, scaled);
        i = i + 1;
    }

    return 0;
}
