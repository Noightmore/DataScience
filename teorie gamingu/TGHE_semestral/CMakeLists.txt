cmake_minimum_required(VERSION 3.24)
project(TGHE_semestral C)

set(CMAKE_C_STANDARD 23)

add_executable(TGHE_semestral src/main.c src/include/general_tools.h src/include/dijkstra_tools.h src/libs/general_tools.c src/include/dictionary.h src/libs/dictionary.c src/unit_tests/basic_tests.h src/unit_tests/basic_tests.c)
