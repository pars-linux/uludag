INCLUDE_DIRECTORIES( ${KDE3_INCLUDE_DIR} ${QT_INCLUDE_DIR} ${CMAKE_CURRENT_SOURCE_DIR} "/usr/include/pci")
LINK_DIRECTORIES(${KDE3_LIB_DIR})

SET(
  tasmatv_sources
  tasmatv.cpp
  tvconfig.cpp
  cards-db.cpp
  tuners-db.cpp
  )

KDE3_AUTOMOC(${tasmatv_sources})

KDE3_ADD_UI_FILES(tasmatv_sources tvconfigui.ui)

KDE3_ADD_KPART(kcm_tasmatv ${tasmatv_sources})
TARGET_LINK_LIBRARIES(kcm_tasmatv ${QT_AND_KDECORE_LIBS} kdeui pci)

INSTALL_TARGETS(/lib/kde3 kcm_tasmatv)
INSTALL_FILES(/share/applications/kde/ tasmatv.desktop)
