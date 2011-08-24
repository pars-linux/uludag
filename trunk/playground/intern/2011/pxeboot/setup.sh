#!/bin/bash

INITRAMFS=`ls /boot/ | sort -r | grep -m 1 initramfs-`
VERSION=`echo $INITRAMFS | cut -c11-`
KERNEL="kernel-$VERSION"
TFTPBOOT_PATH="/tftpboot/pts/latest-ptsp"

python server/iso_to_xml.py /opt/ptsp
echo "1 - ISO xml olusturuldu..."

echo "2 - pxebootselect derleniyor..."
gcc -g -Wall `xml2-config --cflags` client/pxe_select_boot/pxebootselect.c -o client/pxe_select_boot/pxebootselect  -lncurses -lmenu `xml2-config --libs`

echo "3 - Dosyalar kopyalaniyor..."
cp client/initramfs/init /lib/initramfs
cp client/pxe_select_boot/pxebootselect /lib/initramfs

echo "4 - pts klasoru hazirlaniyor"
mkdir /tftpboot/pts/"$VERSION-ptsp"
rm -rf $TFTPBOOT_PATH
ln -s "$VERSION-ptsp" $TFTPBOOT_PATH

echo "5 - Ilk yuklenecek initramfs olusturuluyor..."
python client/initramfs/mkinitramfs -o $TFTPBOOT_PATH --pxeboot --network -k $VERSION

echo "6 - Ilk yuklenecek kernel olusturuluyor..."
cp /boot/$KERNEL $TFTPBOOT_PATH
mkdir $TFTPBOOT_PATH/pxelinux.cfg
cp pxelinux/pxelinux.cfg/default $TFTPBOOT_PATH/pxelinux.cfg/
cp pxelinux/pxelinux.0 $TFTPBOOT_PATH

echo "7 - Baglar olusturuluyor..."
cd $TFTPBOOT_PATH 
ln -s $KERNEL $TFTPBOOT_PATH/latestkernel
ln -s $INITRAMFS $TFTPBOOT_PATH/latestinitramfs

