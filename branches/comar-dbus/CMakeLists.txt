project(comar-dbus)

include_directories(include/
                    /usr/include/python2.4
                    /usr/include/dbus-1.0
                    /usr/lib/dbus-1.0/include
                    /usr/include/glib-2.0
                    /usr/lib/glib-2.0/include)

link_libraries(python2.4
               dbus-glib-1
               dbus-1
               gobject-2.0
               glib-2.0
               db)

add_executable(comar-dbus src/main.c
                          src/cfg.c
                          src/csl.c
                          src/data.c
                          src/dbus.c
                          src/iksemel.c
                          src/log.c
                          src/process.c
                          src/utility.c
                          src/xml.c)
