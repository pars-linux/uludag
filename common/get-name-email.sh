#!/bin/sh

ACCOUNTS_FILE=accounts
LOGIN_NAME=$1

ACCOUNT=`grep "^$LOGIN_NAME:" $ACCOUNTS_FILE`
NAME=`echo $ACCOUNT | cut -d: -f 2`
EMAIL=`echo $ACCOUNT | cut -d: -f 3 | sed "s, \[at\] ,@,"`

echo "$NAME <$EMAIL>"
