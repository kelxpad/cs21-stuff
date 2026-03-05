# blahblahblah
main:
    # get ASCII string from user, store it in a0
    li a7, 63 # read syscall
    li a0, 0  # stdin
    la a1, input
    li a2, 4000 # number of bytes read returned in a0
    ecall
    
    mv t0, a0 # save length in t0
    
    # check length if valid
    blt t0, zero, invalid_string
    li t1, 4000
    blt t1, t0, invalid_string
     
    la a0, input
    call uppercasify # normalize letters
    
    call is_palindrome # store result in a0
    
    beq a0, zero, do_lower
    j exit
    
do_lower:
    la a0, input
    call lowercasify
    j exit
    
invalid_string:
    la a0, invalid
    li a7, 4
    ecall
    j exit
    
is_palindrome:
    # PUSH ra, s0, s1
    addi sp, sp, -12
    sw ra, 8(sp)
    sw s0, 4(sp)
    sw s1, 0(sp)
    
    mv s0, a0 # left pointer

find_end: # find the end of the str
    lb t0, 0(a0)
    beq t0, zero, end_found # null term
    addi a0, a0, 1
    j find_end
    
end_found:
    addi a0, a0, -1 # move to last char
    mv s1, a0 # right pointer

pal_loop:
    
# skip non-letters on left
skip_left:
    bge s0, s1, palindrome_true
    lb t0, 0(s0)
    li t1, 65 # A
    li t2, 90 # Z
    blt t0, t1, inc_left
    blt t2, t0, inc_left
    j left_ok

inc_left:
    addi s0, s0, 1
    j skip_left

left_ok:
    
# skip non-letters on right
skip_right:
    bge s0, s1, palindrome_true
    lb t0, 0(s1)
    blt t0, t1, dec_right
    blt t2, t0, dec_right
    j right_ok

dec_right:
    addi s1, s1, -1
    j skip_right
    
right_ok:
    
    # if pointers crossed, its a palindrome
    bge s0, s1, palindrome_true
    
    # compare chars
    lb t3, 0(s0)
    lb t4, 0(s1)
    bne t3, t4, palindrome_false

    # move inward
    addi s0, s0, 1
    addi s1, s1, -1
    j pal_loop
    
palindrome_true:
    li a0, 1
    j pal_done

palindrome_false:
    li a0, 0
    j pal_done

pal_done:
    lw s1, 0(sp)
    lw s0, 4(sp)
    lw ra, 8(sp)
    addi sp, sp, 12
    ret
    
uppercasify:
    # PUSH ra, s0
    addi sp, sp, -8
    sw ra, 4(sp)
    sw s0, 0(sp)
    
    mv s0, a0 # preserve pointer
    
    lb t0, 0(a0) # load current char
    beq t0, zero, upper_done
    
    # check if 'a' <= char <= 'z'
    li t1, 97
    li t2, 122
    
    blt t0, t1, skip_convert_uppercasify
    blt t2, t0, skip_convert_uppercasify
    
    addi t0, t0, -32 # convert to uppercase
    sb t0, 0(a0)
    
skip_convert_uppercasify:
    addi a0, a0, 1
    call uppercasify

upper_done:
    lw s0, 0(sp)
    lw ra, 4(sp)
    addi sp, sp, 8
    ret
    
lowercasify:
    addi sp, sp, -8
    sw ra, 4(sp)
    sw s0, 0(sp)
    
    mv s0, a0
    
    lb t0, 0(a0)
    beq t0, zero, lower_done
    
    # check if 'A' <= char <= 'Z'
    li t1, 65
    li t2, 90
    
    blt t0, t1, skip_convert_lowercasify
    blt t2, t0, skip_convert_lowercasify

    addi t0, t0, 32 # convert to lowercase
    sb t0, 0(a0)
    
skip_convert_lowercasify:
    addi a0, a0, 1
    call lowercasify
    
lower_done:
    lw s0, 0(sp)
    lw ra, 4(sp)
    addi sp, sp, 8
    ret
    
exit:
    la a0, input
    li a7, 4 # print the string
    ecall
    
    li a0, 0 # END
    li a7, 10
    ecall

data:
    input: .zero 4001
    invalid: .asciz "ERROR: STRING LENGTH IS INVALID!"