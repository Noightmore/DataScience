#ifndef TGHE_SEMESTRAL_DIJKSTRA_SOLVER_H
#define TGHE_SEMESTRAL_DIJKSTRA_SOLVER_H

#include <stdio.h>

#include "matrix_tools.h"

#define DIVISOR_VALUE 1000000


typedef struct distance_node
{
        unsigned int previous_vertex;
        unsigned int* distance_to_previous_vertex_value;
        unsigned int divisor_value;
        struct distance_node * next;
} distance_node;

int load_request_count_from_input_line(char* line);

int process_solution_request_line(char* line, unsigned int* from_to);

int dijkstra_solver(matrix_data* m_data, const unsigned int* from_to);

#endif //TGHE_SEMESTRAL_DIJKSTRA_SOLVER_H
