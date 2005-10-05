SUBDIRS=po

kde_module_LTLIBRARIES = kcm_tasmanet.la

kcm_tasmanet_la_SOURCES = devicesettingsdlg.ui device.cpp devicesettings.cpp tasmanetwidget.cpp tasmanet.cpp

kcm_tasmanet_la_LDFLAGS = $(all_libraries) -module -avoid-version -no-undefined
kcm_tasmanet_la_LIBADD = -lkdeui -liw

INCLUDES= $(all_includes)

METASOURCES = AUTO

xdg_apps_DATA = tasmanet.desktop

podir=po

COMMAND=$(XGETTEXT) --foreign-user -C -ci18n -ki18n -ktr2i18n -kI18N_NOOP -kI18N_NOOP2 -kaliasLocale
messages:
	$(COMMAND) *.cpp *.h -o $(podir)/tasmanet.pot

