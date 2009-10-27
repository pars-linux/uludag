project(tvManager) # the name of your project

cmake_minimum_required(VERSION 2.4.0)

#find_package(Qt4)
find_package(Qt4 REQUIRED) # find and setup Qt4 for this project
find_package(KDE4 REQUIRED)
# SET(QT_USE_QTXML 1)

# the next line sets up include and link directories and defines some variables that we will use.
# you can modify the behavior by setting some variables, e.g.
#   set(QT_USE_OPENGL TRUE)
# -> this will cause cmake to include and link against the OpenGL module
include(${QT_USE_FILE})
include (KDE4Defaults)
include_directories(
    ${KDE4_INCLUDES}
    ${KDE4_INCLUDE_DIR}
    ${QT_INCLUDE_DIR}
    ${QT_INCLUDES}
    ${QT_DEFINITIONS}
    )


# Don't forget to include output directory, otherwise
# the UI file won't be wrapped!
include_directories(${CMAKE_CURRENT_BINARY_DIR} "/usr/include/pci")
LINK_DIRECTORIES(${KDE4_LIB_DIR})

#SET(
#   tvManager_UIS
#   tvconfigui.ui
#   )

#QT4_WRAP_UI(tvManager_UIS_H ${tvManager_UIS})

# the variable "tvManager_SRCS" contains all .cpp files of this project
set(
    tvManager_SRCS
    main.cpp
    tvconfig.cpp
    tvconfigui.cpp
    tv-manager.cpp
    tuners-db.cpp
    cards-db.cpp
    )

file (GLOB tvManager_TS translations/*.ts)

qt4_add_translation(tvManager_QM ${tvManager_TS})

# tell cmake to create .moc files for all files in the variable tvManager_SRCS that require such a file.
# note: this assumes that you use #include "header.moc" in your files
qt4_automoc(${tvManager_SRCS})
# create an executable file named "tvManager" from the source files in the variable "tvManager_SRCS".
add_executable(tvManager ${tvManager_SRCS})

add_custom_target(translations_target DEPENDS ${tvManager_QM})
add_dependencies(tvManager translations_target)


# link the "tvManager" target against the Qt libraries. which libraries exactly, is defined by the "include(${QT_USE_FILE})" line above, which sets up this variable.
target_link_libraries(
    tvManager
    ${QT_LIBRARIES}
    ${KDE4_KDEUI_LIBS}
    ${KDE4_KDECORE_LIBS}
    pci
    )

#Now add these generated files to the ADD_EXECUTABLE step
# If this is NOT done, then the ui_*.h files will not be generated
##add_executable(tvManager ${tvManager_SRCS} ${tvManager_UIS_H} )
install( FILES ${tvManager_QM} DESTINATION ${QT_TRANSLATIONS_DIR} )
