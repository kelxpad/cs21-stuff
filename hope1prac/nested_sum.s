# nested loop practice

main:
    li a0, 3 # a0 = n
    li a1, 4 # a1 = m
    call nested_sum
    
    li a7, 10
    ecall
    
nested_sum:
    li t0, 0 # t0 = sum
    li t1, 0 # i = 0
    
o_loop:
    bge t1, a0, end
    li t2, 0 # reset j pointer
    
i_loop:
    bge t2, a1, i_loop_end
    add t3, t1, t2
    add t0, t0, t3
    addi t2, t2, 1
    j i_loop

i_loop_end:
    addi t1,t1, 1
    j o_loop
    
end:
    mv a0, t0
    li a7, 1
    ecall
    ret
    
    