# let s0 = a, 
# s1 = b, 
# s2 = c, 
# s3 = d
# at most two temp regs allowed

# not part of the original instructions, but we will store the result in a0 so we can print it
# (a + b) - (c + d)
main:
    add t1, s0, s1
    add t2, s2, s3
    sub a0, t2, t1
    
    li a7, 1
    ecall
    li a7, 10
    ecall