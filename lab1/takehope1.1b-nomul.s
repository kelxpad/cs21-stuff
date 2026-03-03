li s0, -6
li s1, 6
li s2, 9

# (a * b) + c
# s0 = a, s1 = b, s2 = c
# temp regs: t0, t1

main:
    mv t0, s0 # t0 = a
    mv t1 s1 # t1 = b
    li a0, 0 # a0 = result
    
    # handle sign
    li t2, 0 # sign flag
    blt t0, zero, neg_a
    j check_b 

neg_a:
    sub t0, zero, t0
    li t2, 1
check_b:
    blt t1, zero, neg_b
    j mult_loop
neg_b:
    sub t1, zero, t1
    xori t2, t2, 1 # neate flag if both are negative
    
mult_loop:
    beq t1, zero, mult_done
    add a0, a0, t0
    addi t1, t1, -1
    j mult_loop
    
mult_done:
    # apply sign
    beq t2, zero, add_c # skip negation if ok naman sign
    sub a0, zero, a0

add_c:
    add a0, a0, s2 # +c
    
    li a7, 1
    ecall
    li a7, 10
    ecall