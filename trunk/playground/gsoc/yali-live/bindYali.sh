#!/bin/bash

if [ -d "/yali" ];
then

	echo "Yali is ready in /yali ..."
	rm -rf /yali/* ;
else

mkdir /yali
mount --bind /yali/ /usr/lib/python2.6/site-packages/yali4/

fi


echo build and install

python setup.py install
