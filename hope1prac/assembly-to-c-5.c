/*
mystery4:
    addi sp, sp, -28
    sw ra, 24(sp)
    sw a0, 20(sp)
    li t0, 0
    sw t0, 16(sp)

    li t1, 1
    ble a0, t1, base

loop:
    lw t0, 16(sp)
    lw t2, 20(sp)
    bge t0, t2, done

    lw a0, 20(sp)
    sub a0, a0, t0
    addi a0, a0, -1
    jal ra, mystery4

    lw t3, 16(sp)
    add t3, t3, a0
    sw t3, 16(sp)

    lw t0, 16(sp)
    addi t0, t0, 1
    sw t0, 16(sp)

    j loop

done:
    lw a0, 16(sp)
    j end

base:
    li a0, 1

end:
    lw ra, 24(sp)
    addi sp, sp, 28
    ret
*/

int mystery4(int a0) {
    int t0 = 0; // 16(sp)
    // t2 holds original n, 20(sp)
    int t2 = a0;

    if (a0 <= 1) {   // base
        return 1;
    }

    while (t0 < t2) {
        a0 = t2 - t0 - 1;   // compute recursive argument
        a0 = mystery4(a0); // jal ra, mystery4: recursive call

        int t3 = t0 + a0; // accumulate result
        t0 = t3; // store back in t0

        t0 = t0 + 1;
    }

    return t0; // final result stored in t0
}

// note: label stack slots as what they re doing, then write a register-based C