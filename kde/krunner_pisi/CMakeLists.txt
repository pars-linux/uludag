set(krunner_pisi_SRCS
    pisirunner.cpp
)

find_package(KDE4 REQUIRED)
include(KDE4Defaults)
add_definitions(${KDE4_DEFINITIONS})
include_directories(${KDE4_INCLUDES})

kde4_add_plugin(krunner_pisi ${krunner_pisi_SRCS})
target_link_libraries(krunner_pisi ${KDE4_KIO_LIBS} ${KDE4_PLASMA_LIBS})

########### install files ###############

install(TARGETS krunner_pisi DESTINATION ${PLUGIN_INSTALL_DIR})
install(FILES plasma-runner-pisi.desktop DESTINATION ${SERVICES_INSTALL_DIR})

