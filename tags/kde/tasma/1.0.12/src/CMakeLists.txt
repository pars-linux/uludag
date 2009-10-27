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
)

KDE3_AUTOMOC(${tasma_sources})

KDE3_ADD_EXECUTABLE(tasma ${tasma_sources})
TARGET_LINK_LIBRARIES(tasma ${QT_AND_KDECORE_LIBS} kdeui kutils)

INSTALL_TARGETS(/bin tasma)
INSTALL_FILES(/share/applications/kde FILES tasma.desktop)
INSTALL_FILES(/share/apps/tasma FILES tasmaui.rc)

KDE3_INSTALL_ICONS(hicolor)

