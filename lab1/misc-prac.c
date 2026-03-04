/*
li s0, 0
li s1, 12345
li s2, 10

L1:
  beq s1, zero, END

  rem t0, s1, s2
  add s0, s0, t0
  div s1, s1, s2

  j L1

END:
*/

int s0 = 0;
int s1 = 12345;
int s2 = 10;

while (s1 != 0) {
    int t0 = s1 % s2;
    s0 += t0;
    s1 /= s2; 
}