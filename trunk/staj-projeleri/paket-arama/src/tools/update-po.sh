#!/bin/bash

LANGUAGES=`ls po/*.po`

set -x

xgettext -L "python" -k__tr -k_ arama/*.py -o po/arama.pot
for lang in $LANGUAGES
do
    msgmerge -U $lang po/arama.pot
done

