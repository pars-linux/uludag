set(QtPulseAudioBindings_SRCS
    QtPulseAudioContext.cpp
    QtPulseAudioStreamManager.cpp
    QtPulseAudioStream.cpp
    QtPulseAudioSinkManager.cpp
    QtPulseAudioSink.cpp
    QtPulseAudioSourceManager.cpp
    QtPulseAudioSource.cpp
   )

set(QtPulseAudioBindings_HDR
    QtPulseAudioContext.h       QtPulseAudioContext_p.h
    QtPulseAudioStreamManager.h QtPulseAudioStreamManager_p.h
    QtPulseAudioStream.h        QtPulseAudioStream_p.h
    QtPulseAudioSinkManager.h   QtPulseAudioSinkManager_p.h
    QtPulseAudioSink.h          QtPulseAudioSink_p.h
    QtPulseAudioSourceManager.h QtPulseAudioSourceManager_p.h
    QtPulseAudioSource.h        QtPulseAudioSource_p.h
   )

qt4_wrap_cpp(QtPulseAudioBindings_MOC_SRCS ${QtPulseAudioBindings_HDR})

add_library(qtpulseaudiobindings  ${QtPulseAudioBindings_SRCS} ${QtPulseAudioBindings_MOC_SRCS} ${QtPulseAudioBindings_HDR})

target_link_libraries ( qtpulseaudiobindings
                        ${QT_QTCORE_LIBRARY}
                        pulse
                      )
