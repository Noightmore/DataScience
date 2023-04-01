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
        unsigned int* visited_vertices = alloca(*m_data->size * sizeof(unsigned int));

        // visited_vertices[*from_to] = 1; // mark the starting vertex as visited

        unsigned int current_vertex = *from_to;

        distance_node* distance_list = NULL;

        while(current_vertex != *(from_to + 1))
        {
                // go through all neighbors of the current vertex
                for(int i = 0; i < *m_data->size; i++)
                {
                        // TODO: refactor all of this decision making into a separate function
                        if(*m_data->matrix[current_vertex][i] == 0)
                        {
                                // no connection between current_vertex and vertex on the i-th position
                                // skip this iteration
                                continue;
                        }

                        if(visited_vertices[i] == 1)
                        {
                                // we have already visited this vertex
                                // skip this iteration
                                continue;
                        }

                        // we are at the start
                        if(distance_list == NULL)
                        {
                                distance_list = alloca(sizeof(distance_node));
                                distance_list->previous_vertex = current_vertex;
                                distance_list->distance_to_previous_vertex_value = NULL;
                                distance_list->divisor_value = DIVISOR_VALUE;

                                distance_list->next = NULL;
                        }
                        // we have already added a record of a distance -> adding another one
                        else
                        {
                                distance_list->next = alloca(sizeof(distance_node));
                                distance_list = distance_list->next;
                                distance_list->previous_vertex = current_vertex;
                                distance_list->distance_to_previous_vertex_value = NULL;
                                distance_list->divisor_value = DIVISOR_VALUE;

                                distance_list->next = NULL;
                        }

                        // loop through distance list and compute the total distance
                        // + the distance to the current vertex






                }

                visited_vertices[current_vertex] = 1;
        }

        return 0;
}
