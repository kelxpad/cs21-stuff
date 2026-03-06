# a0 = x, a1 = y, a2 = result, t0 = sign flag, t1, t2 = sign checks, 
# t3 = temp bit checker


#inputs
li a0, -13
li a1, -6

determine_sign:
    li t0, 0 # sign flag
    
    slt t1, a0, zero # t1 (a0 < 0) ? 1 : 0
    slt t2, a1, zero # t2 (a1 < 0) ? 1 : 0
    xor t0, t1, t2 # if 1 then neg, if 0 then pos
    
    # convert both operands to positive
    beq t1, zero, check_a1
    sub a0, zero, a0
    
check_a1:
    beq t2, zero, start_mul
    sub a1, zero, a1
    
start_mul:
    li a2, 0

mul_loop:
    beq a1, zero, mul_done
    
    andi t3, a1, 1 # check lowest bit
    beq t3, zero, skip_add
    
    
    add a2, a2, a0 # res += multiplicand
    
skip_add:
    slli a0, a0, 1 # multiplicand <<= 1
    srli a1, a1, 1 # multiplier >>= 1
    j mul_loop

mul_done:
    beq t0, zero, finish
    sub a2, zero, a2
    
finish:
    mv a0, a2
    li a7, 1
    ecall