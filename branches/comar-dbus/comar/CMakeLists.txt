project(comar-dbus)

# Application name
set(APP_NAME "comar")
set(APP_SUFFIX "dbus")

# Version string
set(VERSION_MAJOR "2")
set(VERSION_MINOR "0")
set(VERSION_PATCH "0")
set(VERSION_SUFFIX "svn")

set(VERSION ${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH})
if(VERSION_SUFFIX)
   set(VERSION "${VERSION}-${VERSION_SUFFIX}")
endif(VERSION_SUFFIX)

if(APP_SUFFIX)
   set(APP_NAME "${APP_NAME}-${APP_SUFFIX}")
endif(APP_SUFFIX)

add_definitions(-D'VERSION="${VERSION}"'
                -D'CONFIG_DIR="/etc/${APP_NAME}"'
                -D'DATA_DIR="/var/db/${APP_NAME}"'
                -D'LOG_FILE="/var/log/${APP_NAME}.log"')

include_directories(include/
                    /usr/include/python2.4
                    /usr/include/dbus-1.0
                    /usr/lib/dbus-1.0/include
                    /usr/include/PolicyKit)

link_libraries(python2.4
               dbus-1
               polkit-dbus
               db)

add_executable(comar src/main.c
                     src/cfg.c
                     src/csl.c
                     src/data.c
                     src/dbus.c
                     src/iksemel.c
                     src/log.c
                     src/policy.c
                     src/process.c
                     src/pydbus.c
                     src/model.c
                     src/utility.c)

install(PROGRAMS comar
        DESTINATION /usr/bin
        RENAME ${APP_NAME})
install(FILES etc/model.xml
        DESTINATION /etc/${APP_NAME})
install(FILES
        etc/comar.conf
        DESTINATION /etc/dbus-1/system.d
        RENAME ${APP_NAME}.conf)
