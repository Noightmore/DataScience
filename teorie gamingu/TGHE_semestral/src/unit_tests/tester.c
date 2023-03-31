#include "tester.h"

int run_all_tests()
{
        test_loading_matrix_dims_from_stdin();
        test_load_input_data_row();
        test_allocate_connection_matrix();
        test_set_value_to_connection_matrix_by_input_row();
        test_initialize_connection_matrix();

        return 0;
}