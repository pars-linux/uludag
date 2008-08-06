#!/bin/sh
#
# pardus-1.0 to pardus-2007 upgrade script
#
##

# remove current repo and add 2007-trampoline repository
pisi rr pardus-devel
pisi ar -y 2007-trampoline http://cekirdek.pardus.org.tr/~faik/pisi/pardus-1.0/pisi-index.xml

# install all necessary packages with 1.0 package format
pisi it -y --reinstall python
pisi it -y --reinstall -E lzma piksemel python-bsddb3 pisi comar-api comar 

# try again: an old comar restart bug
pisi it -y --reinstall -E lzma piksemel python-bsddb3 pisi comar-api comar

# rebuild database
pisi rdb -y

# switch to pardus-2007 repo
pisi ar -y pardus-2007 http://paketler.pardus.org.tr/pardus-2007/pisi-index.xml.bz2

# all set... yay! up up to 2007
pisi up -y

# paranoia: reinstall again with latest buildnos
pisi it -y --reinstall python lzma piksemel python-bsddb3 mudur pisi comar-api comar

# delete cached ksplash themes
rm -rf ~/.kde3.5/share/apps/ksplash/cache/Moodin/*

# after a reboot X magically worked without a single touch. But let zorg recreate it.
mv /etc/X11/xorg.conf /etc/X11/xorg.conf_1.0-2007_upgrade.backup
