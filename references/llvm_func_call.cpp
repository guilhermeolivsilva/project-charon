int test(int param) {
    return 1 + 2 + param;
}


int main() {
    int func_call, some_other_int;

    func_call = test(123);
    func_call = test(some_other_int);

    return 0;
}
