int main() {
    int my_array[5];

    int i;
    i = 0;

    while(i < 5) {
        my_array[i] = i << i;
        i = i + 1;
    }

    int j;
    j = (my_array[2]) + 3;

    return 0;
}
