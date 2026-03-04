# let n = s0
# size = s1
# height = s2
# ch = s3
# level = s4
# r = s5

main:
    li s0, 5
    li s1, 3
 
    andi s1, s1, 7 # (size & 7)
    addi s1, s1, 1 # + 1;
    slli s2, s1, 1 # int height = size << 1;
    li s3, 0 # char ch = '\0';
    andi s4, s0, 15
    
    mv s5, s2 # int r = height;
 
    # num = t0, left = t1, right = t2
    
while_r:
    blt s5, zero, end_while_r # while (r >= 0) 
    mv t0, s5 # num = r

    #  int left , (r > size) ? r - size : size - r;
    ble s5, s1, left_else
    sub t1, s5, s1
    j left_done
left_else:
    sub t1, s1, s5
left_done:

    
# int right = (r > size) ? size + height - r : r - size + height;
    ble s5, s1, right_else
    add t2, s1, s2
    sub t2, t2, s5
    j right_done
right_else:
    sub t2, s5, s1 # r - size
    add t2, t2, s2 # + height
right_done:
    
    
# let c = t3, ch = s3
init_for_loop:
    li t3, 0
    
for_loop:
    blt s2, t3, for_end # exit if c > height
 
    li s3, 32 # ch = ' ';
    
    # if (c == left)
    bne t3, t1, c_unequal_to_left # skip checks

    # if (r == height)
    beq s5, s2, r_equals_height

    # else if (r == size)
    beq s5, s1, r_equals_size_and_left_equals_c

    # else if (r == 0)
    beqz s5, r_equals_zero
    
    # else if  (r > size)
    blt s1, s5, r_lt_size_and_left_equals_c
    # else
    li s3, 92 # ch = '\\'
    j end_cond
    
r_equals_height:
    li s3, 0x41 # ch = 'A';
    j end_cond

r_equals_size_and_left_equals_c:
    li s3, 0x3C # ch = '<';
    j end_cond
 
r_equals_zero:
    li s3, 0x56 # ch = 'V';
    j end_cond
    
r_lt_size_and_left_equals_c:
    li s3, 0x2F # ch = '/';
    j end_cond

c_unequal_to_left:
    # else if (c == right)
    # else if (c > left && c < right)
    # else if c > right { break; }
    blt t2, t3, for_end
    
end_cond:
    # printf("%c", ch);
    mv a0, s3
    li a7, 11
    ecall
    
    # i++
    addi t3, t3, 1 
    j for_loop
    
for_end:
    
end_while_r:
    nop