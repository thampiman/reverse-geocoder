cmake_minimum_required(VERSION 2.8)
project(reverse_geocode)
find_package(Python 3.8 REQUIRED COMPONENTS Interpreter Development.Module)

include_directories(${PYTHON_INCLUDE_DIRS} lib)
add_definitions(-g -std=c++0x -Wall -Wextra -Wattributes)


FILE(GLOB LIB_SRC "./lib/*.cpp")

ADD_LIBRARY( reverse_geocode STATIC ${LIB_SRC} )
TARGET_LINK_LIBRARIES(reverse_geocode ${PYTHON_LIBRARIES} ${MORE_PYTHON_FLAGS})


#FILE(GLOB CURRENT_SRC "./*.cpp")

#ADD_EXECUTABLE( main ${CURRENT_SRC} )
#TARGET_LINK_LIBRARIES(main reverse_geocode)
