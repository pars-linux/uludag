
project(zpspell)

# variables for project
set(VERSION 0.4.1)

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



# dbus and glib stuff
include(UsePkgConfig)
pkgconfig("dbus-glib-1" _dbusIncDir _dbusLinkDir _dbusLinkFlags _dbusCflags)
pkgconfig("glib-2.0" _glibIncDir _glibLinkDir _glibLinkFlags _glibCflags)

# DBUS_INCLUDE_DIR
find_path(DBUS_INCLUDE_DIR dbus/dbus-glib.h
   ${_dbusIncDir}
   ${_dbusIncDir}/dbus-1.0
   /usr/include/dbus-1.0
   /usr/include
   /usr/local/include/dbus-1.0
   /usr/local/include
)
# DBUS_LIBRARY
find_library(DBUS_LIBRARY NAMES dbus-1
    PATHS
    ${_dbusLinkDir}
    /usr/lib
    /usr/local/lib
)

# GLIB2_INCLUDE_DIR
find_path(GLIB2_INCLUDE_DIR glib.h
   ${_glibIncDir}
   /usr/include
   /usr/include/glib-2.0
   /usr/local/include
)
# GLIB2_LIBRARY
find_library(GLIB2_LIBRARY NAMES glib-2.0
    PATHS
    ${_glibLinkDir}
    /usr/lib
    /usr/local/lib
)
# GLIB_CONFIG
find_path(GLIB_CONFIG_DIR glibconfig.h
   /usr/lib/glib-2.0/include
   /usr/lib/glib-2.0
   /usr/include/glib-2.0
   /usr/local/include
)


if(DBUS_LIBRARY AND DBUS_INCLUDE_DIR)
        message(STATUS "Found DBUS_LIBRARY: ${DBUS_LIBRARY}")
        message(STATUS "Found DBUS_INCLUDE_DIR: ${DBUS_INCLUDE_DIR}")
else(DBUS_LIBRARY AND DBUS_INCLUDE_DIR)
        message(FATAL_ERROR "Can't find DBUS")
endif(DBUS_LIBRARY AND DBUS_INCLUDE_DIR)

if(GLIB2_LIBRARY AND GLIB2_INCLUDE_DIR)
        message(STATUS "Found GLIB2_LIBRARY: ${GLIB2_LIBRARY}")
        message(STATUS "Found GLIB2_INCLUDE_DIR: ${GLIB2_INCLUDE_DIR}")
else(GLIB2_LIBRARY AND GLIB2_INCLUDE_DIR)
        message(FATAL_ERROR "Can't find DBUS")
endif(GLIB2_LIBRARY AND GLIB2_INCLUDE_DIR)


# include and link...
include_directories(${DBUS_INCLUDE_DIR})
include_directories(${GLIB2_INCLUDE_DIR})
include_directories(${GLIB_CONFIG_DIR})

target_link_libraries(zpspell glib-2.0 dbus-glib-1)

