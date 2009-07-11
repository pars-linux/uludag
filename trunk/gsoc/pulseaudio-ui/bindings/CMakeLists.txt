set(QtPulseAudioBindings_SRCS
    context.cpp
    streammanager.cpp
    stream.cpp
    device.cpp
    sinkmanager.cpp
    sink.cpp
    sourcemanager.cpp
    source.cpp
   )

set(QtPulseAudioBindings_HDR
    context.h       context_p.h
    streammanager.h streammanager_p.h
    stream.h        stream_p.h
    device.h        device_p.h
    sinkmanager.h   #sinkmanager_p.h
    sink.h          sink_p.h
    sourcemanager.h #sourcemanager_p.h
    source.h        source_p.h
   )

qt4_wrap_cpp(QtPulseAudioBindings_MOC_SRCS ${QtPulseAudioBindings_HDR})

add_library(qtpulseaudiobindings  ${QtPulseAudioBindings_SRCS} ${QtPulseAudioBindings_MOC_SRCS} ${QtPulseAudioBindings_HDR})

target_link_libraries ( qtpulseaudiobindings
                        ${QT_QTCORE_LIBRARY}
                        pulse
                      )
