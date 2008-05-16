#!/bin/bash

LANGS='ca de es fr it nl pl pt_BR tr'

xgettext sysinfo/*.cpp -o po/kio_sysinfo.pot -ki18n -ktr2i18n -kI18N_NOOP -ktranslate -kaliasLocale

for lang in $LANGS
do
    msgmerge -U po/$lang/kio_sysinfo.po po/kio_sysinfo.pot
done

