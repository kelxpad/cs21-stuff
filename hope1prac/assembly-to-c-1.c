// a0 = pointer to int array
// a1 = length of array

int sum_positive(int *a0, int a1) {
    int t1 = 0; // sum = 0
    for (i = 0; i < a1; i++) {
        int t4 = a0[i];
        if (t4 < 0) {
            continue;
        }
        t1 += t4;
    }
    return t1;
}

/*
# a0 = pointer to int array
# a1 = length of array

sum_positive:
    li t0, 0          # i = 0
    li t1, 0          # sum = 0

loop:
    beq t0, a1, end   # if (i == len) break

    slli t2, t0, 2    # offset = i * 4
    add t3, a0, t2    # address of arr[i]
    lw t4, 0(t3)      # value = arr[i]

    blt t4, zero, skip
    add t1, t1, t4    # sum += value

skip:
    addi t0, t0, 1    # i++
    j loop

end:
    mv a0, t1         # return sum
    ret
*/