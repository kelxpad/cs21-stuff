#sluts

#inputs
li a0, 6766
li a1, -6767

find_smaller:
    slt t0, a0, a1 # 1 if a0 is smaller
    beq t0, zero, store_a1
    mv a2, a0 # store a0
    j print
    
store_a1:
    mv a2, a1
    
print:
    mv a0, a2
    li a7, 1
    ecall
    
    li a7, 10
    ecall