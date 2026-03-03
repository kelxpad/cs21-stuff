main:
    # t0 = t0
    # t1 = t1
    # t2 = t2
    # a0 = n
    # t4 = ans
    addi a0, x0, -21 # Only this line should be manually changed for testing
    addi t4, x0, 0 # int ans;
    addi s0, x0, 3 # i = 3
    
# if (n < 0)
    bltz a0, L_if_neg  

# else if (n == 0)
    beqz a0, L_if_zero      # branch if equal to zero (a0 == x0)

# else if (n == 1 || n == 2)
    li t5, 1
    beq a0, t5, L_if_1or2
    li t6, 2
    beq a0, t6, L_if_1or2

# else
    j L_else                # jump to final else block

L_if_neg:
    xor t4, t4, t4 # zero out
    addi t4, x0, -1 # ans = -1
    j L_end

L_if_zero:
    xor a0, a0, a0 # zero out
    addi a0, x0, 0 # n = 0
    j L_end

L_if_1or2:
    xor t4, t4, t4 # zero out
    addi t4, x0, 1 # n = 1
    j L_end

L_else:
    addi t0, x0, 0
    addi t1, x0, 1
    addi t2, x0, 1
    
    j L_loop

L_loop:
    bgt s0, a0, L_end # while i <= n 
    
    # ans = t0 + t1 + t2;
    add t4, t0, t1
    add t4, t4, t2
    
    # t0 = t1; t1 = t2; t2 = ans;
    mv t0, t1
    mv t1, t2
    mv t2, t4
    
    addi s0, s0, 1 # increment loop
    
    j L_loop

L_end:
    mv a0, t4
    li a7, 1
    ecall
    li a7, 10
    ecall
 