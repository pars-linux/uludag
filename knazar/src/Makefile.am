# set the include path for X, qt and KDE
INCLUDES = $(all_includes)

# let automoc handle all of the meta source files (moc)
METASOURCES = AUTO

podir=../po
messages:
	$(XGETTEXT) --foreign-user -C -ci18n -ki18n -ktr2i18n -kI18N_NOOP -kI18N_NOOP2 -kaliasLocale *.cpp -o $(podir)/knazar.pot

KDE_ICON = knazar

#########################################################################
# APPLICATION SECTION
#########################################################################
# this is the program that gets installed.  it's name is used for all
# of the other Makefile.am variables
bin_PROGRAMS = knazar

# the application source, library search path, and link libraries
knazar_SOURCES = main.cpp knazar.cpp knazarballoon.cpp knazardcop.skel
knazar_LDFLAGS = $(KDE_RPATH) $(all_libraries)
knazar_LDADD = $(LIB_KDEUI) $(LIB_QT) $(LIB_KDECORE) $(LIBSOCKET)

# this is where the desktop file will go 
shelldesktopdir   = $(kde_appsdir)/Utilities
shelldesktop_DATA = knazar.desktop

