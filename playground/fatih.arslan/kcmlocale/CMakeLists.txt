
add_subdirectory( pics )

########### next target ###############

set(kcm_locale_PART_SRCS kcmlocale.cpp)

kde4_add_ui_files(kcm_locale_PART_SRCS kcmlocalewidget.ui )

kde4_add_plugin(kcm_locale ${kcm_locale_PART_SRCS})

target_link_libraries(kcm_locale ${KDE4_KIO_LIBS} ${QT_QTGUI_LIBRARY} )

install(TARGETS kcm_locale  DESTINATION ${PLUGIN_INSTALL_DIR} )

#### KAuth helper and actions ####
kde4_add_executable(kcmlocalehelper helper.cpp)
target_link_libraries(kcmlocalehelper ${KDE4_KDECORE_LIBS})
install(TARGETS kcmlocalehelper DESTINATION ${LIBEXEC_INSTALL_DIR})

kde4_install_auth_helper_files(kcmlocalehelper org.kde.kcontrol.kcmlocale root)

kde4_install_auth_actions(org.kde.kcontrol.kcmlocale kcmlocale.actions)

########### install files ###############

install( FILES language.desktop  DESTINATION  ${SERVICES_INSTALL_DIR} )

