main:
    addi sp, sp, -4
    sw ra, 0(sp)
    
    li a7, 4
    la a0, str2
    ecall #printf("%c", str2);
    
    la a0, str1
    call length
    
    # print returned value
    # mv a0, edited value
    li a7, 1
    ecall
    
    # print newline
    li a7, 11
    li a0, 10
    ecall
    
    lw ra, 0(sp)
    addi sp, sp, 4
    
    li a7, 10
    ecall
    
length:
    addi sp, sp, -4      # allocate stack frame
    sw ra, 0(sp)         # save return address

    lb t0, 0(a0)         # load *s
    beq t0, zero, base_case

    addi a0, a0, 1       # s + 1
    call length          # recursive call

    addi a0, a0, 1       # 1 + length(s+1)
    j length_ret

base_case:
    li a0, 0             # return 0

length_ret:
    lw ra, 0(sp)         # restore ra
    addi sp, sp, 4       # pop stack
    ret
    
.data
str1: .asciz "Hello, world!!!"
str2: .asciz "Length of the string: "