cmake_minimum_required(VERSION 3.24)
project(TGHE_semestral C)

set(CMAKE_C_STANDARD 23)

add_executable(TGHE_semestral src/main.c src/include/matrix_tools.h src/include/general_tools.h src/libs/matrix_tools.c src/include/test_tools.h src/include/dijkstra_tools.h src/libs/test_tools.c)
