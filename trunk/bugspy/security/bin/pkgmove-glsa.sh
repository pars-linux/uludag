#!/bin/bash

UPDATESDIR="/usr/portage/profiles/updates"
GLSADIR="/dev/shm/glsa"

THISYEAR="`date +%Y`"

year=2004

while [ $year -le $THISYEAR ] ; do

	for file in "$UPDATESDIR"/[1-4]Q-"$year" ; do
		[ ! -e "$file" ] && continue
		echo `basename "$file"`

		replace=""

		while read LINE ; do
			FROM=`echo $LINE | cut -d " " -f 2`
			TO=`echo $LINE | cut -d " " -f 3`
			replace="$replace -e s:$FROM\(\"\|&\|-[0-9]\):$TO\1:g"
		done < <(grep "^move " "$file")
		sed -i $replace "$GLSADIR"/glsa-*xml
	done

	let year=year+1
done

