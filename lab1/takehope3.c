#include <stdio.h>

int main() {
    int a1 = 123456;
    int a2 = 765432;
    int a3 = 6;

    int s11 = 10;

    int s0 = 0;
    int s1 = a1;

    int t0 = 0;
    // L1
    for (int t0 = 0; t0 < a3; t0++) {
        int s2 = s1 % s11;
        int s3 = a2;
        // L2
        for (int t1 = 0; t1 < a3; t1++) {
            int s4 = s3 % s11;
            // L3
            if (s2 == s4) {
                s0++;
            }
            s3 /= s11;
        }
        s1 /= s11;
    }
    // L1_end
    printf("%d", s0);
    return 0;
}

/*
Assembly to C Strategy:
1. Find all labels
2. Circle every branch
3. Mark which branches jump upward, they're most likely loops
4. Once the control flow is laid out, translate the arithmetic
*/