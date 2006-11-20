# Project name
project(PARDUS)

# Cmake/Qt deps
cmake_minimum_required(VERSION 2.4.0)

find_package(Qt3 REQUIRED)
add_definitions(${QT_DEFINITIONS})

# Subdirectory
add_subdirectory(src)
