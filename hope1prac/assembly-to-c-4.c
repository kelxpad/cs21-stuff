/*
mystery3:
    addi sp, sp, -24
    sw ra, 20(sp)
    sw a0, 16(sp)

    li t0, 1
    ble a0, t0, base

    addi a0, a0, -1
    jal ra, mystery3
    sw a0, 12(sp)

    lw a0, 16(sp)
    addi a0, a0, -2
    jal ra, mystery3
    sw a0, 8(sp)

    lw t1, 12(sp)
    lw t2, 8(sp)
    mul t1, t1, t2

    lw t3, 16(sp)
    add a0, t1, t3
    j end

base:
    li a0, 1

end:
    lw ra, 20(sp)
    addi sp, sp, 24
    ret
*/

int mystery3(int n) {
    // base
    if (n <= 1) {
        return 1;
    }

    int r1 = mystery3(n - 1);
    int r2 = mystery3(n - 2);

    return n + mystery3(n - 1) * mystery3(n - 2);
}