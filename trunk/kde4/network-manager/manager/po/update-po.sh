#!/bin/bash

LANGUAGES=`ls po/*.po`
TEMP=`mktemp`
set -x

xgettext -L "python" -k__tr -k_ -ki18n build/*.py -o po/base.pot
for lang in $LANGUAGES
do
    #msgcat --use-first -o $TEMP $lang po/yali4.pot
    msgmerge -q -o $TEMP $lang po/base.pot
    cat $TEMP > $lang
done
rm -f $TEMP
