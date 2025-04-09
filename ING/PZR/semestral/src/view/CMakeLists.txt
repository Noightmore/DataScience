set(CMAKE_CXX_STANDARD 26)

set(SOURCES
        chart_plot/PlotAudio.cpp
        chart_plot/PlotAudio.hpp)

add_library(view STATIC ${SOURCES})

target_include_directories(view PUBLIC ${CMAKE_CURRENT_SOURCE_DIR})
set_target_properties(view PROPERTIES VERSION 1.0 SOVERSION 1)

find_package(Qt5 REQUIRED COMPONENTS
        Core
        Widgets
        Charts
        Gui)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

target_link_libraries(view PRIVATE
        Qt5::Core
        Qt5::Widgets
        Qt5::Charts
        Qt5::Gui)