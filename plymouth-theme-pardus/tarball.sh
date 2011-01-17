#!/bin/bash

TARGET=$1

if [ -z $TARGET ]; then
    echo "Usage: $0 [2011|corporate2]"
    exit
fi

svn export . /tmp/pardus
cd /tmp
mv pardus/pardus.script{.$TARGET,}
tar cvjf plymouth-theme-pardus.tar.bz2 pardus
rm -rf pardus

