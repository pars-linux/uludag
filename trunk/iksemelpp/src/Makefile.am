lib_LTLIBRARIES = libiksemelpp.la

libiksemelpp_la_SOURCES = iksemel.c iksemelpp-dom.cpp iksemelpp-stack.cpp iksemelpp-sax.cpp iksemelpp-exception.cpp

if HAVE_GC
extra = -lgc -lgccpp
else
extra =
endif

libiksemelpp_la_CFLAGS = $(CFLAGS) 
libiksemelpp_la_LIBADD = $(extra)
