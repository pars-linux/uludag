kde_module_LTLIBRARIES = kcm_tasmanet.la

kcm_tasmanet_la_SOURCES = devicesettingsdlg.ui devicesettings.cpp tasmanetwidget.cpp tasmanet.cpp

kcm_tasmanet_la_LDFLAGS = $(all_libraries) -module -avoid-version -no-undefined
kcm_tasmanet_la_LIBADD = -lkdeui -liw

INCLUDES= $(all_includes)

METASOURCES = AUTO

xdg_apps_DATA = tasmanet.desktop
