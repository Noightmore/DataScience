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

int connection_exists(matrix_data* m_data, const unsigned int* current_vertex, const unsigned int* neighbor_index)
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

// distance node is a part of linked series of nodes
// which represent the distance from the starting vertex to the current vertex
void append_distance_node_to_vertex_distances(distance_node** neighbours_distance_list,
                                              distance_node* new_distance_node,
                                              unsigned int* distance_ptr)
{
        // set new node's values
        new_distance_node->distance = distance_ptr;
        new_distance_node->next = NULL;

        if (*neighbours_distance_list == NULL)
        {
                *neighbours_distance_list = new_distance_node;
                return;
        }

        distance_node* current_node = *neighbours_distance_list;
        while (current_node->next != NULL)
        {
                current_node = current_node->next;
        }
        current_node->next = new_distance_node;
}


int dijkstra_solver(matrix_data* m_data, const unsigned int* from_to)
{
        // LOCAL VARIABLES ---------------------------------------------------------------------------------------------

        unsigned int* visited_vertices =
                alloca(*m_data->size * sizeof(unsigned int));

        distance_node** min_distance_to_start_for_each_vertex =
                alloca(*m_data->size * sizeof(distance_node**));

        unsigned int* previous_min_vertex_for_each_vertex =
                alloca(*m_data->size * sizeof(unsigned int*));


        // initialize all the memory to NULL (stack corruption)

        memset(visited_vertices, 0, *m_data->size * sizeof(unsigned int));
        memset(min_distance_to_start_for_each_vertex, 0, *m_data->size * sizeof(distance_node**));
        memset(previous_min_vertex_for_each_vertex, 0, *m_data->size * sizeof(unsigned int*));

        // set current vertex to the starting vertex
        unsigned int current_vertex = *from_to;

        // END LOCAL VARIABLES -----------------------------------------------------------------------------------------


        // MAIN ALGORITHM LOOP
        while(current_vertex != *(from_to + 1))
        {
                // go through all neighbors of the current vertex
                for(unsigned int neighbour_i = 0; neighbour_i < *m_data->size; neighbour_i++)
                {

                        // no connection between current_vertex and vertex on the neighbour_i-th position
                        // skip this iteration
                        if(connection_exists(m_data, &current_vertex, &neighbour_i)) continue;

                        // we have already visited this vertex
                        // skip this iteration
                        if(vertex_is_already_visited(&visited_vertices, &neighbour_i)) continue;


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
                unsigned int best_vertex_distance = UINT_MAX;

                for(int neighbour_i = 0; neighbour_i < *m_data->size; neighbour_i++)
                {
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
                                // skip this iteration
                                continue;
                        }

                        // compute the total distance by distance node sequence of the current vertex
                        // TODO: add this to the previous looping of the current vertex's neighbors
                        unsigned int distance_depth = 1;
                        unsigned int total_distance = 0;

                        while(min_distance_to_start_for_each_vertex[neighbour_i] != NULL)
                        {
                                total_distance +=
                                        *min_distance_to_start_for_each_vertex[neighbour_i]->distance;

                                min_distance_to_start_for_each_vertex[neighbour_i] =
                                        min_distance_to_start_for_each_vertex[neighbour_i]->next;
                                distance_depth++;
                        }

                        if(total_distance < best_vertex_distance)
                        {
                                // vertex with the shortest distance to a starting vertex
                                current_vertex = neighbour_i;
                        }
                }

                //break;
                // go for next vertex which is the closest to the starting (the smallest edge distance value
        }

        return 0;
}
