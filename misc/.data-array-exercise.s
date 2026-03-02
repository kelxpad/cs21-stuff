.data
arr: .word 10, 20, 30, 40, 50, 60, 70, 80, 90, 100

.text
la t0, arr
li t1, 1  # i = 1 (start at second element)
li t2, 10 # size
lw t3, 0(t0) # stores arr[0]

loop:
	beq t1, t2, done

	slli t4, t1, 2
	add t5, t0, t4
	lw t6, 0(t5)
	
	sub t3, t3, t6

	addi t1, t1, 1
	j loop

done:
	add a0, zero, t3
	li a7, 1
	ecall
	li a7, 93
	li a0, 0
	ecall