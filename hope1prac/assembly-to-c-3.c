/*
mystery2:
    addi sp, sp, -20
    sw ra, 16(sp)
    sw a0, 12(sp)

    li t0, 1
    ble a0, t0, base

    addi a0, a0, -1
    jal ra, mystery2
    sw a0, 8(sp)

    lw a0, 12(sp)
    addi a0, a0, -2
    jal ra, mystery2

    lw t1, 8(sp)
    add a0, a0, t1
    j end

base:
    mv a0, a0

end:
    lw ra, 16(sp)
    addi sp, sp, 20
    ret
*/

int mystery2(int n) {
    if (n <= 1) {
        return n;
    }

    return mystery2(n - 1) + mystery2(n - 2);
}