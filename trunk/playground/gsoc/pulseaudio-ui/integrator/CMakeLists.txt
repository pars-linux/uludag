set(QtPulseAudioIntegrator_SRCS
    QtPulseAudioIntegrator.cpp
    QtPulseAudioIOEvent.cpp
    QtPulseAudioTimeEvent.cpp
    QtPulseAudioDeferEvent.cpp
   )

set(QtPulseAudioIntegrator_HDR
    QtPulseAudioIntegrator.h
    QtPulseAudioIOEvent_p.h
    QtPulseAudioTimeEvent_p.h
    QtPulseAudioDeferEvent_p.h
   )

qt4_wrap_cpp(QtPulseAudioIntegrator_MOC_SRCS ${QtPulseAudioIntegrator_HDR})

add_library(qtpulseaudiointegrator  ${QtPulseAudioIntegrator_SRCS} ${QtPulseAudioIntegrator_MOC_SRCS} ${QtPulseAudioIntegrator_HDR})

target_link_libraries ( qtpulseaudiointegrator
                        ${QT_QTCORE_LIBRARY}
                        pulse
                      )
