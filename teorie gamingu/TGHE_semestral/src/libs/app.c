#include "../include/app.h"

void print_connection_matrix_to_stdout(matrix_data *m_data)
{
        printf("\n");
        for (int col_i = 0; col_i < *m_data->size; col_i++)
        {
                for (int row_i = 0; row_i < *m_data->size; row_i++)
                {
                        if (*m_data->matrix[col_i][row_i] == 0)
                        {
                                printf("000000 ");
                                continue;
                        }
                        printf("%d ", *m_data->matrix[col_i][row_i]);
                }
                printf("\n");
        }
}

int app_run()
{
        char* buffer = alloca(BUFFER_SIZE);

        matrix_data *m_data =
                initialize_matrix(fgets(buffer, BUFFER_SIZE, stdin));

        //*buffer ^= *buffer; // flush buffer
        //printf("%d %d", *m_data->size, *m_data->connection_count);

        // fill the matrix with data from stdin
        for (int i = 0; i < *m_data->connection_count; i++)
        {
                set_value_to_connection_matrix_by_input_row(
                        m_data, fgets(buffer, BUFFER_SIZE, stdin));
                //*buffer ^= *buffer; // flush buffer
        }

        print_connection_matrix_to_stdout(m_data);



        return 0;
}

