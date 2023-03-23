#ifndef TGHE_SEMESTRAL_MATRIX_TOOLS_H
#define TGHE_SEMESTRAL_MATRIX_TOOLS_H

#include <stdio.h>
#include <malloc.h>

#define BUFFER_SIZE 128

typedef struct {
    unsigned int* col_count;
    unsigned int* row_count;
    unsigned int*** matrix;
} matrix_data;

// loads the first line from stdin
unsigned int* load_matrix_dims();

// loads the next line from stdin and parses it into an array of ints
unsigned int* load_input_data_row();

// method that allocates memory for the connection matrix
int allocate_matrix(matrix_data *m_data);

// fills the matrix with data from stdin
int fill_connection_matrix(matrix_data *m_data);

// runs all matrix intialization functions and returns a pointer to the matrix
// caller takes the responsibility of freeing the memory
matrix_data* initialize_matrix();


#endif //TGHE_SEMESTRAL_MATRIX_TOOLS_H
