/*
mystery:
    addi sp, sp, -16
    sw ra, 12(sp)
    sw a0, 8(sp)

    li t0, 1
    ble a0, t0, base

    addi a0, a0, -1
    jal ra, mystery

    lw t1, 8(sp)
    mul a0, a0, t1
    j end

base:
    li a0, 1

end:
    lw ra, 12(sp)
    addi sp, sp, 16
    ret
*/

int mystery(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * mystery(n - 1);
}