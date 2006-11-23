# Include directories
INCLUDE_DIRECTORIES(${PARDUS_SOURCE_DIR} ${QT_INCLUDE_DIR})

# Library search path
LINK_DIRECTORIES(${PARDUS_SOURCE_DIR})

# Create the library
ADD_LIBRARY(pardus SHARED string.cpp)
TARGET_LINK_LIBRARIES(pardus ${QT_LIBRARIES} "-licuuc")
SET_TARGET_PROPERTIES(pardus PROPERTIES VERSION 1.0 SOVERSION 1)

# Install
INSTALL_TARGETS(/lib pardus)
INSTALL_FILES(/include pardus.h)

