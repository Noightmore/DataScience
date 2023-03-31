#include "../include/matrix_tools.h"

unsigned int *load_matrix_dims_from_input(char* input)
{
        unsigned int *dims = sbrk(2 * sizeof(unsigned int));

        if (sscanf(input, "%u %u", dims, dims + 1) != 2)
        {
                return NULL; // not freeing memory as the program will crash anyway
        }

        return dims;
}

unsigned int *load_input_data_row(char* input, unsigned int* coords)
{
        float probability;
        unsigned int *row_data = sbrk(sizeof(unsigned int));

        if(sscanf(input, "%d %d %f", coords, (coords + 1), &probability) != 3)
        {
                return NULL; // not freeing memory as the program will crash anyway
        }

        // TODO: remove this for code critic test
        if(probability < 0 || probability > 1)
        {
                return NULL; // not freeing memory as the program will crash anyway
        }

        //printf("%d",(unsigned int) (probability*1000000));
        // parse the data to the appropriate format
        *(row_data) = 1000000 - (unsigned int) (probability*1000000);

        return row_data;
}


matrix_data *initialize_matrix(char* input)
{
        // col count = number of vertices
        // row count = number of edges
        matrix_data* m_data = sbrk(sizeof(matrix_data));
        unsigned int *dims = load_matrix_dims_from_input(input);

        m_data->size = dims;
        m_data->connection_count = (dims + 1);

        // TODO: remove this for code critic test
        if(m_data->size == NULL || m_data->connection_count == NULL)
        {
                return NULL;
        }

        // TODO: remove this for code critic test
        if(*m_data->size <= 0 || *m_data->connection_count <= 0)
        {
                return NULL;
        }

        allocate_matrix(m_data);
        //set_value_to_connection_matrix_by_input_row(m_data);

        return m_data;
}

int allocate_matrix(matrix_data *m_data)
{
        m_data->matrix = sbrk(*m_data->size * sizeof(unsigned int***));

        for (int col_i = 0; col_i < *m_data->size; col_i++)
        {
                *(m_data->matrix + col_i) = sbrk(*m_data->size * sizeof(unsigned int**));
                for (int row_i = 0; row_i < *m_data->size; row_i++)
                {
                        *(*(m_data->matrix + col_i) + row_i) = sbrk(sizeof(unsigned int*));
                        //**(*(m_data->matrix + col_i) + row_i) = 0;
                }
        }

        // TODO: remove this for code critic test
        if(m_data->matrix == NULL)
        {
                return 1;
        }
        return 0;
}


int set_value_to_connection_matrix_by_input_row(matrix_data *m_data, char* input)
{
        // read user input - do a separate function for this
        unsigned int *buffer;
        unsigned int* coords = alloca(2 * sizeof(unsigned int));

        // TODO: remove this for code critic test
        if (input == NULL)
        {
                return 1;
        }

        buffer = load_input_data_row(input, coords);

        // TODO: remove this for code critic test
        if(buffer == NULL)
        {
                return 2;
        }

        // TODO: remove this for code critic test
        // Check if the row and column indices are within the valid range of the matrix
        if (*coords >= *m_data->size || *(coords + 1) >= *m_data->size)
        {
                return 3;  // Invalid indices, return error code
        }

        // explanation:
        // matrix[data_col_id][data_row_id] = matrix[data_row_id][data_col_id] = (formatted probability)
        *(*(m_data->matrix + *coords) + *(coords + 1)) = (buffer); // very readable code
        *(*(m_data->matrix + *(coords + 1)) + *(coords)) = (buffer); // very readable code

        return 0;
}
