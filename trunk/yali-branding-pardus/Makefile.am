SUBDIRS = po

releasedir = $(datadir)/yali/branding/pardus
release_in_files = release.xml.in
release_DATA = $(release_in_files:.xml.in=.xml)

@INTLTOOL_XML_RULE@

EXTRA_DIST = \
	     $(release_in_files)

CLEANFILES = \
	     $(release_DATA)

DISTCLEANFILES =
