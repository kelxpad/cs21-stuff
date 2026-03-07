.text

main:
  la a0, arr
  li a1, 6
  li a2, 0
  call f

  li a7, 1
  ecall

  li a7, 10
  ecall

f:
  addi sp, sp, -12
  sw ra, 8(sp)
  sw s0, 4(sp)
  sw s1, 0(sp)

loop:
  bge zero, a1, f__ret_a2

  lw s1, 0(a0) # use a0 directly
  add a2, a2, s1
  addi a0, a0, 4
  addi a1, a1, -1
  j loop

f__ret_a2:
  mv a0, a2
f__ret:
  lw s1, 0(sp)
  lw s0, 4(sp)
  lw ra, 8(sp)
  addi sp, sp, 12
  ret

.data

arr:
  .word 10
  .word 20
  .word 30
  .word 40
  .word 50
  .word 60