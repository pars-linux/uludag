include_directories(${KDE4_INCLUDES})

set(knazar_SRCS
main.cpp
knazar.cpp
)
qt4_add_dbus_adaptor(knazar_SRCS tr.org.pardus.knazar.xml knazar.h Knazar)

kde4_add_executable(knazar ${knazar_SRCS})
target_link_libraries(knazar ${KDE4_KDEUI_LIBS})

install(PROGRAMS knazar DESTINATION ${BIN_INSTALL_DIR})
install(FILES knazar.desktop DESTINATION ${XDG_APPS_INSTALL_DIR})
