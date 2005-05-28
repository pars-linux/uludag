#!/bin/sh
. ./gettext.conf

./getpo
./createpo tr_TR.utf8
vi ../locales/tr_TR.utf8/LC_MESSAGES/$APP_NAME.po
./compilepo tr_TR.utf8
