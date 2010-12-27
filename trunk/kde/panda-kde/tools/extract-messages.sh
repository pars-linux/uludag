#!/bin/sh
BASEDIR="/root/repo/uludag/trunk/kde/panda-kde"    # root of translatable sources
PROJECT="panda-kde"        # project name
WDIR=`pwd`              # working dir

# see above on sorting
find . -name '*.cpp' -o -name '*.h' -o -name '*.c' | sort > ${WDIR}/infiles.list
cd ${WDIR}
xgettext --from-code=UTF-8 -C -kde -ci18n -ki18n:1 -ki18nc:1c,2 -ki18np:1,2 -ki18ncp:1c,2,3 -ktr2i18n:1 \
	-kI18N_NOOP:1 -kI18N_NOOP2:1c,2 -kaliasLocale -kki18n:1 -kki18nc:1c,2 -kki18np:1,2 -kki18ncp:1c,2,3 \
	--files-from=infiles.list -D ${BASEDIR} -D ${WDIR} -o ${BASEDIR}/${PROJECT}.pot || { echo "error while calling xgettext. aborting."; exit 1; }
echo "Done extracting messages"


echo "Merging translations"
catalogs=`find . -name '*.po'`
for cat in $catalogs; do
  echo $cat
  msgmerge -o $cat.new $cat ${BASEDIR}/${PROJECT}.pot
  mv $cat.new $cat
done
echo "Done merging translations"


echo "Cleaning up"
cd ${WDIR}
rm infiles.list
echo "Done"
