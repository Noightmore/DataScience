#include "tester.h"

int run_all_tests()
{
        run_matrix_tests();
        run_dijkstra_tests();
        return 0;
}

int run_matrix_tests()
{
        test_loading_matrix_dims_from_stdin();
        test_load_input_data_row();
        test_allocate_connection_matrix();
        test_set_value_to_connection_matrix_by_input_row();
        test_initialize_connection_matrix();

        return 0;
}

int run_dijkstra_tests()
{
        test_load_request_count_from_input_line();
        test_process_solution_request_line();
        return 0;
}