main:
    addi sp,sp, -4
    sw ra, 0(sp)
    
    li a7, 4
    la a0, str2
    ecall # print("There are")
    
    la a0, str # pointer to string
    lb a1, ch
    
    call count_char
    
    li a7, 1
    ecall
    
    la a0, str3
    li a7, 4
    ecall
    
    la a0, ch
    ecall
    
    la a0, str4
    ecall
    
    la a0, str
    ecall
    
    li a7, 10
    ecall

count_char:
    addi sp, sp, -8
    sw ra, 4(sp)
    sw s0, 0(sp)
    
    mv s0, a1 # preserve ch
    
    lb t0, 0(a0) # t0
    beq t0, zero, count_char_bc
    beq t0, s0, count_char_match

count_char_no_match:
    addi a0, a0, 1
    mv a1, s0
    call count_char
    j count_char_ret

count_char_bc:
    li a0, 0
    j count_char_ret
    
count_char_match:
    addi a0, a0, 1
    mv a1, s0
    call count_char
    addi a0, a0, 1
    j count_char_ret
    
base_case:
    li a0, 0
    
    
count_char_ret:
    lw s0, 0(sp)
    lw ra, 4(sp)
    addi sp, sp, 8
    ret

.data:
    str: .asciz "banana"
    str2: .asciz "There are "
    str3: .asciz " instances of "
    str4: .asciz " in "
    ch: .byte 97