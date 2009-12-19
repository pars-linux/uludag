#!/bin/bash

# This script can be used to merge unchanged translated templates from
# bugzilla 3.x to 3.y.

# Usage:
# merge-translations.sh 3.2 3.4

OLD=$1
NEW=$2

# Find out modified templates

find $OLD/en/default/ -type f | egrep -v '.svn' | sort -u | cut -d/ -f2- | sort -u > oldlist
find $NEW/en/default/ -type f | egrep -v '.svn' | sort -u | cut -d/ -f2- | sort -u > newlist

diff -u oldlist newlist | grep '^+en' | cut -c2- > newtemplates

echo "New templates that need to be translated are:"
echo "---------------------------------------------"
echo

cat newtemplates

echo "Unmodified templates are:"
echo "-------------------------"
echo

for f in $(cat oldlist); do
    cmp $OLD/$f $NEW/$f &> /dev/null
    if [ $? == 0 ]; then
        echo $f | tee -a unmodified
    fi
done

echo "Merging TR translations.."
unalias cp

for f in $(cat unmodified); do
    relpath=$(echo $f | cut -d/ -f3-)
    cp $OLD/tr/default/$relpath $NEW/tr/default/$relpath
done

rm -rf oldlist newlist newtemplates

#LC_ALL=C diff -Naurq --exclude=.svn $OLD/en/default/ $NEW/en/default/ | awk '{print $2}' | cut -d/ -f2- | sort -u > modified
