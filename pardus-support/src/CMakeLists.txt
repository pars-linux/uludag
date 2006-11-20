# Create the library
add_library(pardus SHARED string.cpp)
target_link_libraries(pardus ${QT_LIBRARIES} "-licuuc")
SET_TARGET_PROPERTIES(pardus PROPERTIES VERSION 1.0 SOVERSION 1)

# Install
install(FILES pardus.h DESTINATION include)
install(FILES libpardus.so libpardus.so.1 libpardus.so.1.0 DESTINATION lib)

