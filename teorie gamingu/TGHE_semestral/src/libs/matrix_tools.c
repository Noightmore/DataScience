#include "../include/matrix_tools.h"

#include "../include/test_tools.h"

unsigned int *load_matrix_dims()
{
    char buffer[BUFFER_SIZE];
    unsigned int *dims = malloc(2 * sizeof(unsigned int));
    
    if(fgets(buffer, BUFFER_SIZE, stdin) == NULL)
    {
        return NULL;
    }
    sscanf(buffer, "%d %d", dims, (dims + 1));

    return dims;
}

unsigned int *load_input_data_row()
{
    char buffer[BUFFER_SIZE];
    float probability;
    unsigned int *row_data = malloc(3 * sizeof(unsigned int));

    if(fgets(buffer, BUFFER_SIZE, stdin) == NULL)
    {
        return NULL;
    }
    sscanf(buffer, "%d %d %f", row_data, (row_data + 1), &probability);

    //printf("%d",(unsigned int) (probability*1000000));
    // parse the data to the appropriate format
    *(row_data + 2) = 1000000 - (unsigned int) (probability*1000000);

    return row_data;
}

matrix_data *initialize_matrix()
{
    // col count = number of vertices
    // row count = number of edges
    matrix_data* m_data = malloc(sizeof(matrix_data));
    unsigned int *dims = load_matrix_dims();
    m_data->col_count = dims;
    m_data->row_count = (dims + 1);

    allocate_matrix(m_data);
    fill_connection_matrix(m_data);

    return m_data;
}

int allocate_matrix(matrix_data *m_data)
{
    m_data->matrix = malloc(*m_data->col_count * sizeof(unsigned int***));

    for (int col_i = 0; col_i < *m_data->col_count; col_i++)
    {
        *(m_data->matrix + col_i) = malloc(*m_data->row_count * sizeof(unsigned int**));
        for (int row_i = 0; row_i < *m_data->row_count; row_i++)
        {
            *(*(m_data->matrix + col_i) + row_i) = malloc(sizeof(unsigned int*));
            **(*(m_data->matrix + col_i) + row_i) = 0;
        }
    }

    if(m_data->matrix == NULL)
    {
        return 1;
    }
    return 0;
}

int fill_connection_matrix(matrix_data *m_data)
{
    // read user input - do a separate function for this
    unsigned int *buffer;

    for(int row_i = 0; row_i < *m_data->row_count; row_i++)
    {
        buffer = load_input_data_row();
        // matrix[data_col_id][data_row_id] = (formatted probability)
        *(*(m_data->matrix + *buffer) + *(buffer+1)) = (buffer + 2); // very readable code
    }

    return 0;
}


