#!/bin/bash

LANGS='ca de es fr it nl pl pt_BR tr sv'

xgettext sysinfo/*.cpp -o po/kio_sysinfo.pot -ki18n -ktr2i18n -kI18N_NOOP -ktranslate -kaliasLocale

for lang in $LANGS
do
    echo "updating $lang"
    msgmerge -U po/$lang/kio_sysinfo.po po/kio_sysinfo.pot
done

