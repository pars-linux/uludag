#!/bin/bash

NAME="pardus-dev-tools"
VERSION=0.0.1
DIRNAME="$NAME-$VERSION"
SVR="ibrahim@cekirdek.pardus.org.tr"
DST="public_html/dist"

EXTRA_DIST="\
AUTHORS \
ChangeLog \
COPYING \
INSTALL \
NEWS \
README \
TODO"

DIST=`cat MANIFEST`

if [ -z "$1" ]; then
    echo "Usage: $0 <uludag/trunk/scripts directory>"
    exit 0
fi

if [ -d "$1" ]; then
    SCRIPTSDIR="$1"
else
    echo "Given path is not a directory."
    exit 1
fi

if [ -d $DIRNAME ]; then
    echo "$DIRNAME already exists."
    exit 1
fi

mkdir -p $DIRNAME/scripts

echo "Checking out scripts directory..."
svn up $SCRIPTSDIR

for script in $DIST; do
    cp "$SCRIPTSDIR/$script" "$DIRNAME/scripts/"
done

echo "Rolling..."
cp -R $EXTRA_DIST $DIRNAME
tar cjvf $DIRNAME.tar.bz2 $DIRNAME --exclude .svn
rm -rf $DIRNAME

echo "Sending..."
scp $DIRNAME.tar.bz2 $SVR:$DST
