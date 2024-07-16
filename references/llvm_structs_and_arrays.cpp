int some_integer;
int some_array[5];

struct my_type {
    int attr_1;
    int* attr_2;
    float attr_3;
    int attr_4;
    long attr_5;
};

struct my_type_clone {
    int attr_1;
    int* attr_2;
    float attr_3;
    int attr_4;
    long attr_5;
};

struct another_type {
    int attr_1;
    int attr_2;
    int attr_3;
};

my_type test() {
    my_type test;

    return test;
}


my_type_clone test_clone() {
    my_type_clone test;

    return test;
}


int main() {
    my_type test;
    another_type test_2[5];

    test.attr_1 = 1;
    test.attr_2 = new int[4];
    test.attr_3 = 1.0;
    test.attr_4 = 4;
    test.attr_5 = 321;

    test_2[0].attr_1 = 1;
}
