bin_PROGRAMS = kaptan

kaptan_SOURCES = welcomedlg.ui welcome.cpp \
	mousesetupdlg.ui mouse.cpp \
	wallpaperdlg.ui wallpaper.cpp \
	goodbyedlg.ui goodbye.cpp \
	kaptan.cpp main.cpp

INCLUDES = $(all_includes)

kaptan_LDADD = -lkdeui
kaptan_LDFLAGS = $(all_libraries)

METASOURCES = AUTO

xdg_apps_DATA = kaptan.desktop

KDE_ICON=AUTO

kaptan_pics_data_DATA = kaptan_pardus.png kaptan.png \
	mouse_rh.png mouse_lh.png \
	kaptan_goodbye.png
kaptan_pics_datadir = $(kde_datadir)/kaptan/pics

podir=../po
COMMAND=$(XGETTEXT) --foreign-user --from-code=utf-8 -C -ci18n -ki18n -ktr2i18n -kI18N_NOOP -kI18N_NOOP2 -kaliasLocale
messages:
	$(COMMAND) *.cpp *.h -o $(podir)/kaptan.pot
