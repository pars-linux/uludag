#!/bin/sh

# Update pot file:
xgettext \
    --language=python \
    --output=history-manager-kde4.pot \
    --package-name="history-manager-kde4" \
    --package-version="0.2" \
    --msgid-bugs-address="isbaran@gmail.com" \
    -ki18n:1 -ki18nc:1c,2 -ki18np:1,2 -ki18ncp:1c,2,3 \
    -kki18n:1 -kki18nc:1c,2 -kki18np:1,2 -kki18ncp:1c,2,3 \
    -kI18N_NOOP:1 -kI18N_NOOP2:1c,2 \
    ../src/*.py \

# Update po files:
for po in *.po
do
    msgmerge -U "$po" history-manager-kde4.pot && touch "$po"
done

