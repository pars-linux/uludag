kde_module_LTLIBRARIES = kcm_tasmatv.la

kcm_tasmatv_la_SOURCES = tasmatv.cpp tvconfigui.ui tvconfig.cpp

kcm_tasmatv_la_LDFLAGS = $(all_libraries) -module -avoid-version -no-undefined
kcm_tasmatv_la_LIBADD = -lkdeui -liw

INCLUDES= $(all_includes)

METASOURCES = AUTO

xdg_apps_DATA = tasmatv.desktop

podir=po

COMMAND=$(XGETTEXT) --from-code=UTF-8 --foreign-user -C -ci18n -ki18n -ktr2i18n -kI18N_NOOP -kI18N_NOOP2 -kaliasLocale
messages:
	$(COMMAND) *.cpp *.h -o $(podir)/tasmatv.pot
