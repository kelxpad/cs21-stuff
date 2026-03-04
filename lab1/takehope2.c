#include <stdio.h>

int main() {
  unsigned int n = 5;
  unsigned int size = 3;

  size = (size & 7) + 1;
  int height = size << 1;
  char ch = '\0';
  int level = n & 15;

  do {
    int r = height;

    while (r >= 0) {
      int num = r;
      int left = (r > size) ? r - size : size - r;
      int right = (r > size) ? size + height - r : r - size + height;

      for (int c = 0; c <= height; c++) {
        ch = ' ';

        if (c == left) {
          if (r == height) {
            ch = 'A';
          } else if (r == size) {
            ch = '<';
          } else if (r == 0) {
            ch = 'V';
          } else if (r > size) {
            ch = '/';
          } else {
            ch = '\\';
          }
        } else if (c == right) {
          if (r == size) {
            ch = '>';
          } else if (r > size) {
            ch = '\\';
          } else {
            ch = '/';
          }
        } else if (c > left && c < right) {
          if (level >= r + 1) {
            if (level > 0) {
              ch = '0' + num;

              if (ch > '9') {
                ch += 39;
              }
            }
          }
        } else if (c > right) {
          break;
        }

        printf("%c", ch);
      }

      ch = '\n';
      printf("%c", ch);
      r -= 1;
    }

    level--;
  } while (level > 0 && size > 0);
}