#include "../include/dijkstra_solver.h"

int process_solution_request_line(char* line, unsigned int* from_to)
{

        if (sscanf(line, "%u %u", from_to, from_to + 1) != 2)
        {
                return 1; // in case of failing to read the line
        }
        return 0; // successfully read the line
}

int load_request_count_from_input_line(char* line)
{
        int request_count;
        if (sscanf(line, "%d", &request_count) != 1)
        {
                return -1; // in case of failing to read the line
        }
        return request_count; // successfully read the line
}
