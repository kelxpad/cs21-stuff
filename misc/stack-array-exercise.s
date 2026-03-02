main: 
    addi sp, sp, -20
    li t0, 3
    sw t0, 0(sp)
    li t0, 6
    sw t0, 4(sp)
    li t0, 9
    sw t0, 8(sp)
    li t0, 12
    sw t0, 12(sp)
    li t0, 15
    sw t0, 16(sp)  
    li t1, 4 # i = 4
    li t2, 0
    
loop:
    blt t1, zero, done
    
    slli t3, t1, 2 # calculate offset
    add t5, sp, t3
    lw t5, 0(t5)
    
    add t2, t2, t5
    
    addi t1, t1, -1 # i -= 1
    j loop
    
done:
    addi sp, sp, 20
    add a0, zero, t2
    li a7, 1
    ecall
    
    li a7, 10
    ecall