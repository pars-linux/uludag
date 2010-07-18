@echo off

set prjname=PaW
set pawexe=PaW.exe
set builddir=build
set pyinstallerdir=pyinstaller

echo *********************************************
echo Starting PyInstaller script
mkdir build

echo *********************************************
echo Removing pyinstaller folder if exists.
rd /S /Q %pyinstallerdir%

echo *********************************************
echo Checking out latest PyInstaller
svn co http://svn.pyinstaller.org/trunk %pyinstallerdir%
echo Checked out PyInstaller

cd %pyinstallerdir%
echo *********************************************
echo Configuring PyInstaller
python Configure.py

echo *********************************************
echo Creating specificiations for PaW
python Makespec.py --onefile --windowed --icon=../src/ui/img/pardus_icon_64_64.ico --name=PaW ..\src\__main__.py

echo *********************************************
echo Building PaW
python Build.py PaW\PaW.spec

echo *********************************************
echo Copying generated .exe file to build\.
copy PaW\dist\PaW.exe ..\build\

echo *********************************************
echo Copying other required files.
cd ..
copy src\versions.xml build\
copy src\ui\img\pardus_icon_48_48.ico build\

echo *********************************************
echo Removing pyinstaller
rd /S /Q %pyinstallerdir%

echo *********************************************
echo PaW.exe is ready under 'build/'. Press any key to exit.
pause "You are not expected to understand this."