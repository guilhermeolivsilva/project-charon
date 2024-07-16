int add(int a, int b) {
    return a + b;
}

int main() {
    return add(3, 4);
}


/*
store %add.a 3
store %add.b 4
store %add.ret_addr @6
jump add
...


add:
    load %add.a r0
    load %add.b r1
    add r0 r1 r0
    store %add.ret_val r0
    jump %add.ret_addr
*/
