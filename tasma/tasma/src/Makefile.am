# Copyright (c) 2004, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.

SUBDIRS = pics kfile-plugins
bin_PROGRAMS = tasma

tasma_SOURCES = main.cpp \
	tmodulegroup.cpp \
	tmodulecategorylist.cpp \
	ticonview.cpp \
	tcategoryview.cpp \
	tmoduleview.cpp \
	aboutview.cpp \
	tasmamainwin.cpp

tasma_LDADD = $(LIB_KDEUI) $(LIB_KUTILS) $(LIB_KSYCOCA)
tasma_LDFLAGS = $(all_libraries) $(KDE_RPATH)

xdg_apps_DATA = tasma.desktop

AM_CPPFLAGS = $(all_includes)
METASOURCES = AUTO

KDE_ICON=AUTO

podir=../po

COMMAND=$(XGETTEXT) --foreign-user -C -ci18n -ki18n -ktr2i18n -kI18N_NOOP -kI18N_NOOP2 -kaliasLocale
messages:
	$(COMMAND) *.cpp *.h -o $(podir)/tasma.pot

