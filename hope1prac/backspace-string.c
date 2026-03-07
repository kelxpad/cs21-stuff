#include <stdbool.h>
#include <string.h>
bool backspaceCompare(char* s, char* t) {
    int i = strlen(s) - 1;
    int j = strlen(t) - 1;

    int skip_ss = 0;
    int skip_tt = 0;

    while (i >= 0 || j >= 0) {
        // find next valid char in s
        while (i >= 0) {
            if (s[i] == '#') {
                skip_ss++;
                i--;
            }
            else if (skip_ss > 0) {
                skip_ss--;
                i--;
            } else {
                break; // char found
            }
        }

        // find next valid char in t
        while (j >= 0) {
            if (t[j] == '#') {
                skip_tt++;
                j--;
            } else if(skip_tt > 0) {
                skip_tt--;
                j--;
            } else {
                break;
            }
        }

        if (i >= 0 && j >= 0) {
            if (s[i] != t[j]) { return false; }
            
        } else { 
                if (i >= 0 || j >= 0) { return false; }
            }
        i--; j--;
    }
    return true;
}