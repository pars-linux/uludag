#!/bin/bash
LANGUAGES=`ls po/*.po`
set -x

xgettext -L "python" -k__tr -k_ *.py -o po/sinerji.pot
for lang in $LANGUAGES
do
  msgmerge -U $lang po/sinerji.pot
done

