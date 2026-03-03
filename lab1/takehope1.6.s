# doesnt work for a0 = 0, will end up infinitely looping as the first iteration meets t0 = 1, a0 = 0 as t0 incrementing will never be 0
# fix: swap instructions, keep the loop
li t0, 0

loop:
    # do something with t0 here (print, etc.)
    bge t0, a0, end   # exit if t0 >= a0
    addi t0, t0, 1
    j loop

end:
    nop