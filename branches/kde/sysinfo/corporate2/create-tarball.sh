#!/bin/bash

cd ..
svn export corporate2 sysinfo-$1
tar cvjf sysinfo-$1.tar.bz2 sysinfo-$1
sha1sum sysinfo-$1.tar.bz2
cd -
