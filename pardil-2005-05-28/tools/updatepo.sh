#!/bin/sh
. ./gettext.conf

./getpo
./mergepo tr_TR.utf8
vi ../locales/tr_TR.utf8/LC_MESSAGES/$APP_NAME.po
./compilepo tr_TR.utf8
