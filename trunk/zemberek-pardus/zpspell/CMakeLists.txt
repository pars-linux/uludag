
project(zpspell)

# variables for project
set(VERSION 0.3)


add_executable(zpspell zsconn.cpp
                       zstring.cpp
                       main.cpp)

install(TARGETS zpspell DESTINATION bin)

# check headers
include(CheckIncludeFile)
include(CheckIncludeFileCXX)

check_include_file_cxx(iostream     HAVE_IOSTREAM_H)
check_include_file_cxx(string       HAVE_STRING_H)
check_include_file_cxx(sstream      HAVE_SSTREAM_H)
check_include_file_cxx(vector       HAVE_VECTOR_H)
check_include_file_cxx(algorithm    HAVE_ALGORITHM_H)
check_include_file(sys/types.h  HAVE_TYPES_H)
check_include_file(sys/socket.h HAVE_SOCKET_H) 
check_include_file(netinet/in.h HAVE_NETINET_H)
check_include_file(netdb.h      HAVE_NETDB_H)


# for generated config.h
include_directories(${CMAKE_CURRENT_BINARY_DIR})

configure_file(${CMAKE_CURRENT_SOURCE_DIR}/config.h.cmake
               ${CMAKE_CURRENT_BINARY_DIR}/config.h)
