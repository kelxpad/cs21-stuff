#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 256

double A[N][N];
double B[N][N];
double C[N][N];


void init_matrices(void) {
    srand(42);

    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            A[i][j] = (double)(rand() % 100);
            B[i][j] = (double)(rand() % 100);
            C[i][j] = 0.0;
        }

    }
}

void matmul_naive(void) {
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N; j++) {
            for (int k = 0; k < N; k++) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

#define BS 8
void matmul_optimized(void) {
    for (int i = 0; i < N; i += BS) {
        for (int k = 0; k < N; k += BS) {
            for (int j = 0; j < N; j += BS) {
                for (int ii = i; ii < N && ii < i+BS; ii++) {
                    for (int kk = k; kk < N && kk < k+BS; kk++) {
                        for (int jj = j; jj < N && jj < j+BS; jj++) {
                            C[ii][jj] += A[ii][kk] * B[kk][jj];
                        }
                    }
                }
            }
        }
    }
}

int main(void) {
    init_matrices();

    clock_t start = clock();

    matmul_optimized();

    clock_t end = clock();

    printf("Time: %.3f seconds\n",
           (double)(end - start) / CLOCKS_PER_SEC);

    printf("Checksum: %.2f\n", C[0][0]);

    return 0;
}