#ifndef TGHE_SEMESTRAL_DIJKSTRA_SOLVER_H
#define TGHE_SEMESTRAL_DIJKSTRA_SOLVER_H

#include <stdio.h>
#include <limits.h>
#include <string.h>

#include "matrix_tools.h"

#define DIVISOR_VALUE 1000000

typedef struct probability_distance probability_distance;

struct probability_distance
{
        unsigned int negative_outcomes_count;
        unsigned int all_outcomes_count;
};

int load_request_count_from_input_line(char* line);

int process_solution_request_line(char* line, unsigned int* from_to);

int connection_does_not_exist(matrix_data* m_data, const unsigned int* current_vertex, const unsigned int* neighbor_index);

int vertex_is_already_visited(unsigned int** visited_vertices, const unsigned int* neighbor_index);

int is_distance_to_start_infinite(probability_distance** min_distance_to_start_for_each_vertex);

void initialize_probability_distance(probability_distance** probability_dist, probability_distance* new_prob_dist);

void add_probability_distance(const unsigned int* negative_outcomes_count,
                              probability_distance** vertexes_distance_to_start);

int dijkstra_solver(matrix_data* m_data, const unsigned int* from_to);

#endif //TGHE_SEMESTRAL_DIJKSTRA_SOLVER_H
