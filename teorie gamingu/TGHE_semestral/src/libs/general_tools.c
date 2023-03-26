#include "../include/general_tools.h"

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