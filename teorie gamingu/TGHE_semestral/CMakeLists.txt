cmake_minimum_required(VERSION 3.24)
project(TGHE_semestral C)

set(CMAKE_C_STANDARD 23)

add_executable(TGHE_semestral
        src/main.c
        src/unit_tests/matrix_tests.h
        src/unit_tests/matrix_tests.c
        src/include/matrix_tools.h
        src/libs/matrix_tools.c
        src/unit_tests/tester.h
        src/unit_tests/tester.c
        src/include/app.h
        src/libs/app.c
        src/include/dijkstra_solver.h src/libs/dijkstra_solver.c)
