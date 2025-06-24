struct my_struct {
    int attribute_1;
    float attribute_2;
    short attribute_3;
};

int main() {
    my_struct struct_var;

    struct_var.attribute_1 = 10;
    struct_var.attribute_2 = 13.1 * 23.4 / 30.2;
    struct_var.attribute_3 = (struct_var.attribute_1) * (struct_var.attribute_2);

    return 0;
}
