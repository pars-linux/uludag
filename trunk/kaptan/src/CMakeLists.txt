ADD_DEFINITIONS(${QT_DEFINITIONS} ${KDE3_DEFINITIONS})
LINK_DIRECTORIES(${KDE3_LIB_DIR})
INCLUDE_DIRECTORIES(${KDE3_INCLUDE_DIR} ${QT_INCLUDE_DIR} ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR})

SET(
  kaptan_sources
  welcome.cpp
  mouse.cpp
  wallpaper.cpp
  goodbye.cpp
  kaptan.cpp
  main.cpp
  )

KDE3_AUTOMOC(${kaptan_sources})

SET(
  kaptan_ui
  welcomedlg.ui
  mousesetupdlg.ui
  wallpaperdlg.ui
  goodbyedlg.ui
  )

KDE3_ADD_UI_FILES(kaptan_sources ${kaptan_ui})

KDE3_ADD_EXECUTABLE(kaptan ${kaptan_sources})
TARGET_LINK_LIBRARIES(kaptan ${QT_AND_KDECORE_LIBS} kdeui)

INSTALL_TARGETS(/bin kaptan)
INSTALL_FILES(/share/applications/kde FILES kaptan.desktop)
INSTALL_FILES(/share/apps/kaptan/pics FILES kaptan_pardus.png kaptan.png mouse_rh.png mouse_lh.png kaptan_goodbye.png)
