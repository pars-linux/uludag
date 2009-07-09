set(panda_SRCS
    mainwindow.cpp
    panda.cpp 
    streamstab.cpp
    volumewidget.cpp
)

set(panda_HDRS
    mainwindow.h
    streamstab.h
    volumewidget.h
)

set(panda_UI mainwindow.ui sinkstab.ui)

qt4_wrap_ui(panda_UIC_HDRS ${panda_UI})

qt4_wrap_cpp(panda_MOC_SRCS ${panda_HDRS})
qt4_wrap_cpp(panda_MOC_SRCS ${panda_UIC_HDRS})

add_executable (panda ${panda_SRCS} ${panda_MOC_SRCS} ${panda_HDRS} ${panda_UIC_HDRS})

target_link_libraries ( panda
                        ${QT_QTCORE_LIBRARY}
                        ${QT_QTGUI_LIBRARY}
                        pulse
                        qtpulseaudiointegrator
                        qtpulseaudiobindings
                      )
