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

do_start:
    
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
    bne t3, t1, elif_c_eq_right # skip checks

    # if (r == height)
    beq s5, s2, r_equals_height

    # else if (r == size)
    beq s5, s1, r_equals_size_and_left_equals_c

    # else if (r == 0)
    beqz s5, r_equals_zero
    
    # else if  (r > size)
    blt s1, s5, r_gt_size_and_left_equals_c
    # else
    li s3, 0x5C # ch = '\\'
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
    
r_gt_size_and_left_equals_c:
    li s3, 0x2F # ch = '/';
    j end_cond

    # else if (c == right)
elif_c_eq_right:
    bne t3, t2, elif_c_gt_left_and_c_lt_right
    # if (r == size) and right eq c:
    beq s5, s1, r_equals_size_and_right_equals_c
    # else if (r > size)
    blt s1, s5, r_gt_size_and_right_eq_c
    # else 
    li s3, 0x2F
    j end_cond
    
r_equals_size_and_right_equals_c:
    li s3,0x3E
    j end_cond

r_gt_size_and_right_eq_c:
    li s3, 0x5C
    j end_cond

    # else if (c > left && c < right)
elif_c_gt_left_and_c_lt_right:
    # alternatively, if c <= left, or c >= right, branch to elif_c_gt_right
    bge t1, t3, elif_c_gt_right
    bge t3, t2, elif_c_gt_right
    # if level >= r + 1
    addi t4, s5, 1 # t4 = r + 1
    bge s4, t4, level_geq_rplusone
    j end_cond
    
level_geq_rplusone:
    blt zero, s4, ch_zero_plus_num
    j end_cond
    
ch_zero_plus_num:
    li t5, 48 # '0'
    add s3, t5, t0
    li t5, 57 # '9'
    blt t5, s3, ch_add_39
    j end_cond
    
ch_add_39:
    addi s3, s3, 39
    j end_cond
    
elif_c_gt_right:
    # else if c > right { break; }
    blt t2, t3, for_end
    j end_cond
    
end_cond:
    # printf("%c", ch);
    mv a0, s3
    li a7, 11
    ecall
    
    # i++
    addi t3, t3, 1 
    j for_loop
    
for_end:
    li s3, 10
    mv a0, s3
    li a7, 11
    ecall
    addi s5, s5, -1
    j while_r
    

end_while_r:
    addi s4, s4, -1
    ble s4, zero, exit_do
    ble s1, zero, exit_do
    j do_start

exit_do:
    li a0, 0
    li a7, 10
    ecall