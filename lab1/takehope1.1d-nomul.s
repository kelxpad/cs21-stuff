li s0, 6
li s1, 2
li s2, 0
li s3, 4

# TESTING ZONE ABOVE, IGNORE THE LINES ABOVE

# let s0 = a, 
# s1 = b, 
# s2 = c, 
# s3 = d
# at most two temp regs allowed

# not part of the original instructions, but we will store the result in a0 so we can print it
# nomul version
# (a + b)^2
main:
    add t0, s0, s1 # t0 = a + b
    li a0, 0 # res
    mv t1, t0 # loop counter = t0
    
exp_loop:
    beq t1, zero, done_exp
    add a0, a0, t0
    addi t1, t1, -1
    j exp_loop
    
done_exp:
    li a7, 1
    ecall
    li a7, 10
    ecall

