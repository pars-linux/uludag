#!/bin/sh
srcdir=`dirname $0`

echo "Running libtoolize..."
libtoolize --copy --force --automake

echo "Running aclocal..."
aclocal-1.7

echo "Running autoheader..."
autoheader

echo "Running automake..."
automake-1.7 --add-missing --gnu --include-deps

echo "Running autoconf..."
autoconf

echo
echo "Done!"
echo "Now run $srcdir/configure in order to create Makefiles."
echo

