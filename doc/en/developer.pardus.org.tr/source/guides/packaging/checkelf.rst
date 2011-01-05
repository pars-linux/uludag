.. _checkelf:

checkelf
========

Checkelf is a script which facilitates developers to find dependencies,
undefined symbols of packages, etc. It's based on Ozan's checkelf's script.
I've tried to explain all available options, which you can examine below.
It has a lot of fine-tuning options which allows the user to get the
desired output directly. For more info please read the options and examples
at the end of the page.


The usage and founctionality:
-----------------------------

::

    -u, --unused

This option is used in order to find unused direct dependencies. It shows
only this options, all other result options are damped.

::

    -f, --undefined

This option is used in forder to find undefined symbols. It shows
only this options, all other result options are damped.

::

    -t, --dependencies

This option is used in order to show the relation between dependencies
in a fancy table. The table has three colums, first one shows the written
dependencies that are written in the pspec.xml. The second colums shows
the dependencies which checkelf has found; these dependencies must be added.
The third column is just a difference from the first and second columd.
It shows dependencies that sould be added to pspec.xml. It shows only this
option, all other options are damped.

::

    -m, --missing

This option is used in order to find missing dependencies according
to ELF files. It list the missing packages that did not exist in
pspec.xml, these sould be added to pspec.xml. It's the same as the
third column in the -t option. It shows only this option, all other options are
damped

::

    -p, --runpath

This option is used in order to show the runpath of a binary file. In fact
it executes 'chrpath -l' and shows the output. It shows only this option,
all other options are damped.

::

    -c, --component <component_name>

This option is used in order to check for packages that belongs to a spesific
component.

Example:

$ checkelf -c tex.addon

::

    -s, --systembase

The dependencies from system.base component have not been listed by default,
if you want to list also system.base related dependencies you have to
use this option. The dependencies from system.base component will be listed
in red and (*) marker. The markes is useful to detect system.base packages
in no-color mode.

::

    -a, --all

This option checks all installed packages in the system. Note that this will
print out all the results to the display which might be useless to read. Using
-n option and piping the output is much more efficient

Examle:

$ checkelf -a -n > results.txt

::

    -n, --no-color

This option close the color option. When you take the output via pipe,
the color characters will be ignored. Thus the output will be clear.

::

    -l, --plain-list

This option shows a simplified output. It doesn prettify anything, it 
justs outputs a plain list of packages. If you want to examine your pacakges
via grep,awk,etc your should use this option

::

    -d, --directory <directory>

This option let you specify a folder to check for pisi files inside that 
directory

Example:

checkelf -d tempdir/

::

    -r, --recursive

This option can be used only with -d option. It recursively search for all
pisi files inside the directory specified with -d. That means if a folder
exist in that directory, the pisi files inside that directory is also checked.


Examples:
--------
In general, checkelf can check for two types. It can check for installed
packages, or it can check for a speficied pisi file.
Below are several examples for real-world use of checkelf

Ex::

    $ checkelf gcc chromium-browser

The installed packages gcc and chromium-browser are checked. Because no options
are specified, checkelfs automatically enables -u, -f, -t options

Ex::

    $ checkelf Publican-2.1-1.pisi -s -m -n

In the above example you can list all system.base related dependencies, only the
missing dependencies of Publican pisi package colorless.

Ex::

    $ checkelf

If checkelf is executed standalone, it will be check for all pisi files
in the directory where it has been executed. If the command is executed without
any parameter the -u, -f, -m paramaters take into account by default.


Ex::

    $ checkelf -d -r tempdir/ foo-4.31.pisi -u

All pisi files inside the tempdir will be checked, if any other folder with other
pisi files exist, these are checked too. Additional to the folder, the package
foo-4.31.pisi is also checked. Note that we've used the -u option here. That means
only the unused direct dependencies are showed, all other results are damped and
are not showed

Ex::

    $ checkelf clementine-0.5.3-3.pisi -c tex.tools -n > checked_packages.txt

It checks for clementine and for all installed packages that belongs to tex.tools
component. We store the results to the file checked_packages.txt, note that -n option
is used to supress the colors. That is useful if you want to use piping. When you dont
use the no-color option, all the ASCI color characters coding will be saved too.
An additional note here should be mentioned. As you see, a pisi file and an installed
package is checked together. However, that is not recommended! Because the enviroment
settings for pisi files are changed. These settings also applies to the installed
packages. That means you could get a clean result, but in fact that might be not the case.


**Last Modified Date:** |today|

:Author: Fatih Arslan, Semen Cirit
