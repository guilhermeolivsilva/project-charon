int main() {
    int i;
    int j;
    int k;

    int hits_1;
    hits_1 = 0;

    int hits_2;
    hits_2 = 0;

    int hits_3;
    hits_3 = 0;


    i = 0;
    j = 0;
    k = 0;
    while (i < 10) {
        while (j < 10) {
            while (k < 10) {
                if (i == k) {
                    hits_1 = hits_1 + 1;
                }
                hits_2 = hits_2 + i;

                k = k + 1;
            }
            if (i == j) {
                hits_3 = hits_3 + 1;
                hits_2 = hits_2 + 1;
            }

            k = 0;
            j = j + 1;
        }
        i = i + 1;
        j = 0;
    }

    return 0;
}
