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

int connection_does_not_exist(matrix_data* m_data, const unsigned int* current_vertex, const unsigned int* neighbor_index)
{
        if(*m_data->matrix[*current_vertex][*neighbor_index] == 0)
        {
                return 1; // no connection between current_vertex and vertex on the neighbour_i-th position
        }
        return 0;
}

int vertex_is_already_visited(unsigned int** visited_vertices, const unsigned int* neighbor_index)
{
        if(*visited_vertices[*neighbor_index] == 1)
        {
                return 1; // we have already visited this vertex
        }
        return 0;
}

int is_distance_to_start_infinite(probability_distance** min_distance_to_start_for_each_vertex)
{
        if(*min_distance_to_start_for_each_vertex == NULL)
        {
                return 1; // distance to start is infinite
        }
        return 0;
}

void initialize_probability_distance(probability_distance** probability_dist, probability_distance* new_prob_dist)
{
        *probability_dist = new_prob_dist;
        (*probability_dist)->negative_outcomes_count = 0;
        (*probability_dist)->all_outcomes_count = 0;
}

void add_probability_distance(const unsigned int* negative_outcomes_count,
                              probability_distance** vertexes_distance_to_start)
{
        (*vertexes_distance_to_start)->negative_outcomes_count += *negative_outcomes_count;
        (*vertexes_distance_to_start)->all_outcomes_count += DIVISOR_VALUE;
}

int dijkstra_solver(matrix_data* m_data, const unsigned int* from_to)
{
        // LOCAL VARIABLES ---------------------------------------------------------------------------------------------

        unsigned int* visited_vertices =
                alloca(*m_data->size * sizeof(unsigned int));

        unsigned int visited_vertices_count = 0;

        probability_distance** min_distance_to_start_for_each_vertex =
                alloca(*m_data->size * sizeof(probability_distance**));

        unsigned int* previous_min_vertex_for_each_vertex =
                alloca(*m_data->size * sizeof(unsigned int*));


        // initialize all the memory to NULL (stack corruption)

        memset(visited_vertices, 0, *m_data->size * sizeof(unsigned int));
        memset(min_distance_to_start_for_each_vertex, 0, *m_data->size * sizeof(probability_distance**));
        memset(previous_min_vertex_for_each_vertex, 0, *m_data->size * sizeof(unsigned int*));

        // set current vertex to the starting vertex
        unsigned int current_vertex = *from_to;

        // END LOCAL VARIABLES -----------------------------------------------------------------------------------------


        // MAIN ALGORITHM LOOP
        while(visited_vertices_count < *m_data->size)
        {
                unsigned int closest_vertex = -1;
                unsigned int closest_vertex_distance = UINT_MAX;

                // go through all neighbors of the current vertex
                for(unsigned int neighbour_index = 0; neighbour_index < *m_data->size; neighbour_index++)
                {

                        // no connection between current_vertex and vertex on the neighbour_index-th position
                        // skip this iteration
                        if(connection_does_not_exist(m_data, &current_vertex, &neighbour_index)) continue;

                        // we have already visited this vertex
                        // skip this iteration
                        if(vertex_is_already_visited(&visited_vertices, &neighbour_index)) continue;

                        if(is_distance_to_start_infinite(
                                &min_distance_to_start_for_each_vertex[neighbour_index]))
                        {
                                initialize_probability_distance(
                                        &min_distance_to_start_for_each_vertex[neighbour_index],
                                        alloca(sizeof(probability_distance)));

                                add_probability_distance(
                                        m_data->matrix[current_vertex][neighbour_index],
                                        &min_distance_to_start_for_each_vertex[neighbour_index]);
                                continue;
                        }



                        // what if there is a shorter path to the current vertexes neighbor?
                        // check if this distance is really the closest one to the starting vertex
                        // if it is, then update the distance to the starting vertex and the previous vertex
                }

                // loop through distance list and compute the total distance
                // + the distance to the current vertex

                visited_vertices[current_vertex] = 1; // mark the current vertex as visited
                visited_vertices_count++; // increment the number of visited vertices

                // print all distances
                for(unsigned int i = 0; i < *m_data->size; i++)
                {
                        if(min_distance_to_start_for_each_vertex[i] != NULL)
                        {
                                printf("Distance from %u to start (%u): %u/%u\n", i,
                                       *from_to,
                                       min_distance_to_start_for_each_vertex[i]->negative_outcomes_count,
                                       min_distance_to_start_for_each_vertex[i]->all_outcomes_count);
                        }
                }

                break;
                // go for next vertex which is the closest to the starting (the smallest edge distance value
        }

        return 0;
}
