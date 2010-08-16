#!/bin/bash
#Tweaked bindScript by SarathLakshman
echo Binding Yali;

rm -rf /yali 2> /dev/null
umount /yali 2> /dev/null

mkdir /yali/backup -p
cp /usr/lib/python2.6/site-packages/yali4/* /yali/ -Rp
mount --bind /yali/ /usr/lib/python2.6/site-packages/yali4/


cp /yali/sysutil* /yali/backup -Rp
cp -Rp yali4/*.py /yali
cp -Rp yali4/gui/* /yali/gui
cp /yali/backup/* /yali/ -Rp

cp desktop/yali-live ~pars/.yali-live
chmod +xs ~pars/.yali-live
cp desktop/yali-live-installer.desktop ~pars/Desktop/

#echo build and install

#python setup.py install
