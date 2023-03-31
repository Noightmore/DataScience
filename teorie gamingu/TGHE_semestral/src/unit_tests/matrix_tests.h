#ifndef TGHE_SEMESTRAL_MATRIX_TESTS_H
#define TGHE_SEMESTRAL_MATRIX_TESTS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <limits.h>

#include "../include/matrix_tools.h"

int test_loading_matrix_dims_from_stdin();

int test_load_input_data_row();

int test_allocate_connection_matrix();

int test_set_value_to_connection_matrix_by_input_row();

int test_initialize_connection_matrix();

#endif //TGHE_SEMESTRAL_MATRIX_TESTS_H
