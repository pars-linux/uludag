# Project name
project(PARDUS)

# Cmake/Qt deps
cmake_minimum_required(VERSION 2.4.0)

find_package(Qt3 REQUIRED)
add_definitions(${QT_DEFINITIONS})

# Include directories
include_directories(${QT_INCLUDE_DIR})

# Library search path
link_directories(${PARDUS_SOURCE_DIR})

# Create the library
add_library(pardus SHARED string.cpp)
target_link_libraries(pardus ${QT_LIBRARIES} "-licuuc")
SET_TARGET_PROPERTIES(pardus PROPERTIES VERSION 1.0 SOVERSION 1)

# Install
install(FILES pardus.h DESTINATION include)
install(FILES libpardus.so libpardus.so.1 libpardus.so.1.0 DESTINATION lib)
