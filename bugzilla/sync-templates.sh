#!/bin/bash

# Usage
# sync-template <work_dir_to_sync> <version_to_sync_from>
# e.g. sync-template 3.4 3.4.4

# Tarball to fetch
URL="http://ftp.mozilla.org/pub/mozilla.org/webtools/bugzilla-$2.tar.gz"
DIR="bugzilla-$2"

wget $URL
echo "Unpacking $DIR"
tar xvzf `basename $URL` &> /dev/null
rm -rf `basename $URL`

# Clean CVS directories
find $DIR/ -type d -name CVS | xargs rm -rf

# Now we have new templates in $DIR/template/en/default
diff -Naur --exclude=.svn $1/en/default $DIR/template/en/default > templates-$2.patch

cd $1/en/default
echo "Patching $1.."
patch -p4 < ../../../templates-$2.patch
cd -

echo "$1 templates are now in sync with bugzilla $2, have fun."
rm -rf templates-$2.patch

# Cleanup
rm -rf $DIR
