# Copyright (c) 2004, TUBITAK/UEKAE
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Please read the COPYING file.

lib_LTLIBRARIES = libcomarrpc.la

libcomarrpc_la_SOURCES = comarxml.cpp \
	comarrpchttp.cpp \
	comarrpcunix.cpp

libcomarrpc_la_LIBADD = $(LIB_QT)
libcomarrpc_la_LDFLAGS = $(all_libraries)

AM_CPPFLAGS = $(all_includes)

comarrpcincludedir = $(includedir)/comarrpc
comarrpcinclude_HEADERS = comarrpc.h \
	comarrpchttp.h \
	comarrpcunix.h

METASOURCES = AUTO

