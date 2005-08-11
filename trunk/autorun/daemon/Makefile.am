bin_PROGRAMS = autorun

autorun_SOURCES = autorun.c config.l device.c utils.c module.c

INCLUDES = -DSYSCONF=\"$(sysconfdir)\" -DLIBDIR=\"$(pkglibdir)\" -g -Wall -I../include -DDEBUG

autorun_LDADD = -lfl -ldl

autorun_LDFLAGS = -rdynamic
