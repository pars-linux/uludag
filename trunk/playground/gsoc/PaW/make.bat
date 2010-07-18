@echo off

set prjname=PaW
set pawexe=PaW.exe
set srcpath=src\
set icopath=%srcpath%ui\img\pardus_icon_64_64.ico
set builddir=build
set pyinstallerdir=pyinstaller

echo *********************************************
echo Starting PyInstaller script
echo NOTE: Make sure that SVN is installed and in PATH.

echo *********************************************
echo Removing pyinstaller and build folder if exists.
rd /S /Q %pyinstallerdir%
rd /S /Q %builddir%
mkdir %builddir%

echo *********************************************
echo Checking out the latest pyInstaller via SVN
svn co http://svn.pyinstaller.org/trunk %pyinstallerdir%
echo Checked out PyInstaller

cd %pyinstallerdir%
echo *********************************************
echo Configuring PyInstaller
python Configure.py

echo *********************************************
echo Creating specificiations for PaW
python Makespec.py --onefile --icon=..\%srcpath%ui\img\pardus_icon_64_64.ico --name=%prjname% ..\%srcpath%__main__.py

echo *********************************************
echo Building %prjname%
python Build.py %prjname%\%prjname%.spec

echo *********************************************
echo Copying generated .exe file to %builddir%\.
copy %prjname%\dist\%prjname%.exe ..\%builddir%\

echo *********************************************
echo Copying other required files.
cd ..
copy %srcpath%versions.xml %builddir%\
copy %srcpath%files\boot.ini.tpl %builddir%\
copy %srcpath%files\grub4dos\menu.lst.tpl %builddir%\
copy %srcpath%files\grub4dos\grldr %builddir%\
copy %srcpath%files\grub4dos\grldr.mbr %builddir%\
copy %srcpath%files\grub4dos\pardus.tag %builddir%\
copy %srcpath%ui\img\pardus_icon_48_48.ico %builddir%\

echo *********************************************
echo Removing pyinstaller
rd /S /Q %pyinstallerdir%

echo *********************************************
echo %prjname%.exe is ready under '%builddir%/'. Press any key to exit.
pause>NUL