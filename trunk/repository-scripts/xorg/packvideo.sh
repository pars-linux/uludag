#!/bin/bash

VERSION="xorg-video-7.1"
MIRROR="http://ftp.gwdg.de/pub/x11/x.org/pub/individual/driver/"

# xf86-video-impact is mips only
PACKAGES="xf86-video-apm-1.1.1.tar.bz2
xf86-video-ark-0.6.0.tar.bz2
xf86-video-ast-0.81.0.tar.bz2
xf86-video-ati-6.6.2.tar.bz2
xf86-video-chips-1.1.1.tar.bz2
xf86-video-cirrus-1.1.0.tar.bz2
xf86-video-cyrix-1.1.0.tar.bz2
xf86-video-dummy-0.2.0.tar.bz2
xf86-video-fbdev-0.3.0.tar.bz2
xf86-video-glint-1.1.1.tar.bz2
xf86-video-i128-1.2.0.tar.bz2
xf86-video-i740-1.1.0.tar.bz2
xf86-video-i810-1.6.5.tar.bz2
xf86-video-imstt-1.1.0.tar.bz2
xf86-video-mga-1.4.2.tar.bz2
xf86-video-neomagic-1.1.1.tar.bz2
xf86-video-newport-0.2.0.tar.bz2
xf86-video-nsc-2.8.1.tar.bz2
xf86-video-nv-1.2.0.tar.bz2
xf86-video-rendition-4.1.0.tar.bz2
xf86-video-s3-0.4.1.tar.bz2
xf86-video-s3virge-1.9.1.tar.bz2
xf86-video-savage-2.1.1.tar.bz2
xf86-video-siliconmotion-1.4.1.tar.bz2
xf86-video-sis-0.9.1.tar.bz2
xf86-video-sisusb-0.8.1.tar.bz2
xf86-video-sunbw2-1.1.0.tar.bz2
xf86-video-suncg14-1.1.0.tar.bz2
xf86-video-suncg3-1.1.0.tar.bz2
xf86-video-suncg6-1.1.0.tar.bz2
xf86-video-sunffb-1.1.0.tar.bz2
xf86-video-sunleo-1.1.0.tar.bz2
xf86-video-suntcx-1.1.0.tar.bz2
xf86-video-tdfx-1.2.1.tar.bz2
xf86-video-tga-1.1.0.tar.bz2
xf86-video-trident-1.2.1.tar.bz2
xf86-video-tseng-1.1.0.tar.bz2
xf86-video-v4l-0.1.1.tar.bz2
xf86-video-vesa-1.2.1.tar.bz2
xf86-video-vga-4.1.0.tar.bz2
xf86-video-via-0.2.1.tar.bz2
xf86-video-vmware-10.13.0.tar.bz2
xf86-video-voodoo-1.1.0.tar.bz2"

mkdir $VERSION/
cd $VERSION

for i in $PACKAGES
do
    wget $MIRROR"/"$i
    tar jxvf $i
    rm -f $i
done

cd ..
tar cjvf $VERSION.tar.bz2 $VERSION/
rm -rf $VERSION/
