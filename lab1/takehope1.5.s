# t0 = x, t1 = y, t2 = z, t3 = r
main:
    # check x < y
    blt t0, t1, r0_case # if x < y, r = 0
    # check z == 0
    beq t2, zero, r0_case
    # both conditions passed
    li t3, 1
    j end
    
r0_case:
    li t3, 0

end:
    mv a0, t3
    li a7, 1
    ecall
    li a7, 10
    ecall