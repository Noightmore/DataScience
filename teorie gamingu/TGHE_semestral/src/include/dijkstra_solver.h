#ifndef TGHE_SEMESTRAL_DIJKSTRA_SOLVER_H
#define TGHE_SEMESTRAL_DIJKSTRA_SOLVER_H

#include <stdio.h>
#include <limits.h>
#include <string.h>

#include "matrix_tools.h"

#define DIVISOR_VALUE 1000000.0

typedef struct distance_node distance_node;

struct distance_node
{
        unsigned int* distance;
        distance_node* next;
};

int load_request_count_from_input_line(char* line);

int process_solution_request_line(char* line, unsigned int* from_to);

int connection_exists(matrix_data* m_data, const unsigned int* current_vertex, const unsigned int* neighbor_index);

int vertex_is_already_visited(unsigned int** visited_vertices, const unsigned int* neighbor_index);

void append_distance_node_to_vertex_distances(distance_node** neighbours_distance_list,
                                              distance_node* new_distance_node,
                                              unsigned int* distance_ptr);

int dijkstra_solver(matrix_data* m_data, const unsigned int* from_to);

#endif //TGHE_SEMESTRAL_DIJKSTRA_SOLVER_H
