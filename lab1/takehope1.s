li s0, -1
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
# (a * b) + c
main:
    mul a0, s0, s1
    add a0, a0, s2
    
    li a7, 1
    ecall
    li a7, 10
    ecall