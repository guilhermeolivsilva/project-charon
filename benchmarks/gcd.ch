int main() {
    int i;
    i = 125;

    int j;
    j = 100;

    while (i - j) {
        if (i < j) {
            j = j - i;
        }
        else {
            i = i - j;
        }
    }

    return 0;
}
