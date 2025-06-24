int main() {
    int i;
    i = 1;

    int a;
    a = 0;

    int b;
    b = 1;

    int c;

    while (i < 10) {
        c = a;
        a = b;
        b = c + a;
        i = i + 1; 
    }

    return 0;
}
