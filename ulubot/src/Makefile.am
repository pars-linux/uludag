##
## Process this file with automake to produce Makefile.in
##

INCLUDES = -I$(top_srcdir)/include -I$(top_builddir)/include

bin_PROGRAMS = ulubot

ulubot_CFLAGS = $(CFLAGS) $(IKSEMEL_CFLAGS)
ulubot_LDADD = $(IKSEMEL_LIBS)

ulubot_SOURCES = \
	main.c \
	jabber.c \
	dict.c \
	command.c \
	import.c \
	prefs.c
