#ifndef TGHE_SEMESTRAL_GENERAL_TOOLS_H
#define TGHE_SEMESTRAL_GENERAL_TOOLS_H

#include <stdio.h>
#include <malloc.h>

#define BUFFER_SIZE 128

// loads the first line from stdin
unsigned int* load_matrix_dims();

// loads the next line from stdin and parses it into an array of ints
unsigned int* load_input_data_row();

#endif //TGHE_SEMESTRAL_GENERAL_TOOLS_H
