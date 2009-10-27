project(pulseaudio-ui)

find_package(KDE4 REQUIRED)
include (KDE4Defaults)

include_directories( ${KDE4_INCLUDES} ${QT_INCLUDES} )
#pkgconfig (libpulse PULSE_INCLUDE_DIR PULSE_LIB_DIR PULSE_LINK_FLAGS PULSE_CFLAGS)

#add_definitions (${QT_DEFINITIONS} -O3 ${PULSE_CFLAGS} )

#include_directories ( ${QT_INCLUDE_DIR} ${PULSE_INCLUDE_DIR} )

add_subdirectory(integrator)
add_subdirectory(bindings)
add_subdirectory(panda)
