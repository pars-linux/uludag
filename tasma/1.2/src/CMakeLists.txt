ADD_DEFINITIONS(${QT_DEFINITIONS} ${KDE3_DEFINITIONS})
LINK_DIRECTORIES(${KDE3_LIB_DIR})
INCLUDE_DIRECTORIES(${KDE3_INCLUDE_DIR} ${QT_INCLUDE_DIR} ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR})

ADD_SUBDIRECTORY(pics)
ADD_SUBDIRECTORY(kfile-plugins)


SET(
  tasma_sources
  main.cpp
  tmodulegroup.cpp
  tmodulecategorylist.cpp
  ticonview.cpp
  tcategoryview.cpp
  tmoduleview.cpp
  aboutview.cpp
  tasmamainwin.cpp
  tlistviewtooltip.cpp
)

KDE3_AUTOMOC(${tasma_sources})

KDE3_ADD_EXECUTABLE(tasma ${tasma_sources})
TARGET_LINK_LIBRARIES(tasma ${QT_QT_LIBRARY} kdecore kdeui kutils)

INSTALL(TARGETS tasma DESTINATION bin)
INSTALL(FILES tasma.desktop DESTINATION share/applications/kde)
INSTALL(FILES tasmaui.rc DESTINATION share/apps/tasma)
INSTALL(FILES ../docs/index.html DESTINATION share/doc/HTML/tr/tasma)

KDE3_INSTALL_ICONS(hicolor)

