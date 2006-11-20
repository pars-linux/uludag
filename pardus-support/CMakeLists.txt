# Project name
project(PARDUS)

# Cmake/Qt deps
cmake_minimum_required(VERSION 2.4.0)

find_package(Qt3 REQUIRED)
add_definitions(${QT_DEFINITIONS})

# Include directories
include_directories(${PARDUS_SOURCE_DIR} ${QT_INCLUDE_DIR})

# Library search path
link_directories(${PARDUS_SOURCE_DIR})

# Subdirectory
add_subdirectory(src)
