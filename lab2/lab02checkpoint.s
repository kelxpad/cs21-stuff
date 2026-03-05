.text

main:
  li a7, 63
  li a0, 0
  la a1, input
  li a2, 10
  ecall

  la a0, input
  la a1, output
  li a2, 10
  call retain_letters

  li a7, 4
  la a0, output
  ecall

  li a7, 10
  ecall

retain_letters:
    # PUSH ra, a0, a1, a2
    addi sp, sp, -16
    sw ra, 12(sp)
    sw a0, 8(sp)
    sw a1, 4(sp)
    sw a2, 0(sp)
    
    # if (n <= 0) { return; }
    blt a2, zero, retain_letters_ret
    beq a2, zero, retain_letters_ret
    
    # if (ch == '\0') { return; }
    lb t4, 0(a0)
    beq t4, zero, retain_letters_ret
    
    
    # else if (('A' <= ch && ch <= 'Z') || ('a' <= ch && ch <= 'z'))
    li t0 0x40 # @
    li t1 0x5B # open bracket
    li t2 0x60 # `
    li t3 0x7B # {
    
    # filter out special characters
    
    slt t0, t0, t4
    slt t1, t4, t1
    slt t2, t2, t4
    slt t3, t4, t3
    
    and t0, t0, t1
    and t1, t2, t3
    or t0, t0, t1
 
    beq t0, zero, skip_store
    
    # if letter
    sb t4, 0(a1)
    addi a1, a1, 1 # output

skip_store:
    addi a0, a0, 1 #input
    addi a2, a2, -1 # n - 1
    
    call retain_letters
    
retain_letters_ret:
    # POP ra, a0, a1, a2
    lw a2, 0(sp)
    lw a1, 4(sp)
    lw a0, 8(sp)
    lw ra, 12(sp)
    addi sp, sp, 16
    
    # RETURN
    ret
    
.data

input: .zero 11
output: .zero 11