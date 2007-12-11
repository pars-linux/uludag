#!/bin/sh

if [[ ${UID} != 0 ]]
then
    echo "You must be root";
    exit 1;
fi

rm -rf data/

echo "Running Comar..."
../comar/comar-dbus --print --configdir=../comar/etc --datadir=data --debug=full
