##
## Process this file with automake to produce Makefile.in
##

SUBDIRS = include src

EXTRA_DIST =

snapshot:
	$(MAKE) dist distdir=$(PACKAGE)-`date +"%y%m%d"`
	mv $(PACKAGE)-`date +"%y%m%d"`.tar.gz ../
