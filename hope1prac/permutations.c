#include <stdlib.h>
/**
 * Return an array of arrays of size *returnSize.
 * The sizes of the arrays are returned as *returnColumnSizes array.
 * Note: Both returned array and *columnSizes array must be malloced, assume caller calls free().
 */

void swap(int* a, int* b) {
    int t = *a;
    *a = *b;
    *b = t;
}

void backtrack(int* nums, int numsSize, int start, int** result, int* returnSize) {
    if (start == numsSize) {
        int* perm = malloc(numsSize * sizeof(int));

    for (int i = 0; i < numsSize; i++) {
        perm[i] = nums[i];
    }

    result[*returnSize] = perm;
    (*returnSize)++;
    return;
    }
    for (int i = start; i < numsSize; i++) {
        swap(&nums[start], &nums[i]);
        backtrack(nums, numsSize, start + 1, result, returnSize);
        swap(&nums[start], &nums[i]); // undo
    }
}
int** permute(int* nums, int numsSize, int* returnSize, int** returnColumnSizes) {
    int max = 720; // 6! max permutations for safety

    int** result = malloc(max * sizeof(int*));

    *returnColumnSizes = malloc(max * sizeof(int));

    *returnSize = 0; // no permutations yet

    backtrack(nums, numsSize, 0, result, returnSize);

    for (int i = 0; i < *returnSize; i++) {
        (*returnColumnSizes)[i] = numsSize;
    }
    return result;
}