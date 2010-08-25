#!/bin/bash

LANGUAGES=`cat LINGUAS`
TEMP=`mktemp`
set -x

if [ -z $1 ];then
    echo "give an argument: po or html"
    echo "po; to update pot file according to the html template and merge the changes from pot file to po files."
    echo "html; to update html files according to translated po files"

elif [ $1 = "html" ];then
    for lang in $LANGUAGES
    do
        po2html -t ../media-content/release-notes/releasenotes-en.html "$lang".po ../media-content/release-notes/releasenotes-"$lang".html
    done

elif [ $1 = "po" ];then
    for lang in $LANGUAGES
    do
        html2po -u --keepcomments ../media-content/release-notes/releasenotes-en.html -P releasenotes.pot
        msgmerge --no-wrap --sort-by-file -q -o $TEMP $lang.po releasenotes.pot
        cat $TEMP > $lang.po
    done
    rm -f $TEMP
fi

