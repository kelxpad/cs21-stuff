# triple nested loop

main:
    li a0, 2
    li a1, 3
    li a2, 4
    call triple_nested_sum
    
    li a7, 10
    ecall
    
triple_nested_sum:
    li t0, 0 # sum = 0
    li t1, 0 # i = 0
    
i_loop:
    bge t1, a0, end
    li t2, 0 # j = 0
    
j_loop:
    bge t2, a1, j_loop_end
    
    li t3, 0 # k = 0
    
k_loop:
    bge t3, a2, k_loop_end

    # sum += i + j + k
    add t4, t1, t2
    add t4, t4, t3
    add t0, t0, t4

    addi t3, t3, 1 # k++
    j k_loop
    
k_loop_end:
    addi t2, t2, 1 # j++
    j j_loop
    
j_loop_end:
    addi t1, t1, 1 # i++
    j i_loop
    


end:
    mv a0, t0
    li a7, 1
    ecall
    ret