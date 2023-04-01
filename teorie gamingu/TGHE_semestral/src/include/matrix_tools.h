#ifndef TGHE_SEMESTRAL_MATRIX_TOOLS_H
#define TGHE_SEMESTRAL_MATRIX_TOOLS_H

#include <stdio.h>
#include <unistd.h>
#include <alloca.h>

#define BUFFER_SIZE 128
#define NORMALIZATION_VALUE 1000000

typedef struct matrix_data matrix_data;

struct matrix_data
{
    unsigned int* size;
    unsigned int* connection_count;
    unsigned int*** matrix;
};

// loads the first line from stdin
unsigned int* load_matrix_dims_from_input(char* input);

// loads the next line from stdin and parses it into an array of ints
unsigned int* load_input_data_row(char* input, unsigned int* coords);

// method that allocates memory for the connection matrix
int allocate_matrix(matrix_data *m_data);

// fills the matrix with data from stdin
int set_value_to_connection_matrix_by_input_row(matrix_data *m_data, char* input);

// runs all matrix intialization functions and returns a pointer to the matrix
// caller takes the responsibility of freeing the memory
matrix_data* initialize_matrix(char* input);

#endif //TGHE_SEMESTRAL_MATRIX_TOOLS_H