struct my_type {
    int attr_1;
    int* attr_2;
    float attr_3;
    int attr_4;
    long attr_5;
};


int main() {
    my_type test;

    test.attr_1 = 1;
    test.attr_2 = new int[4];
    test.attr_3 = 1.0;
    test.attr_4 = 4;
    test.attr_5 = 321;
}
