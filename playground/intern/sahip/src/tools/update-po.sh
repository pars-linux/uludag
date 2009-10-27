#!/bin/bash

LANGUAGES=`ls po/*.po`

set -x

xgettext -L "python" -k__tr -k_ sahip/sahip sahip/*.py -o po/sahip.pot
for lang in $LANGUAGES
do
    msgmerge -U $lang po/sahip.pot
done

