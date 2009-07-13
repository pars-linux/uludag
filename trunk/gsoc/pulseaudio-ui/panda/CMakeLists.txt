set(panda_SRCS
    mainwindow.cpp
    panda.cpp 
    streamstab.cpp
    volumewidget.cpp
    group.cpp
    groupmanager.cpp
    groupwidget.cpp
    groupstab.cpp
 )

kde4_add_ui_files(panda_SRCS mainwindow.ui)

<<<<<<< .mine
#kde4_add_kcfg_files(panda_SRCS settings.kcfgc )
=======
set(panda_UI mainwindow.ui)
>>>>>>> .r24766

kde4_add_executable(panda ${panda_SRCS})

target_link_libraries(panda ${KDE4_KDEUI_LIBS} 
                        pulse
                        qtpulseaudiointegrator
                        qtpulseaudiobindings)

install(TARGETS panda ${INSTALL_TARGETS_DEFAULT_ARGS} )


########### install files ###############

#install( FILES testapp.desktop  DESTINATION ${XDG_APPS_INSTALL_DIR} )
#install( FILES testapp.kcfg  DESTINATION  ${KCFG_INSTALL_DIR} )
#install( FILES testappui.rc  DESTINATION  ${DATA_INSTALL_DIR}/testapp )
