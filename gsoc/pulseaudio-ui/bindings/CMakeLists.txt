set(QtPulseAudioBindings_SRCS
    context.cpp
    streammanager.cpp
    stream.cpp
    sinkmanager.cpp
    sink.cpp
    sourcemanager.cpp
    source.cpp
   )

set(QtPulseAudioBindings_HDR
    context.h       context_p.h
    streammanager.h streammanager.h
    stream.h        stream.h
    sinkmanager.h   sinkmanager.h
    sink.h          sink.h
    sourcemanager.h sourcemanager.h
    source.h        source.h
   )

qt4_wrap_cpp(QtPulseAudioBindings_MOC_SRCS ${QtPulseAudioBindings_HDR})

add_library(qtpulseaudiobindings  ${QtPulseAudioBindings_SRCS} ${QtPulseAudioBindings_MOC_SRCS} ${QtPulseAudioBindings_HDR})

target_link_libraries ( qtpulseaudiobindings
                        ${QT_QTCORE_LIBRARY}
                        pulse
                      )
