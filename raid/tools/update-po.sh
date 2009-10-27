#!/bin/bash

LANGUAGES=`ls po/*.po`

set -x

xgettext -L "python" -k__tr -k_ yali4/gui/Ui/*.py yali4/gui/*.py yali4/*.py -o po/yali4.pot
for lang in $LANGUAGES
do
    msgmerge -U $lang po/yali4.pot
done

