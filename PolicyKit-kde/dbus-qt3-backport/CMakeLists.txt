FIND_PACKAGE(Qt3 REQUIRED)

ADD_DEFINITIONS(${QT_DEFINITIONS})
LINK_DIRECTORIES(${QT_QT_LIBRARY})
INCLUDE_DIRECTORIES(${QT_INCLUDE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}
    /usr/include/dbus-1.0/qt3 /usr/include/dbus-1.0 /usr/lib/dbus-1.0/include
    ${CMAKE_CURRENT_SOURCE_DIR}/dbus)

SET (
    dbus_sources
    qdbusconnection.cpp
    qdbuserror.cpp
    qdbusintegrator.cpp
    qdbusmarshall.cpp
    qdbusmessage.cpp
    qdbusproxy.cpp
    qdbusserver.cpp
    )

SET ( mocs qdbusserver.moc qdbusconnection.moc qdbusproxy.moc )

ADD_CUSTOM_COMMAND(
    OUTPUT ${mocs}
    COMMAND ${QT_MOC_EXECUTABLE} ARGS -o qdbusserver.moc ${CMAKE_CURRENT_SOURCE_DIR}/dbus/qdbusserver.h
    COMMAND ${QT_MOC_EXECUTABLE} ARGS -o qdbusconnection.moc ${CMAKE_CURRENT_SOURCE_DIR}/qdbusconnection_p.h
    COMMAND ${QT_MOC_EXECUTABLE} ARGS -o qdbusproxy.moc ${CMAKE_CURRENT_SOURCE_DIR}/dbus/qdbusproxy.h
    )

ADD_CUSTOM_TARGET(moc_target ALL DEPENDS ${mocs})

ADD_LIBRARY(dbus-1-qt3 SHARED ${dbus_sources})

ADD_DEPENDENCIES(dbus-1-qt3 moc_target)

TARGET_LINK_LIBRARIES(dbus-1-qt3 ${QT_LIBRARIES} dbus-1)

