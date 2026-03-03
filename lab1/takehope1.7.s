li a0, 10
li a1, 5

# k = a1, n = a0
main:
    li t0, 0 # count = 0
    li t1, 0 # i = 0
    j loop

loop:
    beq t1, a0, end
    blt t1, a1, incr_t0
    
skip_incr:
    addi t1, t1, 1
    j loop
    
incr_t0:
    addi t0, t0, 1
    j skip_incr
    
    
end:
    mv a0, t0
    li a7, 1
    ecall
    li a7, 10
    ecall