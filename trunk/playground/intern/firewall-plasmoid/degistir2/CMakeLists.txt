# Project Needs a name ofcourse
project(kapatac)
 
# Find the required Libaries
find_package(KDE4 REQUIRED)
include(KDE4Defaults)
 
add_definitions (${QT_DEFINITIONS} ${KDE4_DEFINITIONS})
include_directories(
   ${CMAKE_SOURCE_DIR}
   ${CMAKE_BINARY_DIR}
   ${KDE4_INCLUDES}
   )
 
# We add our source code here
set(kapatac_SRCS plasma-tutorial2.cpp)
 
# Now make sure all files get to the right place
kde4_add_plugin(plasma_applet_kapatac ${kapatac_SRCS})
target_link_libraries(plasma_applet_kapatac 
                      ${KDE4_PLASMA_LIBS} ${KDE4_KDEUI_LIBS})
 
install(TARGETS plasma_applet_kapatac
        DESTINATION ${PLUGIN_INSTALL_DIR})
 
install(FILES plasma-applet-tutorial2.desktop
        DESTINATION ${SERVICES_INSTALL_DIR})