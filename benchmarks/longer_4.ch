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
        if (i % 2 == 0) {
            x = i + avg + scaled;
        }
        i = i + 1;
    }

    return 0;
}
