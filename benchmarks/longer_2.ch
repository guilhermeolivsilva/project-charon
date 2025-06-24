int main() {
    int i;
    int x;
    int avg;
    int scaled;
    int factor;

    factor = 1;

    avg = (72 + 85 + 90 + 60 + 88) / factor;

    i = 0;
    while (i < 5) {
        x = i + avg;
        i = i + 1;
    }

    return 0;
}
