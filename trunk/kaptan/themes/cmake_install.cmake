# Install script for directory: /home/caglar/buildbox/kaptan/themes

# Set the install prefix
IF(NOT DEFINED CMAKE_INSTALL_PREFIX)
  SET(CMAKE_INSTALL_PREFIX "/usr/kde/3.5")
ENDIF(NOT DEFINED CMAKE_INSTALL_PREFIX)
STRING(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
IF(NOT CMAKE_INSTALL_CONFIG_NAME)
  IF(BUILD_TYPE)
    STRING(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  ELSE(BUILD_TYPE)
    SET(CMAKE_INSTALL_CONFIG_NAME "")
  ENDIF(BUILD_TYPE)
  MESSAGE(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
ENDIF(NOT CMAKE_INSTALL_CONFIG_NAME)

# Set the component getting installed.
IF(NOT CMAKE_INSTALL_COMPONENT)
  IF(COMPONENT)
    MESSAGE(STATUS "Install component: \"${COMPONENT}\"")
    SET(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  ELSE(COMPONENT)
    SET(CMAKE_INSTALL_COMPONENT)
  ENDIF(COMPONENT)
ENDIF(NOT CMAKE_INSTALL_COMPONENT)

FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apps/kaptan/themes/KDE" TYPE FILE FILES "/home/caglar/buildbox/kaptan/themes/KDE.preview.png")
FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apps/kaptan/themes/KDE" TYPE FILE FILES "/home/caglar/buildbox/kaptan/themes/KDE.xml")
FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apps/kaptan/themes/KDE_Classic" TYPE FILE FILES "/home/caglar/buildbox/kaptan/themes/KDE_Classic.preview.png")
FILE(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/apps/kaptan/themes/KDE_Classic" TYPE FILE FILES "/home/caglar/buildbox/kaptan/themes/KDE_Classic.xml")
