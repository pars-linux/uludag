#!/bin/sh

export NOAN_PATH="/home/noan/public_html/noan/noan"

echo "" > /home/noan/public_html/noan/noan/media/sync.txt

# Import 2008 source
./import_source.py ${NOAN_PATH} /home/noan/public_html/noan/repos/sources/pardus/2008/stable -u >> /home/noan/public_html/noan/noan/media/sync.txt
echo -------------------------- >> /home/noan/public_html/noan/noan/media/sync.txt

# Import 2008 binaries (stable and test)
rsync rsync://yali.pardus.org.tr/2008 --recursive --delete-after --update --verbose /home/noan/public_html/noan/repos/binaries/2008-stable/ >> /home/noan/public_html/noan/noan/media/sync.txt
echo -------------------------- >> /home/noan/public_html/noan/noan/media/sync.txt
rsync rsync://yali.pardus.org.tr/2008-test --recursive --delete-after --update --verbose /home/noan/public_html/noan/repos/binaries/2008-test/ >> /home/noan/public_html/noan/noan/media/sync.txt
echo -------------------------- >> /home/noan/public_html/noan/noan/media/sync.txt
./import_binary.py ${NOAN_PATH} /home/noan/public_html/noan/repos/binaries/2008-stable /home/noan/public_html/noan/repos/binaries/2008-test >> /home/noan/public_html/noan/noan/media/sync.txt
echo -------------------------- >> /home/noan/public_html/noan/noan/media/sync.txt

# Import 2009 source
#./import_source.py ${NOAN_PATH} /home/noan/public_html/noan/repos/sources/pardus/2009/stable -u >> /home/noan/public_html/noan/noan/media/sync.txt
echo -------------------------- >> /home/noan/public_html/noan/noan/media/sync.txt

# Import 2009 binaries (stable and test)
#rsync rsync://mudur.pardus.org.tr/2009-stable --recursive --delete-after --update --verbose /home/noan/public_html/noan/repos/binaries/2009-stable/ >> /home/noan/public_html/noan/noan/media/sync.txt
echo -------------------------- >> /home/noan/public_html/noan/noan/media/sync.txt
#rsync rsync://mudur.pardus.org.tr/2009-test --recursive --delete-after --update --verbose /home/noan/public_html/noan/repos/binaries/2009-test/ >> /home/noan/public_html/noan/noan/media/sync.txt
echo -------------------------- >> /home/noan/public_html/noan/noan/media/sync.txt
#./import_binary.py ${NOAN_PATH} /home/noan/public_html/noan/repos/binaries/2009-stable /home/noan/public_html/noan/repos/binaries/2009-test >> /home/noan/public_html/noan/noan/media/sync.txt
echo -------------------------- >> /home/noan/public_html/noan/noan/media/sync.txt
