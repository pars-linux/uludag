pkgname="wink"
pkgdispname="Wink"
tarname="installdata.tar.gz"
installerbasename=`basename $0`
#definstdir="/usr/local/bin/$pkgname"
definstdir=`whoami`
definstdir="/home/$definstdir/$pkgname"

# Goto the proper dir if not already there
cd `dirname $0`

# Show error if we are not running on x86
case `uname -m` in
  i?86) ;;
  *) echo "This installer only has x86 binaries. Sorry.";
     exit 1;;
esac

# extract the exe to curdir
tar -zx --file="$tarname" "$pkgname"
if [ $? != 0 ]; then
  exit $?;
fi

# check if all dependent packages are already installed
dep=`ldd "$pkgname" | grep "not found" | cut -d= -f1`;
if [ "$dep" != "" ]; then
  echo "";
  echo "$pkgdispname requires that the following packages be installed to run properly. Please install them and try again."
  echo ""; echo $dep; echo "";
  exit 2;
fi

# remove the file used to test dependencies
rm "$pkgname"

# Now ask the user where he wants to install our package
echo -e "Please specify where you want to install $pkgdispname [$definstdir]: \c"
read instdir
if [ -z "$instdir" ]; then
  instdir="$definstdir"
fi

# create the installation directory first
mkdir "$instdir"
if [ $? != 0 ]; then
  echo "Installation failed."; exit $?;
fi

# extract the files to the given directory and save the filenames to the variable
#instfiles=`tar -zxv --directory="$instdir" --file="$tarname" | grep -v /$ | tr \  +`
allinstfiles=`tar -zxv --directory="$instdir" --file="$tarname" | tr \  +`
instfiles=`echo "$allinstfiles" | grep -v /$`
instdirs=`echo "$allinstfiles" | grep /$`

if [ $? != 0 ]; then
  echo "Installation failed."; exit $?;
fi

# create uninstaller script
uis="$instdir/uninstall.sh"
echo "cd \`dirname \$0\`" > "$uis";
for fname in $instfiles; do
  fname=`echo "$fname" | tr + \ `
  echo "if [ -f \"$fname\" ]; then" >> "$uis"
  echo " rm \"$fname\"" >> "$uis"
  echo "fi" >> "$uis"
done
for fname in $instdirs; do
  revinstdirs="$fname $revinstdirs"
done
for fname in $revinstdirs; do
  fname=`echo "$fname" | tr + \ `
  echo "rmdir \"$fname\"" >> "$uis"
done
echo "rm \"$uis\"" >> "$uis"
echo "cd .." >> "$uis"
echo "rmdir \"$instdir\"" >> "$uis"
echo "echo Successfully uninstalled $pkgdispname" >> "$uis"
chmod +x "$uis"
#rm "$instdir/$installerbasename"

# whew!
echo "Successfully installed $pkgdispname"

