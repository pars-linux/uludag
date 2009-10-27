SET(
  kfile_pisi_sources
  kfile_pisi.cpp
  zip.c
  )

KDE3_AUTOMOC(${kfile_pisi_sources})

KDE3_ADD_KPART(kfile_pisi ${kfile_pisi_sources})
TARGET_LINK_LIBRARIES(kfile_pisi "-lkio" "-liksemel")

INSTALL_FILES(/share/services/ FILES kfile_pisi.desktop)
INSTALL_TARGETS(/lib/kde3 kfile_pisi)
