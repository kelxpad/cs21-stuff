# let a0 = base, a1 = exponent, a2 = result
# t0 = sign flag, t1 = exponent counter, t2,t3,t4 = mult temps

.data
    invalid: .asciz "ERROR: INVALID EXPONENT!"
    
.text
inputs:
    li a0, 2
    li a1, -3
    
    # ban negative exponents
    slt t5, a1, zero
    bne t5, zero, invalid_exp
    j determine_sign

invalid_exp:
    la a0, invalid
    li a7, 4
    ecall
    li a7, 10
    ecall
    
determine_sign:
    li t0, 0
    
    slt t1, a0, zero # base < 0 ? 1 : 0
    beq t1, zero, sign_done # positive base always positive
    
    andi t2, a1, 1 # is exponent odd?
    beq t2, zero, sign_done
    
    li t0, 1 # negative flag
    
sign_done:
    slt t1, a0, zero
    beq t1, zero, init_power
    sub a0, zero, a0
    
init_power:
    li a2, 1 # result = 1 identity
    mv t1, a1 # counter = exponent
    
power_loop:
    beq t1, zero, power_done
    
    # prepare multiplication
    mv t2, a2 # multiplicand
    mv t3, a0 # multiplier
    li a2, 0 # new result
    
mul_loop:
    beq t3, zero, mul_done
    
    andi t4, t3, 1
    beq t4, zero, skip_add
    
    add a2, a2, t2 # add multiplicand if it contributes
    
    
skip_add:
    slli t2, t2, 1  #  multiplicand <<= 1
    srli t3, t3, 1  #  multiplier >>= 1
    j mul_loop

mul_done:
    addi t1, t1, -1
    j power_loop
    
power_done:
    beq t0, zero, finish
    sub a2, zero, a2

finish:
    mv a0, a2
    li a7, 1
    ecall
    
    li a7, 10
    ecall