


########### next target ###############

set(kcm_panda_PART_SRCS panda.cpp )


kde4_add_plugin(kcm_panda ${kcm_panda_PART_SRCS})


target_link_libraries(kcm_panda  ${KDE4_KDEUI_LIBS} ${QT_QTGUI_LIBRARY} ${X11_X11_LIB})

install(TARGETS kcm_panda  DESTINATION ${PLUGIN_INSTALL_DIR} )


########### install files ###############

install( FILES panda.desktop  DESTINATION  ${SERVICES_INSTALL_DIR} )

kde4_install_icons( ${ICON_INSTALL_DIR}  )
