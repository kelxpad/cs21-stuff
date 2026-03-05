int count_char(const char *str, char ch) {
    if (str == NULL) {
        return 0;
    }

    int count = 0;
    for (int i = 0; str[i] != '\0'; i++) {
        if (str[i] == ch) {
            count++;
        }
    }
    return count;
}

// recursive
int count_char(const char *str, char ch) {
    if (*str == '\0') {
        return 0;
    }
    if (*str == ch) {
        return 1 + count_char(str + 1, ch);
    }

    return count_char(str + 1, ch);
}