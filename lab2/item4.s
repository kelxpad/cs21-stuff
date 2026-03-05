# asterisk ascii = 42
main:
    li a0, 1 # rows
    li a1, 2 # cols
    call layered_stars
    
    li a7, 10
    ecall
    
form_line:
    addi sp, sp, -12
    sw ra, 8(sp)
    sw a0, 4(sp)
    sw a1, 0(sp)
    beq a1, zero, form_line_bc
    
    li a7, 11 # printf("*");
    li a0, 42
    ecall
    
    addi a1, a1, -1
    call form_line
    j form_line_ret
    
form_line_bc:
    li a0, 10
    li a7, 11
    ecall

form_line_ret:
    # POP ra, a0, a1
    lw a1, 0(sp)
    lw a0, 4(sp)
    lw ra, 8(sp)
    addi sp, sp, 12
    ret
    
layered_stars:
    # PUSH ra, a0, a1
    addi sp, sp, -12
    sw ra, 8(sp)
    sw a0, 4(sp)
    sw a1, 0(sp)
    
    beq a0, zero, layered_stars_ret
    
    call form_line
    addi a0, a0, -1
    addi a1, a1, -1
    call layered_stars
    
layered_stars_ret:
    lw a1, 0(sp)
    lw a0, 4(sp)
    lw ra, 8(sp)
    addi sp, sp, 12
    ret