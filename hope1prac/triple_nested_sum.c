#include <stdio.h>

void triple_nested_sum(int x, int y, int z) {
    int sum = 0;

    for (int i = 0; i < x; i++) {
        for (int j = 0; j < y; j++) {
            for (int k = 0; k < z; k++) {
                sum += i + j + k;
            }
        }
    }

    printf("%d\n", sum);
}

int main() {
    triple_nested_sum(2, 3, 4);
    return 0;
}