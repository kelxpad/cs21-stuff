#include <stdio.h>

int arr[] = {10, 20, 30, 40, 50, 60};
// a2 running sum
// a1 is the arr length
// a0 = pointer to curr element
int f(int *a0, int a1, int a2){
    if (0 >= a1) {
        return a2; // mv a0, a2 (return value goes in a0)
    }

    // mv s0, a0
    int *s0 = a0;

    // lw s1, 0(s0)
    int s1 = *s0;

    // add a2, a2, s1
    a2 = a2 + s1;

    // addi a0, a0, 4
    a0 = a0 + 1; // +1 int = +4 bytes

    // addi a1, a1, -1
    a1 = a1 - 1;

    // call f
    return f(a0, a1, a2);


}
int main(int a1, int a2) {
    int a0 = (int*)arr; // la a0, arr
    int a1 = 6;         // li a1, 6
    int a2 = 0;         // li a2, 0

    res = f(a0, a1, a2);
    printf("%d\n", res);

    return 0;
}

/*5d
so in short,
1. 5b is recursive, 5c is not
2. 5b: 15n + c, 5c: 6n + c
3. both straight diagonal lines
4. both are O(n), but recursive is slower because of the overhead for stack management
*/