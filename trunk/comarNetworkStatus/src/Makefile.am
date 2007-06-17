kde_module_LTLIBRARIES = kded_comarnetworkstatus.la

METASOURCES = AUTO
INCLUDES = $(all_includes)

kded_comarnetworkstatus_la_SOURCES = comarNetworkStatus.cpp comarNetworkStatus.skel networkstatusiface.stub
kded_comarnetworkstatus_la_LDFLAGS = $(all_libraries) -module -avoid-version
kded_comarnetworkstatus_la_LIBADD = $(all_libraries) $(KDE_RPATH) -lnetworkstatus

networkstatusiface_DIR = $(includedir)

servicesdir = $(kde_servicesdir)/kded
services_DATA = comarNetworkStatus.desktop
