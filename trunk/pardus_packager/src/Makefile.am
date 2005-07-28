SUBDIRS = .

METASOURCES = AUTO

bin_PROGRAMS = pardus_packager

pardus_packager_SOURCES = main.cpp packagerui.cpp packagemanager.ui pisimanager.cpp threadrunner.cpp htmlwriter.cpp

pardus_packager_LDADD = $(LIB_KDECORE) $(LIB_KHTML)
pardus_packager_LDFLAGS = $(all_libraries) $(KDE_RPATH)

INCLUDES = $(all_includes)

