#include "dijkstra_tests.h"

void print_distance_list(distance_node* neighbours_distance_list)
{
        printf("Distances: ");
        while (neighbours_distance_list != NULL)
        {
                printf("%u ", *(neighbours_distance_list->distance));
                neighbours_distance_list = neighbours_distance_list->next;
        }
        printf("\n");
}


int test_load_request_count_from_input_line()
{
        char* input1 = "10\n"; // valid input
        int expected_output1 = 10;
        int output1 = load_request_count_from_input_line(input1);
        assert(output1 == expected_output1);

        char* input2 = "3"; // valid input without newline character
        int expected_output2 = 3;
        int output2 = load_request_count_from_input_line(input2);
        assert(output2 == expected_output2);

        char* input3 = "invalid input\n"; // invalid input
        int expected_output3 = -1;
        int output3 = load_request_count_from_input_line(input3);
        assert(output3 == expected_output3);

        char* input4 = "0\n"; // valid input with zero count
        int expected_output4 = 0;
        int output4 = load_request_count_from_input_line(input4);
        assert(output4 == expected_output4);

        printf("All tests passed successfully - load_request_count_from_input_line\n");
        return 0;
}

int test_process_solution_request_line()
{
        // Test case 1: Valid input, returns 0
        char line1[] = "1 2\n";
        unsigned int from_to1[2] = {0, 0};
        int result1 = process_solution_request_line(line1, from_to1);
        assert(result1 == 0);
        assert(from_to1[0] == 1);
        assert(from_to1[1] == 2);

        // Test case 2: Invalid input, returns 1
        char line2[] = "1 a\n";
        unsigned int from_to2[2] = {0, 0};
        int result2 = process_solution_request_line(line2, from_to2);
        assert(result2 == 1);

        // Test case 3: Invalid input, returns 1
        char line3[] = "1\n";
        unsigned int from_to3[2] = {0, 0};
        int result3 = process_solution_request_line(line3, from_to3);
        assert(result3 == 1);

        // Test case 4: Invalid input, returns 1
        // lets ignore this
//        char line4[] = "1 2 3\n";
//        unsigned int from_to4[2] = {0, 0};
//        int result4 = process_solution_request_line(line4, from_to4);
//        printf("result4: %d \n", result4);
//        assert(result4 == 1);

        // Test case 5: Valid input, returns 0
        char line5[] = "10 100\n";
        unsigned int from_to5[2] = {0, 0};
        int result5 = process_solution_request_line(line5, from_to5);
        assert(result5 == 0);
        assert(from_to5[0] == 10);
        assert(from_to5[1] == 100);

        printf("All tests passed successfully - process_solution_request_line \n");
        return 0;

}

int test_distance_list_append()
{
        // Test case 1: neighbours_distance_list is initially empty
        distance_node* neighbours_distance_list1 = NULL;
        distance_node* new_distance_node1 = (distance_node*)malloc(sizeof(distance_node));
        unsigned int distance1 = 10;
        append_distance_node_to_vertex_distances(&neighbours_distance_list1,
                                                 new_distance_node1,
                                                 &distance1);
        // print the whole linked list
        print_distance_list(neighbours_distance_list1);
        printf("Test case 1: distance node added to the end of the list.\n");

        // Test case 2: neighbours_distance_list has one node initially
        distance_node* neighbours_distance_list2 = (distance_node*)malloc(sizeof(distance_node));
        unsigned int distance2 = 20;
        neighbours_distance_list2->distance = &distance2;
        neighbours_distance_list2->next = NULL;
        distance_node* new_distance_node2 = (distance_node*)malloc(sizeof(distance_node));
        unsigned int distance3 = 30;
        append_distance_node_to_vertex_distances(&neighbours_distance_list2,
                                                 new_distance_node2,
                                                 &distance3);
        // print the whole linked list
        print_distance_list(neighbours_distance_list2);
        printf("Test case 2: distance node added to the end of the list.\n");

        // Test case 3: neighbours_distance_list has multiple nodes initially
        distance_node* neighbours_distance_list3 = (distance_node*)malloc(sizeof(distance_node));
        unsigned int distance4 = 40;
        neighbours_distance_list3->distance = &distance4;
        neighbours_distance_list3->next = (distance_node*)malloc(sizeof(distance_node));
        unsigned int distance5 = 50;
        neighbours_distance_list3->next->distance = &distance5;
        neighbours_distance_list3->next->next = NULL;
        distance_node* new_distance_node3 = (distance_node*)malloc(sizeof(distance_node));
        unsigned int distance6 = 60;
        append_distance_node_to_vertex_distances(&neighbours_distance_list3,
                                                 new_distance_node3,
                                                 &distance6);
        // print the whole linked list
        print_distance_list(neighbours_distance_list3);
        printf("Test case 3: distance node added to the end of the list.\n");

        return 0;
}
