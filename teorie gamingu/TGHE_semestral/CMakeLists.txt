cmake_minimum_required(VERSION 3.24)
project(TGHE_semestral C)

set(CMAKE_C_STANDARD 23)

add_executable(TGHE_semestral src/main.c src/include/general_tools.h src/libs/general_tools.c src/unit_tests/matrix_tests.h src/unit_tests/matrix_tests.c src/include/matrix_tools.h src/libs/matrix_tools.c src/unit_tests/tester.h src/unit_tests/tester.c src/include/most_reliable_way_finding_app.h src/libs/most_reliable_way_finding_app.c)
