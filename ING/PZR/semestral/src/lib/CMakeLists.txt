set(CMAKE_CXX_STANDARD 26)

set(TUL_LIB_DECLARATION TulAudioLib.hpp)

set(SOURCES ${TUL_LIB_DECLARATION} audio_xtraction/detect_word_boundaries.c
        audio_xtraction/helper_funcs.c)
add_library(lib STATIC ${SOURCES})

target_include_directories(lib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
set_target_properties(lib PROPERTIES VERSION 1.0 SOVERSION 1)