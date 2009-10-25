#!/bin/sh

ACCOUNTS_FILE=$(dirname $0)/accounts
LOGIN_NAME=$1

if [ ! -f $ACCOUNTS_FILE ]; then
    wget http://svn.pardus.org.tr/uludag/trunk/common/accounts >/dev/null 2>&1
    ACCOUNTS_FILE=accounts
fi

ACCOUNT=`grep "^$LOGIN_NAME:" $ACCOUNTS_FILE` || exit 1
NAME=`echo $ACCOUNT | cut -d: -f 2`
EMAIL=`echo $ACCOUNT | cut -d: -f 3 | sed "s, \[at\] ,@,"`

echo "$NAME <$EMAIL>"
