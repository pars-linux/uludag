#!/bin/sh

export NOAN_PATH="/path_to/noan"

./import_source.py ${NOAN_PATH} /mnt/sda6/noan/repo/pardus-source/pardus/devel/ -r Devel -u
./import_source.py ${NOAN_PATH} /mnt/sda6/noan/repo/pardus-source/pardus/2008/ -u
./import_source.py ${NOAN_PATH} /mnt/sda6/noan/repo/pardus-source/pardus/2007/ -u

echo --------------------------

rsync rsync://192.168.3.110/2007 --recursive --delete-after --update --verbose /mnt/sda6/noan/repo/pardus-binary/2007-stable/

echo --------------------------

rsync rsync://192.168.3.110/2007-test --recursive --delete-after --update --verbose /mnt/sda6/noan/repo/pardus-binary/2007-test/

echo --------------------------

./import_binary.py ${NOAN_PATH} /mnt/sda6/noan/repo/pardus-binary/2007-stable /mnt/sda6/noan/repo/pardus-binary/2007-test -r 1.1

echo --------------------------

rsync rsync://192.168.3.111/2008 --recursive --delete-after --update --verbose /mnt/sda6/noan/repo/pardus-binary/2008-stable/

echo --------------------------

rsync rsync://192.168.3.111/2008-test --recursive --delete-after --update --verbose /mnt/sda6/noan/repo/pardus-binary/2008-test/

echo --------------------------

./import_binary.py ${NOAN_PATH} /mnt/sda6/noan/repo/pardus-binary/2008-stable /mnt/sda6/noan/repo/pardus-binary/2008-test
