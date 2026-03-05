# observation: uppercase + 32 = lowercase

main:
    li a7, 63 # get user input
    li a0, 0
    la a1, input
    li a2, 20
    ecall
    
    la a0, input
    call capitalize_letters
    
    li a7, 4
    la a0, input
    ecall

capitalize_letters:
    # PUSH ra, s0
    addi sp, sp, -8
    sw ra, 4(sp)
    sw s0, 0(sp)
    
    mv s0, a0 # preserve pointer
    
    lb t0, 0(a0) # load current char
    beq t0, zero, capitalize_letters_ret # base case: '\0'
    
    # check if 'a' <= <= 'z'
    li t1, 97
    li t2, 122
    
    blt t0, t1, skip_convert
    bgt t0, t2, skip_convert
    
    addi t0, t0, -32 # convert to uppercase
    sb t0, 0(a0)
    
skip_convert:
    addi a0, a0, 1
    call capitalize_letters
    
capitalize_letters_ret:
    lw s0, 0(sp)
    lw ra, 4(sp)
    addi sp, sp, 8
    ret

.data
input: .zero 21