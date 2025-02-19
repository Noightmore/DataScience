#include "matrix_tests.h"

int test_loading_matrix_dims_from_stdin()
{
        // Test case 1: Empty input
        char input1[] = "";
        assert(load_matrix_dims_from_input(input1) == NULL);

        // Test case 2: Valid input
        char input2[] = "3 4";
        unsigned int* dims2 = load_matrix_dims_from_input(input2);
        assert(dims2[0] == 3 && dims2[1] == 4);

        // Test case 3: Only one dimension given
        char input3[] = "5";
        assert(load_matrix_dims_from_input(input3) == NULL);

        // Test case 4: Non-integer input
        char input4[] = "2 hello";
        assert(load_matrix_dims_from_input(input4) == NULL);

        // Test case 5: Large input
        char input5[BUFFER_SIZE] = {0};
        sprintf(input5, "%u %u", UINT_MAX-1, UINT_MAX);
        unsigned int* dims5 = load_matrix_dims_from_input(input5);
        assert(dims5[0] == UINT_MAX-1 && dims5[1] == UINT_MAX);

        printf("All tests passed successfully - loading_matrix_dims_from_stdin\n");
        return 0;
}

int test_load_input_data_row()
{
        unsigned int coords[2];
        char* input = "1 2 0.5";
        unsigned int* result = load_input_data_row(input, coords);
        assert(result != NULL);
        assert(*result == 500000);
        assert(coords[0] == 1);
        assert(coords[1] == 2);

        unsigned int coords2[2];
        char* input2 = "1 abc 0.5";
        unsigned int* result2 = load_input_data_row(input2, coords2);
        assert(result2 == NULL);

        unsigned int coords3[2];
        char* input3 = "1 2 1.5";
        unsigned int* result3 = load_input_data_row(input3, coords3);
        assert(result3 == NULL);


        printf("All tests passed successfully - loading_input_data_row\n");
        return 0;
}

int test_allocate_connection_matrix()
{
        // Test case 1: Allocate a matrix of size 2x2
        matrix_data m_data1 = {
                .connection_count = malloc(sizeof(unsigned int)),
                .size = malloc(sizeof(unsigned int))
        };
        *m_data1.connection_count = 2;
        *m_data1.size = 2;
        int result1 = allocate_matrix(&m_data1);
        assert(result1 == 0);
        assert(m_data1.matrix != NULL);
        assert(**(*(m_data1.matrix + 0) + 0) == 0);
        assert(**(*(m_data1.matrix + 0) + 1) == 0);
        assert(**(*(m_data1.matrix + 1) + 0) == 0);
        assert(**(*(m_data1.matrix + 1) + 1) == 0);

        // Test case 2: Allocate a matrix of size 3x4
        matrix_data m_data2 = {
                .connection_count = malloc(sizeof(unsigned int)),
                .size = malloc(sizeof(unsigned int))
        };
        *m_data2.connection_count = 3;
        *m_data2.size = 4;
        int result2 = allocate_matrix(&m_data2);
        assert(result2 == 0);
        assert(m_data2.matrix != NULL);
        assert(**(*(m_data2.matrix + 0) + 0) == 0);
        assert(**(*(m_data2.matrix + 0) + 1) == 0);
        assert(**(*(m_data2.matrix + 0) + 2) == 0);
        assert(**(*(m_data2.matrix + 1) + 0) == 0);
        assert(**(*(m_data2.matrix + 1) + 1) == 0);
        assert(**(*(m_data2.matrix + 1) + 2) == 0);
        assert(**(*(m_data2.matrix + 2) + 0) == 0);

        printf("All tests passed successfully - allocate_connection_matrix\n");

        return 0;
}

int test_set_value_to_connection_matrix_by_input_row()
{
        matrix_data m_data = {0};
        unsigned int connection_count = 3;
        unsigned int size = 3;
        m_data.connection_count = &connection_count;
        m_data.size = &size;
        allocate_matrix(&m_data);

        // Valid input
        char input1[] = "1 2 0.8\n";
        int output = set_value_to_connection_matrix_by_input_row(&m_data, input1);
        assert(output == 0);
        assert(*(*(*(m_data.matrix + 1) + 2)) == 200000);

        // Invalid column index
        char input2[] = "5 2 0.5\n";
        assert(set_value_to_connection_matrix_by_input_row(&m_data, input2) == 3);

        // Invalid row index
        char input3[] = "1 5 0.5\n";
        assert(set_value_to_connection_matrix_by_input_row(&m_data, input3) == 3);

        // Invalid input
        char input4[] = "1 2\n";
        assert(set_value_to_connection_matrix_by_input_row(&m_data, input4) == 2);

        // Null input
        assert(set_value_to_connection_matrix_by_input_row(&m_data, NULL) == 1);

        printf("All tests passed successfully - set_value_to_connection_matrix_by_input_row\n");

        return 0;
}

int test_initialize_connection_matrix()
{
        // Test case 1: Valid input
        char input1[] = "4 6\n";
        matrix_data* m_data1 = initialize_matrix(input1);
        assert(*(m_data1->size) == 4);
        assert(*(m_data1->connection_count) == 6);

        // Test case 2: Invalid input
        char input2[] = "0 5\n";
        matrix_data* m_data2 = initialize_matrix(input2);
        assert(m_data2 == NULL);

        // Test case 3: Valid input with large numbers
        char input3[] = "1000 5000\n";
        matrix_data* m_data3 = initialize_matrix(input3);
        assert(*(m_data3->size) == 1000);
        assert(*(m_data3->connection_count) == 5000);
        // works even for at least 10 times larger numbers but takes a long time to run

        printf("All tests passed successfully - initialize_connection_matrix\n");
        return 0;
}


