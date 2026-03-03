li t0, 67
# let t0 = x, t1 = y, create a risc-v program that evaluates
main:
    blt t0, zero, cas1
    beq t0, zero, cas2
    j cas3

cas1:
    li t1, -1
    j end

cas2:
    li t1, 0
    j end
    
cas3: 
    li t1, 1
    j end
    
end:
    mv a0, t1
    li a7, 1
    ecall