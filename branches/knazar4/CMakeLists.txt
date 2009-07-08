project(knazar)
add_definitions(-DKNAZAR_VERSION=\\"1.0\\")
find_package(KDE4 REQUIRED)
add_definitions(${KDE4_DEFINITIONS})

add_subdirectory(icons)
add_subdirectory(po)
add_subdirectory(src)
