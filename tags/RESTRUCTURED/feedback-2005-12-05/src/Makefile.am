bin_PROGRAMS = feedback

feedback_SOURCES = welcomedlg.ui welcome.cpp \
	experiencedlg.ui  experience.cpp \
	purposedlg.ui purpose.cpp \
	usagedlg.ui usage.cpp \
	questiondlg.ui question.cpp \
	opiniondlg.ui opinion.cpp \
	hardwareinfodlg.ui hardwareinfo.cpp \
	goodbyedlg.ui goodbye.cpp \
	feedback.cpp main.cpp

INCLUDES = $(all_includes)

feedback_LDADD = $(LIB_KDEUI)
feedback_LDFLAGS = $(all_libraries)

METASOURCES = AUTO

xdg_apps_DATA = feedback.desktop

KDE_ICON=AUTO

feedback_pics_data_DATA = pardus.png feedback.png

feedback_pics_datadir = $(kde_datadir)/feedback/pics

podir=../po
COMMAND=$(XGETTEXT) --foreign-user --from-code=utf-8 -C -ci18n -ki18n -ktr2i18n -kI18N_NOOP -kI18N_NOOP2 -kaliasLocale
messages:
	$(COMMAND) *.cpp *.h *.ui -o $(podir)/feedback.pot
