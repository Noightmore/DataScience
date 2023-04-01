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

int dijkstra_solver(matrix_data* m_data, const unsigned int* from_to)
{
        unsigned int* visited_vertices =
                alloca(*m_data->size * sizeof(unsigned int));

        distance_node** min_distance_to_start_for_each_vertex =
                alloca(*m_data->size * sizeof(distance_node**));

        unsigned int* previous_min_vertex_for_each_vertex =
                alloca(*m_data->size * sizeof(unsigned int*));


        // initialize all the memory to NULL (stack corruption)
        for(int i = 0; i < *m_data->size; i++)
        {
                visited_vertices[i] = 0;
                min_distance_to_start_for_each_vertex[i] = NULL;
                previous_min_vertex_for_each_vertex[i] = 0;
        }

        unsigned int current_vertex = *from_to;


        while(current_vertex != *(from_to + 1))
        {
                // go through all neighbors of the current vertex
                for(int neighbour_i = 0; neighbour_i < *m_data->size; neighbour_i++)
                {
                        // TODO: refactor all of this decision making into a separate function
                        if(*m_data->matrix[current_vertex][neighbour_i] == 0)
                        {
                                // no connection between current_vertex and vertex on the neighbour_i-th position
                                // skip this iteration
                                continue;
                        }

                        if(visited_vertices[neighbour_i] == 1)
                        {
                                // we have already visited this vertex
                                // skip this iteration
                                continue;
                        }

                        // if distance_node[neighbour_i] == NULL -> infinity
                        // if current vertex does not have an existing connection to the starting vertex
                        if(min_distance_to_start_for_each_vertex[neighbour_i] == NULL)
                        {
                                // allocate memory for the initial linked list node
                                min_distance_to_start_for_each_vertex[neighbour_i]
                                = alloca(sizeof(distance_node*));

                                // save the edge value
                                min_distance_to_start_for_each_vertex[neighbour_i]->distance
                                = m_data->matrix[current_vertex][neighbour_i];

                                // set next vertex to NULL
                                min_distance_to_start_for_each_vertex[neighbour_i]->next = NULL;

                                // set the previous min vertex to the current vertex
                                previous_min_vertex_for_each_vertex[neighbour_i] = current_vertex;

                                continue;
                        }

                }

                // loop through distance list and compute the total distance
                // + the distance to the current vertex

                // debug printing function
                for(int neighbour_i = 0; neighbour_i < *m_data->size; neighbour_i++)
                {
                        while(min_distance_to_start_for_each_vertex[neighbour_i] != NULL)
                        {
                                printf("distance from 0 to %d: %f\n",
                                       neighbour_i,
                                       (float) *min_distance_to_start_for_each_vertex[neighbour_i]
                                       ->distance / DIVISOR_VALUE
                                       );

                                min_distance_to_start_for_each_vertex[neighbour_i]
                                = min_distance_to_start_for_each_vertex[neighbour_i]->next;
                        }

                }

                visited_vertices[current_vertex] = 1; // mark the current vertex as visited

                // look for the best vertex to go to next

                break;
                // go for next vertex which is the closest to the starting (the smallest edge distance value
        }

        return 0;
}
