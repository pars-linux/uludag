ADD_SUBDIRECTORY(desktop)

SET(
  directory_files
  tasma.directory
  tasma-desktop.directory
  tasma-localization.directory
  tasma-looknfeel.directory
  tasma-network.directory
  tasma-peripherals.directory
  tasma-sound.directory
  tasma-useraccount.directory
  tasma-system.directory
  )

INSTALL_FILES(/etc/xdg/menus/  FILES kde-settings.menu)
INSTALL_FILES(/share/desktop-directories/ FILES ${directory_files})
