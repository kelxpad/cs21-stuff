#include<stdio.h>

// int fib( int i ) {
//   printf("fib(%d) : i = %d : &i = %p\n", i, i, &i);
//   return (i==1 || i==2) ? 1 : fib(i-1) + fib(i-2);
// }

// int fib( int i ) {
//   char x[10]; // unused array of 10 characters
//   printf("fib(%d) : i = %d : &i = %p\n", i, i, &i);
//   return (i==1 || i==2) ? 1 : fib(i-1) + fib(i-2);
// }

int fib( int i ) {
  char x[11]; // unused array of 11 characters
  printf("fib(%d) : i = %d : &i = %p\n", i, i, &i);
  return (i==1 || i==2) ? 1 : fib(i-1) + fib(i-2);
}

int main() {
  int n = 9;
  printf("main   : n = %d : &n = %p\n", n, &n);
  fib(n);
  return 0;
}

/*
Step 1. Compile the program (without optimizations) and then run the program.
main   : n = 9 : &n = 0x7fffbb2be2a4
fib(9) : i = 9 : &i = 0x7fffbb2be27c
fib(8) : i = 8 : &i = 0x7fffbb2be24c
fib(7) : i = 7 : &i = 0x7fffbb2be21c
fib(6) : i = 6 : &i = 0x7fffbb2be1ec
fib(5) : i = 5 : &i = 0x7fffbb2be1bc
fib(4) : i = 4 : &i = 0x7fffbb2be18c
fib(3) : i = 3 : &i = 0x7fffbb2be15c
fib(2) : i = 2 : &i = 0x7fffbb2be12c
fib(1) : i = 1 : &i = 0x7fffbb2be12c
fib(2) : i = 2 : &i = 0x7fffbb2be15c
fib(3) : i = 3 : &i = 0x7fffbb2be18c
fib(2) : i = 2 : &i = 0x7fffbb2be15c
fib(1) : i = 1 : &i = 0x7fffbb2be15c
fib(4) : i = 4 : &i = 0x7fffbb2be1bc
fib(3) : i = 3 : &i = 0x7fffbb2be18c
fib(2) : i = 2 : &i = 0x7fffbb2be15c
fib(1) : i = 1 : &i = 0x7fffbb2be15c
fib(2) : i = 2 : &i = 0x7fffbb2be18c
fib(5) : i = 5 : &i = 0x7fffbb2be1ec
fib(4) : i = 4 : &i = 0x7fffbb2be1bc
fib(3) : i = 3 : &i = 0x7fffbb2be18c
fib(2) : i = 2 : &i = 0x7fffbb2be15c
fib(1) : i = 1 : &i = 0x7fffbb2be15c
fib(2) : i = 2 : &i = 0x7fffbb2be18c
fib(3) : i = 3 : &i = 0x7fffbb2be1bc
fib(2) : i = 2 : &i = 0x7fffbb2be18c
fib(1) : i = 1 : &i = 0x7fffbb2be18c
fib(6) : i = 6 : &i = 0x7fffbb2be21c
fib(5) : i = 5 : &i = 0x7fffbb2be1ec
fib(4) : i = 4 : &i = 0x7fffbb2be1bc
fib(3) : i = 3 : &i = 0x7fffbb2be18c
fib(2) : i = 2 : &i = 0x7fffbb2be15c
fib(1) : i = 1 : &i = 0x7fffbb2be15c
fib(2) : i = 2 : &i = 0x7fffbb2be18c
fib(3) : i = 3 : &i = 0x7fffbb2be1bc
fib(2) : i = 2 : &i = 0x7fffbb2be18c
fib(1) : i = 1 : &i = 0x7fffbb2be18c
fib(4) : i = 4 : &i = 0x7fffbb2be1ec
fib(3) : i = 3 : &i = 0x7fffbb2be1bc
fib(2) : i = 2 : &i = 0x7fffbb2be18c
fib(1) : i = 1 : &i = 0x7fffbb2be18c
fib(2) : i = 2 : &i = 0x7fffbb2be1bc
fib(7) : i = 7 : &i = 0x7fffbb2be24c
fib(6) : i = 6 : &i = 0x7fffbb2be21c
fib(5) : i = 5 : &i = 0x7fffbb2be1ec
fib(4) : i = 4 : &i = 0x7fffbb2be1bc
fib(3) : i = 3 : &i = 0x7fffbb2be18c
fib(2) : i = 2 : &i = 0x7fffbb2be15c
fib(1) : i = 1 : &i = 0x7fffbb2be15c
fib(2) : i = 2 : &i = 0x7fffbb2be18c
fib(3) : i = 3 : &i = 0x7fffbb2be1bc
fib(2) : i = 2 : &i = 0x7fffbb2be18c
fib(1) : i = 1 : &i = 0x7fffbb2be18c
fib(4) : i = 4 : &i = 0x7fffbb2be1ec
fib(3) : i = 3 : &i = 0x7fffbb2be1bc
fib(2) : i = 2 : &i = 0x7fffbb2be18c
fib(1) : i = 1 : &i = 0x7fffbb2be18c
fib(2) : i = 2 : &i = 0x7fffbb2be1bc
fib(5) : i = 5 : &i = 0x7fffbb2be21c
fib(4) : i = 4 : &i = 0x7fffbb2be1ec
fib(3) : i = 3 : &i = 0x7fffbb2be1bc
fib(2) : i = 2 : &i = 0x7fffbb2be18c
fib(1) : i = 1 : &i = 0x7fffbb2be18c
fib(2) : i = 2 : &i = 0x7fffbb2be1bc
fib(3) : i = 3 : &i = 0x7fffbb2be1ec
fib(2) : i = 2 : &i = 0x7fffbb2be1bc
fib(1) : i = 1 : &i = 0x7fffbb2be1bc


Step 2: Observe the logs produced by the program. There is one 'logging' (printf) instruction in main and one logging instruction in fib. Each call to a function will produce one line of the logs.

Guide Questions:
1. What is the address of the int variable i for the first fib(9) call? You can see this from the first log produced by the fib function (not the main function)
0x7fffbb2be27c
2. What is the address of the int variable i for the first fib(8) call? You can see this from the second log produced by the fib function.
0x7fffbb2be24c
3. What is the address of the int variable i for the first fib(7) call? You can see this from the third log produced by the fib function.
0x7fffbb2be21c
4. Can you observe pattern of the change of address of variable i as the sequence of calls to fib continues? Describe the pattern.
The address decreases by 48 bytes for each deeper recursive call, indicating that each stack frame occupies 48 bytes and the stack grows downward in memory.

5. Look at the address of variable i for the fib(2) and fib(1) calls. What can you observe? Explain this observation.
The address decreases by 48 bytes for each recursive call, showing that each fib function call creates a stack frame of 48 bytes. The stack grows downward in memory.

The addresses for fib(2) and fib(1) are often identical because once fib(2) returns, its stack frame is popped and the memory is reused for fib(1). This reuse of stack memory explains why the addresses are the same.
Step 3: Store the logs for this run of the program so it can be used for comparison later.
Done.

STEP 4: Change the function fib by adding an (unused) array of characters of size 10.
STEP 5: Compile and run the updated program and observe the produced logs for this run.

main   : n = 9 : &n = 0x7ffe77ef4784
fib(9) : i = 9 : &i = 0x7ffe77ef473c
fib(8) : i = 8 : &i = 0x7ffe77ef46ec
fib(7) : i = 7 : &i = 0x7ffe77ef469c
fib(6) : i = 6 : &i = 0x7ffe77ef464c
fib(5) : i = 5 : &i = 0x7ffe77ef45fc
fib(4) : i = 4 : &i = 0x7ffe77ef45ac
fib(3) : i = 3 : &i = 0x7ffe77ef455c
fib(2) : i = 2 : &i = 0x7ffe77ef450c
fib(1) : i = 1 : &i = 0x7ffe77ef450c
fib(2) : i = 2 : &i = 0x7ffe77ef455c
fib(3) : i = 3 : &i = 0x7ffe77ef45ac
fib(2) : i = 2 : &i = 0x7ffe77ef455c
fib(1) : i = 1 : &i = 0x7ffe77ef455c
fib(4) : i = 4 : &i = 0x7ffe77ef45fc
fib(3) : i = 3 : &i = 0x7ffe77ef45ac
fib(2) : i = 2 : &i = 0x7ffe77ef455c
fib(1) : i = 1 : &i = 0x7ffe77ef455c
fib(2) : i = 2 : &i = 0x7ffe77ef45ac
fib(5) : i = 5 : &i = 0x7ffe77ef464c
fib(4) : i = 4 : &i = 0x7ffe77ef45fc
fib(3) : i = 3 : &i = 0x7ffe77ef45ac
fib(2) : i = 2 : &i = 0x7ffe77ef455c
fib(1) : i = 1 : &i = 0x7ffe77ef455c
fib(2) : i = 2 : &i = 0x7ffe77ef45ac
fib(3) : i = 3 : &i = 0x7ffe77ef45fc
fib(2) : i = 2 : &i = 0x7ffe77ef45ac
fib(1) : i = 1 : &i = 0x7ffe77ef45ac
fib(6) : i = 6 : &i = 0x7ffe77ef469c
fib(5) : i = 5 : &i = 0x7ffe77ef464c
fib(4) : i = 4 : &i = 0x7ffe77ef45fc
fib(3) : i = 3 : &i = 0x7ffe77ef45ac
fib(2) : i = 2 : &i = 0x7ffe77ef455c
fib(1) : i = 1 : &i = 0x7ffe77ef455c
fib(2) : i = 2 : &i = 0x7ffe77ef45ac
fib(3) : i = 3 : &i = 0x7ffe77ef45fc
fib(2) : i = 2 : &i = 0x7ffe77ef45ac
fib(1) : i = 1 : &i = 0x7ffe77ef45ac
fib(4) : i = 4 : &i = 0x7ffe77ef464c
fib(3) : i = 3 : &i = 0x7ffe77ef45fc
fib(2) : i = 2 : &i = 0x7ffe77ef45ac
fib(1) : i = 1 : &i = 0x7ffe77ef45ac
fib(2) : i = 2 : &i = 0x7ffe77ef45fc
fib(7) : i = 7 : &i = 0x7ffe77ef46ec
fib(6) : i = 6 : &i = 0x7ffe77ef469c
fib(5) : i = 5 : &i = 0x7ffe77ef464c
fib(4) : i = 4 : &i = 0x7ffe77ef45fc
fib(3) : i = 3 : &i = 0x7ffe77ef45ac
fib(2) : i = 2 : &i = 0x7ffe77ef455c
fib(1) : i = 1 : &i = 0x7ffe77ef455c
fib(2) : i = 2 : &i = 0x7ffe77ef45ac
fib(3) : i = 3 : &i = 0x7ffe77ef45fc
fib(2) : i = 2 : &i = 0x7ffe77ef45ac
fib(1) : i = 1 : &i = 0x7ffe77ef45ac
fib(4) : i = 4 : &i = 0x7ffe77ef464c
fib(3) : i = 3 : &i = 0x7ffe77ef45fc
fib(2) : i = 2 : &i = 0x7ffe77ef45ac
fib(1) : i = 1 : &i = 0x7ffe77ef45ac
fib(2) : i = 2 : &i = 0x7ffe77ef45fc
fib(5) : i = 5 : &i = 0x7ffe77ef469c
fib(4) : i = 4 : &i = 0x7ffe77ef464c
fib(3) : i = 3 : &i = 0x7ffe77ef45fc
fib(2) : i = 2 : &i = 0x7ffe77ef45ac
fib(1) : i = 1 : &i = 0x7ffe77ef45ac
fib(2) : i = 2 : &i = 0x7ffe77ef45fc
fib(3) : i = 3 : &i = 0x7ffe77ef464c
fib(2) : i = 2 : &i = 0x7ffe77ef45fc
fib(1) : i = 1 : &i = 0x7ffe77ef45fc
Guide Question:

How is the pattern of change of address of variable i for this program (with the addtional char x[10]; line) different from pattern produced by the original program (no additional local variables)? Relate this to the idea of the stack frame size.
The address now decreases every 80 bytes per call instead of 48 bytes. The unused array made the stack frame grow bigger.

STEP 6: Changed the function fib by changing the array of characters size to 11.

int fib( int i ) {
  char x[11]; // unused array of 11 characters
  printf("fib(%d) : i = %d : &i = %p\n", i, i, &i);
  return (i==1 || i==2) ? 1 : fib(i-1) + fib(i-2);
}
STEP 7: Compile and run the updated program and observe the produced logs for this run.
main   : n = 9 : &n = 0x7ffd652caec4
fib(9) : i = 9 : &i = 0x7ffd652cae7c
fib(8) : i = 8 : &i = 0x7ffd652cae2c
fib(7) : i = 7 : &i = 0x7ffd652caddc
fib(6) : i = 6 : &i = 0x7ffd652cad8c
fib(5) : i = 5 : &i = 0x7ffd652cad3c
fib(4) : i = 4 : &i = 0x7ffd652cacec
fib(3) : i = 3 : &i = 0x7ffd652cac9c
fib(2) : i = 2 : &i = 0x7ffd652cac4c
fib(1) : i = 1 : &i = 0x7ffd652cac4c
fib(2) : i = 2 : &i = 0x7ffd652cac9c
fib(3) : i = 3 : &i = 0x7ffd652cacec
fib(2) : i = 2 : &i = 0x7ffd652cac9c
fib(1) : i = 1 : &i = 0x7ffd652cac9c
fib(4) : i = 4 : &i = 0x7ffd652cad3c
fib(3) : i = 3 : &i = 0x7ffd652cacec
fib(2) : i = 2 : &i = 0x7ffd652cac9c
fib(1) : i = 1 : &i = 0x7ffd652cac9c
fib(2) : i = 2 : &i = 0x7ffd652cacec
fib(5) : i = 5 : &i = 0x7ffd652cad8c
fib(4) : i = 4 : &i = 0x7ffd652cad3c
fib(3) : i = 3 : &i = 0x7ffd652cacec
fib(2) : i = 2 : &i = 0x7ffd652cac9c
fib(1) : i = 1 : &i = 0x7ffd652cac9c
fib(2) : i = 2 : &i = 0x7ffd652cacec
fib(3) : i = 3 : &i = 0x7ffd652cad3c
fib(2) : i = 2 : &i = 0x7ffd652cacec
fib(1) : i = 1 : &i = 0x7ffd652cacec
fib(6) : i = 6 : &i = 0x7ffd652caddc
fib(5) : i = 5 : &i = 0x7ffd652cad8c
fib(4) : i = 4 : &i = 0x7ffd652cad3c
fib(3) : i = 3 : &i = 0x7ffd652cacec
fib(2) : i = 2 : &i = 0x7ffd652cac9c
fib(1) : i = 1 : &i = 0x7ffd652cac9c
fib(2) : i = 2 : &i = 0x7ffd652cacec
fib(3) : i = 3 : &i = 0x7ffd652cad3c
fib(2) : i = 2 : &i = 0x7ffd652cacec
fib(1) : i = 1 : &i = 0x7ffd652cacec
fib(4) : i = 4 : &i = 0x7ffd652cad8c
fib(3) : i = 3 : &i = 0x7ffd652cad3c
fib(2) : i = 2 : &i = 0x7ffd652cacec
fib(1) : i = 1 : &i = 0x7ffd652cacec
fib(2) : i = 2 : &i = 0x7ffd652cad3c
fib(7) : i = 7 : &i = 0x7ffd652cae2c
fib(6) : i = 6 : &i = 0x7ffd652caddc
fib(5) : i = 5 : &i = 0x7ffd652cad8c
fib(4) : i = 4 : &i = 0x7ffd652cad3c
fib(3) : i = 3 : &i = 0x7ffd652cacec
fib(2) : i = 2 : &i = 0x7ffd652cac9c
fib(1) : i = 1 : &i = 0x7ffd652cac9c
fib(2) : i = 2 : &i = 0x7ffd652cacec
fib(3) : i = 3 : &i = 0x7ffd652cad3c
fib(2) : i = 2 : &i = 0x7ffd652cacec
fib(1) : i = 1 : &i = 0x7ffd652cacec
fib(4) : i = 4 : &i = 0x7ffd652cad8c
fib(3) : i = 3 : &i = 0x7ffd652cad3c
fib(2) : i = 2 : &i = 0x7ffd652cacec
fib(1) : i = 1 : &i = 0x7ffd652cacec
fib(2) : i = 2 : &i = 0x7ffd652cad3c
fib(5) : i = 5 : &i = 0x7ffd652caddc
fib(4) : i = 4 : &i = 0x7ffd652cad8c
fib(3) : i = 3 : &i = 0x7ffd652cad3c
fib(2) : i = 2 : &i = 0x7ffd652cacec
fib(1) : i = 1 : &i = 0x7ffd652cacec
fib(2) : i = 2 : &i = 0x7ffd652cad3c
fib(3) : i = 3 : &i = 0x7ffd652cad8c
fib(2) : i = 2 : &i = 0x7ffd652cad3c
fib(1) : i = 1 : &i = 0x7ffd652cad3c
Guide Questions:

How is the pattern of change of address of variable i for this program (with the char x[11]; line) different from pattern produced by the second program (with the line char x[10];)?
It's the same??
The stack frame size remains 80 bytes even when increasing the array from 10 to 11 characters. This is because the compiler aligns stack frames to certain memory boundaries (typically 16 byte), so the extra 1 byte does not change the total allocated size.
How many times does program call function fib?
67 times.

What is the maximum number of stack frames from fib function calls that exist simultaneously on the call stack?
9 (simultaneous active calls)
*/