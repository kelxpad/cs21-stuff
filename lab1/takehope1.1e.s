li s0, 6
li s1, 2
li s2, 9
li s3, 4

# TESTING ZONE ABOVE, IGNORE THE LINES ABOVE

# let s0 = a, 
# s1 = b, 
# s2 = c, 
# s3 = d
# at most two temp regs allowed

# not part of the original instructions, but we will store the result in a0 so we can print it
# (a + b)^2 - (c + d)^2
main:
    add t0, s0, s1
    mul t0, t0, t0
    add t1, s2, s3
    mul t1, t1, t1
    sub a0, t0, t1
    
    li a7, 1
    ecall
    li a7, 10
    ecall

