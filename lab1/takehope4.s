# a0 = n, a1 = k
li a0, 10
li a1, 3
li a2, 0 # butt count
li a3, 0 # output

pearl_smoke_count:
    beq a0, zero, pearl_end
    addi a0, a0, -1
    addi a2, a2, 1
    addi a3, a3, 1
    bge a2, a1, create_new_cig
    j pearl_smoke_count

create_new_cig:
    addi a0, a0, 1
    sub a2, a2, a1
    j pearl_smoke_count


pearl_end:
    mv a0, a3
    li a7, 1
    ecall
    li a7, 10
    ecall
