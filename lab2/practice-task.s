g: # no stack frame needed because ra and sx registers untouched
    addi a0, a0, 2
    ret
    
f:
    addi sp, sp, -4 # allocate stack
    sw ra, 0(sp)
    
    call g
    
    addi a0, a0, 1 # g(n) + 1
    
    lw ra, 0(sp)
    addi sp, sp, 4 # dealloc stack
    
main:
    addi sp, sp, -4
    sw ra, 0(sp)
    
    li a0, 10
    call f # result in a0
    
    lw ra, 0(sp)
    addi sp, sp, 4
    ret