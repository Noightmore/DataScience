#include "../include/test_tools.h"

void print_connection_matrix_to_stdout(matrix_data *m_data)
{
    printf("\n");
    for (int col_i = 0; col_i < *m_data->col_count; col_i++)
    {
        for (int row_i = 0; row_i < *m_data->row_count; row_i++)
        {
            if(*m_data->matrix[col_i][row_i] == 0)
            {
                printf("000000 ");
                continue;
            }
            printf("%d ", *m_data->matrix[col_i][row_i]);
        }
        printf("\n");
    }

}
