# t0 = x, t1 = y, t2 = z, and t3 = r
main:
    slt t4, zero, t0 # t4 = 1 if x > 0
    slt t5, t0, zero # t5 = 1 if x < 0
    or t4, t4, t5 # t4 = 1 if x != 0
    slt t5, t1, t2 # t5 = 1 if y < z
    and t3, t4, t5 # r = t4 & t5
    