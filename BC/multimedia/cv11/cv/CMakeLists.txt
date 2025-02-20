cmake_minimum_required(VERSION 3.25)
project(cv C)

set(CMAKE_C_STANDARD 23)

set(CXXFLAGS -O3 -march=native -Wall -Werror -Wpedantic -mtune=native -fno-exceptions -mmmx -fno-rtti -fomit-frame-pointer -fno-stack-ch -lgmp)

add_executable(cv main.c main2.c bruh.c)
target_link_libraries(cv gmp)