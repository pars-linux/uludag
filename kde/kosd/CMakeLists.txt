cmake_minimum_required(VERSION 2.6)

set(kded_kosd_SRCS osd.cpp kosd.cpp)

kde4_add_plugin(kded_kosd ${kded_kosd_SRCS})

target_link_libraries(kded_kosd ${KDE4_PLASMA_LIBS})

install(TARGETS kded_kosd  DESTINATION ${PLUGIN_INSTALL_DIR})

########### install files ###############

install( FILES kosd.desktop  DESTINATION ${SERVICES_INSTALL_DIR}/kded )
install( FILES org.kde.KOSD.xml DESTINATION ${DBUS_INTERFACES_INSTALL_DIR} )
