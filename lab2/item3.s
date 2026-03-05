main:
    li a0, 22 # a0 = n
    la t0, hailstone
    li t1, 0 # i = 0

collatz:
    # store current n into array
    sw a0, 0(t0)
    addi t0, t0, 4 # move pointer
    addi t1, t1, 1 # incr length
    
    li t2, 1
    beq a0, t2, collatz_end
    
    andi t3, a0, 1
    beq t3, zero, collatz_even
    j collatz_odd

collatz_even:
    srli a0, a0, 1 # n // 2
    j collatz

collatz_odd:
    li t3, 3
    mul a0, a0, t3
    addi a0, a0, 1
    j collatz
    
collatz_end:
    # setup pointers
    la t2, hailstone
    addi t3, t1, -1 # k = length - 1
    slli t3, t3, 2 # int size = 4 so k*4
    la t4, hailstone
    add t4, t4, t3 # right pointer
    
    li a0, 0 # x = 0
    
    # compute number of pairs = length/2
    li t5, 2
    div t6, t1, t5 # t6 = # of pairs
    
sum_loop:
    beq t6, zero, sum_done
    
    lw a1, 0(t2) # h_i
    lw a2, 0(t4) # h_k-i
    
    sub s2, a1, a2
    add a0, a0, s2
    
    # move pointers, decrement # of pairs
    addi t2, t2, 4
    addi t4, t4, -4
    addi t6, t6, -1
    j sum_loop

sum_done:
    li a7, 1
    ecall
    
    li a7, 10
    ecall
    
    
.data
hailstone: .zero 400 # space for 100 ints