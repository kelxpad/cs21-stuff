#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    if (argv[1] == '1') {

        size_t elements_read;
        char buffer[100];

        FILE *f = fopen("/var/tmp/.lab04", "r");
        elements_read = fread(buffer,  1, (sizeof(buffer), f));
        fclose(f);

        for (int i = 0; i < elements_read; i++) {
            printf("[%i] %c\n", i, buf[i]);
        }
        // Do Item 1: Increase trial period by 5 seconds
    } else if (argv[1] == '2') {
        // Do Item 2: Trial period check has no effect
    } else if (argv[1] == '3') {
        // Do Item 3:
    }
}

/*
hints subitem 1 no need to edit hex, subitems 2-3 need to edit hex
item 2: make the jalr into a nop to skip the trial shit

idea to help with this lab: 
- python code to convert hex to ascii
- ripes to translate hex to binary of instructions

addresses of note:

header = 0x000c40d8
message = 0x00057df0
.shstrtab_index =o 0x001F
.shstrtab_section = 0x000C3F8D

text_sh      = 0xc4150
text_offset  = 0x010130
text_segment = 0x00000120
text_size    = 0x10
*/

/*
File begins with 0x7F 0x45 0x4C 0c46, confirming the ELF magic bytes.
At file offset 0x4, value is 0x01, indicating 32-bit format
At file offset 0x5, value is 0x01, indicating little endianness

Address of instruction that sets its return value in main: 0x106a0
*/