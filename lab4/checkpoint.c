#include <stdio.h>
#include <string.h>
#include <time.h>

int main(int argc, char *argv[]) {
    if (argc < 2) {
        printf("No argument provided\n");
        return 1;
    }

    if (strcmp(argv[1], "1") == 0) {
        FILE *f;
        time_t timestamp;

        f = fopen("/var/tmp/.lab04", "r+b");
        if (f == NULL) {
            printf("Could not open.\n");
            return 1;
        }

        timestamp = time(NULL) + 5;  // extend by 5 seconds

        rewind(f);
        fwrite(&timestamp, sizeof(time_t), 1, f);
        fclose(f);

        printf("Trial extended by 5 seconds!\n");

    } else if (strcmp(argv[1], "2") == 0) {

        FILE *f = fopen("lab04", "r+b");
        if (!f) { return 1; }

        unsigned int patched = 0x00079a63; // bnez a5, 105b8 <main+0x2c>

        fseek(f, 0x5a4, SEEK_SET);
        fwrite(&patched, sizeof(patched), 1, f);

        fclose(f);

        printf("Patched main trial check!\n");
    } else if (strcmp(argv[1], "3") == 0) {
        FILE *f = fopen("lab04", "r+b");
        if (!f) { return 1; }

        unsigned int inst1 = 0x00000513; // li a0,0
        unsigned int inst2 = 0x00008067; // ret

        fseek(f, 0x438, SEEK_SET);
        fwrite(&inst1, sizeof(inst1), 1, f);
        fwrite(&inst2, sizeof(inst2), 1, f);

        fclose(f);

        printf("Patched check_trial to always succeed!");
    }
    return 0;
}

/*
EXPLANATIONS
Item 1: The program stores the trial expiration time as a Unix timestamp 
in "/var/tmp/.lab04".
To extend the trial period via `./checkpoint 1`, the program writes a new 
timestamp equal to the current Unix time plus 5 seconds.

This sets the expiration time to 5 seconds in the future, causing the 
program to report that the trial period still has a few seconds remaining
when `qemu-riscv32 ./lab04` is executed immediately afterward.

Item 2:
The conditional branch in main that controls the trial expiration logic was modified:

   105a4:	      /-- 00078a63          	beqz	a5,105b8 <main+0x2c>
to
   105a4:	      /-- 00079a63          	bnez	a5,105b8 <main+0x2c>

This reverses the branch condition, effectively bypassing the code path that prints
"Trial period has lapsed", allowing the code to continue execution regardless of the 
trial status.

Item 3: 
The beginning of the check_trial function was patched so that it immediately returns 0 (success).

   10438:	       fd010113          	addi	sp,sp,-48
   1043c:	       02112623          	sw	ra,44(sp)
to
   10438:	       00000513          	li	a0,0
   1043c:	       00008067          	ret

As a result, the trial period check has no effect when the `./lab04` is executed.
*/


/*
SCRATCH WORK
File begins with 0x7F 0x45 0x4C 0c46, confirming the ELF magic bytes.
At file offset 0x4, value is 0x01, indicating 32-bit format
At file offset 0x5, value is 0x01, indicating little endianness

Address of instruction that sets its return value in main: 0x106a0

section_header_start = 0xC40D8
at offset 0x32 = 0x001f, n = 31
.shstrtab index (n): 31

section header for .shstrtab = e_shoff + (n x 40)
= 0xC40D8 + (31 x 40)
= 0xC45B0 

data offset = 0xC45C0

S (file offset of .shstrtab data) = 0x000C3F8D
.shstrtab section header = 

Identify the offset from S containing .text: S + 0x25
text_section_header = 0xC4150
text_section_offset = 0x00000130 (hex was 30 01 00 00) (contains 0xff010113)

Memory address of instruction: 0x1069c
.text starting memory address: 0x10130

Offset within .text:
0x1069c − 0x10130 = 0x56c

.text file offset: 0x130

File offset of instruction:
0x130 + 0x56c = 0x69c

At file offset 0x69c, the instruction 0x00000793
(93 07 00 00 in little-endian) is present.

.sdata = 178 from the offset = 0xB2
B2 00 00 00 at 0x000c4380
0x000c4380+0x0c = starting memory address of .sdata
= DC 39 09 00 = 0x000939DC

0x000c4380+0x10 = file offset of section data .sdata
= DC 2D 08 00 = 0x00082DDC

offset_in_sdata = filepath_address - sdata_mem_start
= 0x93DE0 - 0x939DC = 0x404

filepath_file_offset = sdata_file_offset + offset_in_sdata
= 0x82ddc + 0x404 = 0x831e0

P = 0x831e0 = 20 03 24 00 = 0x230320 (memory address where .rodata lives)

.rodata = 43 bytes from the offset = 0x2B
2B 00 00 00 at 0x000c4178
0xc4178+0x0c = starting memory address of .rodata
= F0 7D 06 00 = 0x67df0
0xc4178+0x10 = file offset of section data .rodata
= F9 7D 05 00 = 0x57df0

"Trial period has lapsed" = 0x57e34
*/