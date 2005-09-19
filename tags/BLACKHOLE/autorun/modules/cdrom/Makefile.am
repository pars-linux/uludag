pkglib_LTLIBRARIES = libautorun_cdrom.la

libautorun_cdrom_la_SOURCES = cdrom.c

INCLUDES = -I../../include -g -Wall -Werror

libautorun_cdrom_la_LDFLAGS = -no-version-info

install-am:
	@$(MAKE) $(AM_MAKEFLAGS) install-exec-am install-data-am
	rm -f $(pkglibdir)/libautorun_cdrom.a
	rm -f $(pkglibdir)/libautorun_cdrom.la
	rm -f $(pkglibdir)/libautorun_cdrom.so
	rm -f $(pkglibdir)/libautorun_cdrom.so.0
