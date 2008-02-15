INCLUDES         = $(all_includes) -I/usr/include/python2.4

noinst_HEADERS   = kfile_pisi.h zip.h

kde_module_LTLIBRARIES = kfile_pisi.la

kfile_pisi_la_SOURCES = kfile_pisi.cpp zip.c

kfile_pisi_la_LDFLAGS = $(all_libraries) -module $(KDE_PLUGIN)

kfile_pisi_la_LIBADD = $(LIB_KIO) -lpython2.4 -lz -liksemel

METASOURCES = AUTO

services_DATA = kfile_pisi.desktop

servicesdir = $(kde_servicesdir)

messages:
	        $(XGETTEXT) *.cpp -o $(podir)/kfile_pisi.pot
