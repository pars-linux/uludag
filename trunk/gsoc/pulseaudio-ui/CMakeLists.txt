project(pulseaudio-ui)

find_package(Qt4 REQUIRED)
include( ${QT_USE_FILE} )
include( UsePkgConfig )

pkgconfig (libpulse PULSE_INCLUDE_DIR PULSE_LIB_DIR PULSE_LINK_FLAGS PULSE_CFLAGS)

add_definitions (${QT_DEFINITIONS} -O3 ${PULSE_CFLAGS} )

include_directories ( ${QT_INCLUDE_DIR} ${PULSE_INCLUDE_DIR} )

add_subdirectory(integrator)
add_subdirectory(bindings)
add_subdirectory(panda)
