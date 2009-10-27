project(kio-to-local)

find_package(KDE3 REQUIRED)

LINK_DIRECTORIES(${KDE3_LIB_DIR})
INCLUDE_DIRECTORIES(${QT_INCLUDE_DIR} ${KDE3_INCLUDE_DIR})

SET(kio-to-local_sources main.cpp)

KDE3_ADD_EXECUTABLE(kio-to-local ${kio-to-local_sources})
TARGET_LINK_LIBRARIES(kio-to-local ${QT_AND_KDECORE_LIBS} kio kdeui)

# Install
INSTALL_TARGETS(/bin kio-to-local)

