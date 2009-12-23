#!/bin/bash

svn export pardus gfxtheme-pardus-$1
tar cvjf gfxtheme-pardus-$1.tar.bz2 gfxtheme-pardus-$1
sha1sum gfxtheme-pardus-$1.tar.bz2
