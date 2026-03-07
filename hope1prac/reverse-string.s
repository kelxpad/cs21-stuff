# a0 = s (char*), a1 = sSize

.data
s: .asciz "hello"

.text
main:
    la a0, s
    li a1, 5
    call reverseString
    
    la a0, s # not necessary since a0 wasnt overwritten
    li a7, 4
    ecall
    
    li a7, 10
    ecall
    
reverseString:
    addi sp, sp, -4
    sw ra, 0(sp)
    
    li t0, 0 # left = 0
    addi t1, a1, -1 # right = sSize - 1
    
loop:
    
    bge t0, t1, loop_end
    
    add a2, a0, t0 # &s[left]
    add a3, a0, t1 # &s[right]
    call swap
    
    addi t0, t0, 1
    addi t1, t1, -1
    j loop

loop_end:
    lw ra, 0(sp)
    addi sp, sp, 4
    ret

swap:
    lb t4, 0(a2)
    lb t5, 0(a3)
    
    sb t4, 0(a3)
    sb t5, 0(a2)
    ret