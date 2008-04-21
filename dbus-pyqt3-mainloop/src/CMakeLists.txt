FIND_PACKAGE(Qt3 REQUIRED)
FIND_PACKAGE(PythonLibs REQUIRED)

ADD_DEFINITIONS(${QT_DEFINITIONS})
LINK_DIRECTORIES(${QT_QT_LIBRARY})
INCLUDE_DIRECTORIES(${QT_INCLUDE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR})

INCLUDE_DIRECTORIES(${QT_INCLUDE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${CMAKE_CURRENT_BINARY_DIR}
    ${PYTHON_INCLUDE_PATH}
    /usr/include/dbus-1.0
    /usr/lib/dbus-1.0/include)

SET (sources mainloop.cpp)

# we have to create moc file manually. Why? Because, QT_WRAP_CPP doesn't work
# and we don't want to use FindKDE3.cmake module's KDE3_AUTOMOC for a qt
# library
ADD_CUSTOM_TARGET(and_god_created_cmake ALL ${QT_MOC_EXECUTABLE} -o
    ${CMAKE_CURRENT_SOURCE_DIR}/mainloop.moc ${CMAKE_CURRENT_SOURCE_DIR}/mainloop.h)

ADD_LIBRARY(qt3 SHARED ${sources})

# we don't want the name 'libqt3.so'
SET_TARGET_PROPERTIES(qt3
                      PROPERTIES PREFIX ""
                      IMPORT_PREFIX "")

TARGET_LINK_LIBRARIES(qt3
                      ${QT_LIBRARIES}
                      dbus-1)

INSTALL(TARGETS qt3 DESTINATION ${CMAKE_INSTALL_PREFIX}/lib/${PYTHONVER}/site-packages/dbus/mainloop )

