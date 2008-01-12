PROJECT (PolicyKit-kde)

# use FindKDE3 module of cmake for KDE specific operations
FIND_PACKAGE(KDE3 REQUIRED)

# add definitions, library directories and header directories for KDE and QT
ADD_DEFINITIONS(${QT_DEFINITIONS} ${KDE3_DEFINITIONS})

LINK_DIRECTORIES(${KDE3_LIB_DIR} dbus-qt3-backport)

INCLUDE_DIRECTORIES(${KDE3_INCLUDE_DIR} ${QT_INCLUDE_DIR}
    ${CMAKE_CURRENT_SOURCE_DIR} ${CMAKE_CURRENT_BINARY_DIR}
    /usr/include/dbus-1.0/qt3 /usr/include/dbus-1.0 /usr/lib/dbus-1.0/include
    ${CMAKE_SOURCE_DIR}/dbus-qt3-backport
    ${CMAKE_SOURCE_DIR}/dbus-qt3-backport/dbus)

# specify sources
SET (
    sources
    authdialog.cpp
    policykitkde.cpp
    service.cpp
    main.cpp
    )

# moc files will be created automatically
KDE3_AUTOMOC(${sources})

# generate code from ui file
KDE3_ADD_UI_FILES(sources authdialogui.ui)

# build executable named policykit-kde
KDE3_ADD_EXECUTABLE(policykit-kde ${sources})

# link executabel with kde libraries
TARGET_LINK_LIBRARIES(policykit-kde ${QT_AND_KDECORE_LIBS} kdeui dbus-1 dbus-1-qt3)
