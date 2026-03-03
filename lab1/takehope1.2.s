li a0, 1
li a1, 2

# Create a RISC-V program that swaps the values in registers a0 and a1 in place without using temporary registers or pseudoinstructions.

xor a0, a0, a1 # a0 = a0 ^ a1
xor a1, a0, a1 # a1 = (a0 ^ a1) ^ a1 = a0
xor a0, a0, a1 # a0 = (a0 ^ a1) ^ a0 = a1


# testing by print
li a7, 1
ecall

# print newline
li a0, 10
li a7, 11
ecall

li a7, 1
mv a0, a1
ecall
li a7,10