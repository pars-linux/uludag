#!/bin/sh

# Create template file
echo "Creating pot file..."
xgettext --no-wrap --copyright-holder="Pardus" --package-name="$1" --keyword=i18n --keyword=i18np:1,2 -o ./$1-new.pot code/*/*.py

echo "Fixing header information..."
sed 's/CHARSET/utf-8/' ./$1-new.pot > $1-new1.pot ; rm $1-new.pot
mv $1-new1.pot $1.pot

echo "Done."
