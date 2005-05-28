kde_module_LTLIBRARIES = kcm_comartest.la

kcm_comartest_la_SOURCES = comartest.cpp

kcm_comartest_la_LDFLAGS = $(all_libraries) -module -avoid-version -no-undefined
kcm_comartest_la_LIBADD = -lkdeui -lcomarrpc

INCLUDES= $(all_includes)

kcm_comartest_la_METASOURCES = comartest.moc

xdg_apps_DATA = comartest.desktop
