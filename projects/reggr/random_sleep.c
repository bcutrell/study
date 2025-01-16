#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <unistd.h>

#define MAX_CONTENT_SIZE 10000
#define TIMESTAMP_SIZE 64

// Function to read entire file content
char* read_file(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        fprintf(stderr, "Error opening input file\n");
        return NULL;
    }

    static char content[MAX_CONTENT_SIZE];
    size_t read_size = fread(content, 1, MAX_CONTENT_SIZE - 1, file);  // Changed 'content' to 'file' here
    content[read_size] = '\0';
    fclose(file);
    return content;
}

// Function to get current timestamp
void get_timestamp(char* buffer) {
    time_t now = time(NULL);
    struct tm* tm_info = localtime(&now);
    strftime(buffer, TIMESTAMP_SIZE, "%Y-%m-%d %H:%M:%S", tm_info);
}

// Main random sleep function
void random_sleep(const char* input_file, const char* output_file) {
    // Read input file
    char* content = read_file(input_file);
    if (content == NULL) {
        return;
    }

    // Generate random sleep duration
    srand(time(NULL));
    double duration = (double)rand() / RAND_MAX * 5.0;
    printf("Sleeping for %.2f seconds...\n", duration);

    // Sleep for the random duration
    usleep((unsigned int)(duration * 1000000));

    // Get current timestamp
    char timestamp[TIMESTAMP_SIZE];
    get_timestamp(timestamp);

    // Write output file
    FILE* file = fopen(output_file, "w");
    if (file == NULL) {
        fprintf(stderr, "Error opening output file\n");
        return;
    }

    fprintf(file, "start=%s\n", timestamp);
    fprintf(file, "sleep=%.2f\n", duration);
    fprintf(file, "input_content=%s", content);
    fclose(file);
}

int main(int argc, char* argv[]) {
    if (argc != 5) {
        fprintf(stderr, "Usage: %s -i <input_file> -o <output_file>\n", argv[0]);
        return 1;
    }

    char* input_file = NULL;
    char* output_file = NULL;

    // Parse command line arguments
    for (int i = 1; i < argc; i += 2) {
        if (strcmp(argv[i], "-i") == 0) {
            input_file = argv[i + 1];
        } else if (strcmp(argv[i], "-o") == 0) {
            output_file = argv[i + 1];
        }
    }

    if (input_file == NULL || output_file == NULL) {
        fprintf(stderr, "Both input and output files must be specified\n");
        return 1;
    }

    random_sleep(input_file, output_file);
    return 0;
}
