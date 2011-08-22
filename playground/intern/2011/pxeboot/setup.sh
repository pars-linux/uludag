#!/bin/bash

python server/iso_to_xml.py /opt/ptsp
echo "1- ISO xml olusturuldu..."


echo "2 - pxebootselect derleniyor..."
gcc -g -Wall `pkg-config libxml-2.0 --cflags --libs` client/pxebootselect/pxebootselect.c -o client/pxebootselect/pxebootselect -lncurses -lmenu


echo "3 -Dosyalar kopyalanıyor..."
cp client/initramfs/init /lib/initramfs
cp client/initramfs/hotplug /lib/initramfs
cp client/initramfs/profile.rc /lib/initramfs
cp client/initramfs/udhcpc.script /lib/initramfs
cp client/pxebootselect/pxebootselect /lib/initramfs
cp client/initramfs/checkfirstload /lib/initramfs

echo "4 - Ilk yuklenecek initramfs olusturuluyor..."
python client/initramfs/mkinitramfs -o /tftpboot/pts/latest-ptsp/ --pxeboot --network

echo "Server hazirlandi..."
