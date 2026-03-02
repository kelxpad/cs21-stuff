#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <string.h>

char* replace_substring(const char *source,
                        const char *target,
                        const char *replacement){
    assert(source != NULL);
    assert(target != NULL);
    assert(replacement != NULL);

    int64_t len_source = strlen(source);
    int64_t len_target = strlen(target);
    int64_t len_replacement = strlen(replacement);

    // if target empty, return copy of source
    if (len_target == 0) {
        char *copy = malloc(len_source + 1); // 1 from \0
        assert(copy != NULL);
        for (int64_t i = 0; i <= len_source; i++) {
            copy[i] = source[i];
        }
        return copy;
    }

    // first pass: count occurrences of target
    int64_t count = 0;
    for (int64_t i = 0; i + len_target <= len_source;) {
        int64_t j = 0;
        while (j < len_target && source[i + j] == target[j]) {
            j++;
        }
        if (j == len_target) {
            count++;
            i += len_target; // move past this match
        } else {
            i++;
        }
    }

    // if no matches, return copy of source
    if (count == 0) {
        char *copy = malloc(len_source + 1);
        assert(copy != NULL);
        for (int64_t i = 0; i <= len_source; i++) {
            copy[i] = source[i];
        }
        return copy;
    }
    
    // calculate new length
    int64_t new_length = len_source + count * (len_replacement - len_target);

    char *result = malloc(new_length + 1);
    assert(result != NULL);

    // second pass: build result
    int64_t i = 0; // index for source
    int64_t k = 0; // index for result

    while (i < len_source) {
        int64_t j = 0;
        // check if target matches: are we still in target/source? do chars match?
        while (j < len_target && i + j < len_source && source[i + j] == target[j]) {
            j++;
        }

        if (j == len_target) {
            // copy replacement
            for (int64_t r = 0; r < len_replacement; r++) {
                result[k] = replacement[r];
                k++;
            }
            i += len_target;
        } else {
            result[k] = source[i];
            k++; i++;
        }
    }
    result[k] = '\0';
    return result;
}

int evaluate_replace_string(char *test_string, char *test_result){
    int i = 0;
    while (test_string[i]||test_result[i]){
        if (test_string[i]!=test_result[i]){
            return 1;
        }
        ++i;
    }
    return 0;
}
int main(){
    {
        const char *test_string = "Thirty-three thirsty, thundering thoroughbreds thumped Mr. Thurber on Thursday.";
        const char *test_substring = "th";
        const char *test_replace = "squw";
        char *test_result = "Thirty-squwree squwirsty, squwundering squworoughbreds squwumped Mr. Thurber on Thursday.";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }
    {
        const char *test_string = "Hello hello CS21!";
        const char *test_substring = "Hello";
        const char *test_replace = "Goodbye";
        char *test_result = "Goodbye hello CS21!";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }
    {
        const char *test_string = "Hello hello CS21!";
        const char *test_substring = "hEllO";
        const char *test_replace = "goodBye";
        char *test_result = "Hello hello CS21!";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }
    {
        const char *test_string = "ababABABabab";
        const char *test_substring = "ba";
        const char *test_replace = "cal";
        char *test_result = "acalbABABacalb";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }
    {
        const char *test_string = "ggGGGggGgGGGGGGgG";
        const char *test_substring = "gg";
        const char *test_replace = "All";
        char *test_result = "AllGGGAllGgGGGGGGgG";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }
    {
        const char *test_string = "aa aaa aaaa aaaaa";
        const char *test_substring = "aa";
        const char *test_replace = "rt";
        char *test_result = "rt rta rtrt rtrta";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }
    {
        const char *test_string = "Agree";
        const char *test_substring = "E";
        const char *test_replace = "EEEEEE";
        char *test_result = "Agree";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }
    {
        const char *test_string = "hello";
        const char *test_substring = "hello";
        const char *test_replace = "Hello World!";
        char *test_result = "Hello World!";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }
    {
        const char *test_string = "hello";
        const char *test_substring = "hello";
        const char *test_replace = "";
        char *test_result = "";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }
    {
        const char *test_string = "run";
        const char *test_substring = "walk";
        const char *test_replace = "sprint";
        char *test_result = "run";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }
    {
        const char *test_string = "Zero,one";
        const char *test_substring = "o";
        const char *test_replace = "0";
        char *test_result = "Zer0,0ne";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }
    {
        const char *test_string = "Zer0,0ne";
        const char *test_substring = "0";
        const char *test_replace = "o";
        char *test_result = "Zero,one";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }
    {
        const char *test_string = "pointer";
        const char *test_substring = "";
        const char *test_replace = "";
        char *test_result = "pointer";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }
    {
        const char *test_string = "spa ce dou t";
        const char *test_substring = "space";
        const char *test_replace = "tab";
        char *test_result = "spa ce dou t";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }
    {
        const char *test_string = "0123456789ABCDEF";
        const char *test_substring = "9AB";
        const char *test_replace = "Gabby";
        char *test_result = "012345678GabbyCDEF";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }
    {
        const char *test_string = "";
        const char *test_substring = "9AB";
        const char *test_replace = "Gabby";
        char *test_result = "";
        char* replaced_string = replace_substring(test_string, test_substring, test_replace);
        printf("Test case passed: %s",evaluate_replace_string(replaced_string, test_result) ? "False" : "True");
        printf("\n");
    }

}