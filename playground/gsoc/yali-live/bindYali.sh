#!/bin/bash

mkdir /yali
mount --bind /yali/ /usr/lib/python2.6/site-packages/yali4/

echo "Yali is ready in /yali ..."

echo build and install

python setup.py install
