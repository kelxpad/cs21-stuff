#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

#define OUTPUT_PATH "output.ppm"

void transpose_basic(uint8_t *data, uint32_t width, uint32_t height) {
    uint8_t *temp = calloc(width * height * 3, 1);
    if (!temp) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }

    for (uint32_t rgb = 0; rgb < 3; rgb++) {
        for (uint32_t c = 0; c < width; c++) {
            for (uint32_t r = 0; r < height; r++) {
                temp[c * height * 3 + r * 3 + rgb] =
                    data[r * width * 3 + c * 3 + rgb];
            }
        }
    }

    memcpy(data, temp, width * height * 3);
    free(temp);
}

int chunksize = 32;
void transpose_improved(uint8_t *data,
                        uint32_t width,
                        uint32_t height) {
    uint8_t *temp = calloc(width * height * 3, 1);
    if (!temp) {
        fprintf(stderr, "Memory allocation failed\n");
        exit(1);
    }

    for (uint32_t r = 0; r < height; r += chunksize) {
        for (uint32_t c = 0; c < width; c += chunksize) {
            for (uint32_t rr = r; rr < height && rr < r+chunksize; rr++) {
                for (uint32_t cc = c; cc < width && cc < c+chunksize; cc++) {
                    for (uint32_t rgb = 0; rgb < 3; rgb++) {
                        temp[cc * height * 3 + rr * 3 + rgb] = 
                        data[rr * width * 3 + cc * 3 + rgb];
                    }
                }
            }
        }
    }
    memcpy(data, temp, width * height * 3);
    free(temp);
}


void skip_comment_lines(FILE *fp) {
    int ch;

    while ((ch = fgetc(fp)) == '#') {
        fscanf(fp, " %*[^\n]\n");
    }

    ungetc(ch, fp);
}

int read_header(FILE *in,
                uint32_t *width,
                uint32_t *height,
                uint32_t *max_value) {
    char magic[3];

    if (fread(magic, 1, 3, in) != 3 || strncmp(magic, "P6\n", 3) != 0) {
        fprintf(stderr, "Invalid or missing P6 header\n");
        return -1;
    }

    skip_comment_lines(in);

    if (fscanf(in, " %u %u", width, height) != 2) {
        fprintf(stderr, "Failed to read image dimensions\n");
        return -1;
    }

    skip_comment_lines(in);

    if (fscanf(in, " %u%*c", max_value) != 1) {
        fprintf(stderr, "Failed to read max value\n");
        return -1;
    }

    return 0;
}

uint8_t *read_image_data(FILE *in, size_t size) {
    uint8_t *data = malloc(size);
    if (!data) {
        fprintf(stderr, "Failed to allocate image buffer\n");
        return NULL;
    }

    size_t read_bytes = fread(data, 1, size, in);
    if (read_bytes != size) {
        fprintf(stderr, "Image read error (%zu/%zu bytes)\n", read_bytes, size);
        free(data);
        return NULL;
    }

    return data;
}

int write_image(const char *path,
                uint8_t *data,
                uint32_t width,
                uint32_t height,
                uint32_t max_value) {
    FILE *out = fopen(path, "wb");
    if (!out) {
        fprintf(stderr, "Error opening output file\n");
        return -1;
    }

    fprintf(out, "P6\n%u %u\n%u\n", height, width, max_value);
    fwrite(data, 1, width * height * 3, out);

    fclose(out);

    return 0;
}

int main(int argc, char *argv[]) {
    if (argc != 3) {
        fprintf(stderr, "Usage: %s <filename> <0|blocksize>\n", argv[0]);
        return -1;
    }

    const char *input_path = argv[1];
    int mode = atoi(argv[2]);

    FILE *in = fopen(input_path, "rb");
    if (!in) {
        fprintf(stderr, "Error reading %s\n", input_path);
        return -1;
    }

    uint32_t width, height, max_value;

    if (read_header(in, &width, &height, &max_value) != 0) {
        fclose(in);
        return -1;
    }

    printf("%u x %u image with max value %u\n", width, height, max_value);

    size_t data_size = (size_t)width * height * 3;
    uint8_t *data = read_image_data(in, data_size);
    fclose(in);

    if (!data) {
        return -1;
    }

    if (mode == 0) {
        transpose_basic(data, width, height);
    } else {
        transpose_improved(data, width, height);
    }

    if (write_image(OUTPUT_PATH, data, width, height, max_value) != 0) {
        free(data);
        return -1;
    }

    free(data);
}