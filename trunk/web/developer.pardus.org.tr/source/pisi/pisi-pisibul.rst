Pisibul
**************

Introduction
------------------

There are many source packages which don't exist in official repository of Pardus. With pisibul you can perform fast and efficient searches among all source packages. Pisibul can update itself automaticly by downloading latest database of packages in source repositories.

Preperations
------------------

    1. Install PyQt4 via the Package Manager.

Download Pisibul
-----------------------

    1. Run the browser and go to: http://pisibul.sourceforge.net/en.html
    2. Do NOT download the Pisibul pisi package (it doesn't work in 2008.1). Instead, go to the source code and download the GNU tarball to your home directory. 

Installation
--------------------

    1. Run Konsole [Programs>System>Konsole] and type::

          tar -xvf pisibul.tar.gz

    2. Become root (type, "su root"). Then type "cd pisibul/trunk" to navigate to the install files
    3. In Konsole, type the following to install Pisibul::

           python setup.py install

    4. Close Konsole

Using Pisibul
--------------------

Pisibul can be found in the start menu under Utilities. To demonstrate the use of Pisibul I will install a Sudoku game.

    1. Start Pisibul and in the search bar enter "ksudoku".
    2. In the right-hand pane highlight the package and click on "Build Package".
    3. You will see a warning recommending you to install this package via the standard Package Manager. Just click OK.
    4. Enter the password for "root".
    5. A new Konsole will open. Depending upon the package you attempt to build, dependencies may need to be satisfied. Type "yes" if you want to install the missing dependencies (which is what you do want).
    6. The package will now be built, which may take several minutes.
    7. Your new package file will be placed on the Desktop.
    8. Double-click the pisi-file and note that Pardus does not know how to handle this package (it did in older versions of Pardus). In the "Open With" line type::

        /usr/kde/3.5/share/apps/package-manager/pm-install.py

Then click OK. 

    9. The package will now be installed, just like any other package.
    10.  Close the finished Konsole window.

Notes
----------

    *  Pisibul works remarkably well, although a large packages such as OpenOffice are more likely to fail.
    * I do not recommend activating Playground, unless you have enough programming experience under your belt.
    * Packages you install by using Pisibul can be removed through the normal Package Manager. 

