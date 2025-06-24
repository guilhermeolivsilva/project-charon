int average(int a, int b, int c, int d, int e) {
    int sum;
    sum = a + b + c + d + e;
    return sum / 5;
}

int scale(int value, int factor) {
    return value * factor;
}

int print_result(int id, int grade) {
    return 0;
}

int main() {
    int i;
    int x;
    int avg;
    int scaled;
    int class_label;
    int factor;

    factor = 1;

    avg = average(72, 85, 90, 60, 88);
    scaled = scale(avg, factor);

    i = 0;
    while (i < 5) {
        x = print_result(i, avg);
        i = i + 1;
    }

    return 0;
}
