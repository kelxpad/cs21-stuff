# n = a0, return value in a0

factorial:
    addi sp, sp, -8
    sw a0, 4(sp)
    sw ra, 0(sp)
    
    blt a0, zero, factorial_neg
    li t0, 1
    # elif (n <= 1)
    bge t0, a0, factorial_one
    # else { return n * factorial(n - 1)}
    addi a0, a0, -1
    call factorial
    
    lw t1, 0(sp) # reload original n in this stack
    mul a0, a0, t1 # n * factorial(n - 1)
    j factorial_ret
    
factorial_one:
    li a0, 1
    j factorial_ret
    
factorial_neg:
    li a0, -21
    j factorial_ret
    
factorial_ret:
    lw ra, 4(sp)
    addi sp, sp, 8
    ret
    