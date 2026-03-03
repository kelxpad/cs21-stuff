# t0 = x, t1 = y, t2 = z, and t3 = r
li t0, 0
li t1, 1
li t2, 2
li t3, 3

main:
    beq t0, zero, r_zero
    bge t1, t2, r_zero
    li t3, 1
    j end

r_zero:
    li t3, 0

end:
    li a7, 1
    ecall
    li a7, 10
    ecall
    