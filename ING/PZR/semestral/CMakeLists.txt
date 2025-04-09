cmake_minimum_required(VERSION 3.30)
project(semestral)

set(CMAKE_CXX_STANDARD 23)

set(SRC ./src/)
set(STACK_SIZE 3221225472) # 3GB stack size

add_subdirectory(${SRC}lib)
add_subdirectory(${SRC}view)

set(SOURCE_FILES ${SRC}main.cpp)

enable_language(ASM_NASM)
set(NASM_COMPILER nasm)

set(CXXFLAGS -O3 -march=native -Wall -Werror -Wpedantic -mtune=native -fno-exceptions -mmmx
        -fno-rtti -fomit-frame-pointer -fno-stack-ch -lQt5Widgets -lQt5Core ) # -lQt5Charts

# required config for nasm
set(CMAKE_ASM_NASM_OBJECT_FORMAT elf64)
set(CMAKE_ASM_NASM_COMPILE_OBJECT
        "<CMAKE_ASM_NASM_COMPILER> <INCLUDES> <FLAGS> -f ${CMAKE_ASM_NASM_OBJECT_FORMAT}  -o <OBJECT> <SOURCE>")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -no-pie")

add_executable(semestral ${SRC}main.cpp)

set_target_properties(semestral PROPERTIES
        LINK_FLAGS "-Wl,-z,stack-size=${STACK_SIZE}"
)

find_package(Qt5 REQUIRED COMPONENTS
        Core
        Widgets
        Charts
        Gui)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

target_link_libraries(semestral PRIVATE
        lib
        view
        sndfile
        Qt5::Core
        Qt5::Widgets
        Qt5::Charts
        Qt5::Gui)