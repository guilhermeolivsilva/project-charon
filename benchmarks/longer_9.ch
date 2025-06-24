int average(int x_1, int x_2, int x_3, int x_4, int x_5) {
    int total;
    total = 0;

    total = total + x_1;
    total = total + x_2;
    total = total + x_3;
    total = total + x_4;
    total = total + x_5;

    return total / 5;
}

int main() {
    int i;
    int x;
    int avg;
    int scaled;
    int factor;

    factor = 1;

    avg = average(72, 85, 90, 60, 88);
    scaled = avg / factor;

    i = 0;
    while (i < 5) {
        x = i + avg + scaled;
        i = i + 1;
    }

    return 0;
}
