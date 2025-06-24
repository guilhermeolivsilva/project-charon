int classify(int score) {
    int result;
    if (score > 90 || score == 90) {
        result = 5;
    } else if (score > 75 || score == 75) {
        result = 4;
    } else if (score > 60 || score == 60) {
        result = 3;
    } else if (score > 40 || score == 40) {
        result = 2;
    } else {
        result = 1;
    }

    return result;
}

int print_result(int id, int grade) {
    return 0;
}

int average(int x_1, int x_2, int x_3, int x_4, int x_5) {
    return (x_1 + x_2 + x_3 + x_4 + x_5) / 5;
}

int main() {
    int i;
    int x;
    int avg;
    int scaled;
    int class_label;

    avg = average(72, 85, 90, 60, 88);
    class_label = classify(avg);

    i = 0;
    while (i < 5) {
        x = print_result(i, class_label);
        i = i + 1;
    }

    return 0;
}
