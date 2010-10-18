.. _checklib:

Checklib
========

Checklib is a script which facilitates developers to find dependencies,
undefined symbols of packages.

The usage and founctionality:
-----------------------------

::

    -u, --unused

This option is used in order to find unused direct dependencies.

::

    -f, --undefined

This option is used in forder to find undefined symbols

::

    -m, --missing

This option is used in order to find missing dependencies according
to ELF files. It list the missing packages that did not exist in
pspec.xml.

::

    -s, --systembase

The dependencies from system.base component have not been listed by default,
if you want to list also system.base related dependencies you have to
use this option. The dependencies from system.base component will be listed
in red and (*) marker.

::

    -n, --no-color

This option close the color option. When you take the output via pipe,
the color characters will be ignored. Thus the output will be clear.

::

    -d <directory>
This option enable developer to find dependencies of packges under the
given directory.

::

    -r <directory>

This option enable developer to find dependencies under the given
directory recursively.


And you can use these option in combination:

Ex::

    $ checklib2 gcc chromium-browser -d -r testdir/ Publican-2.1-1.pisi

In this example the packages gcc and chromium-browser, the packages
under testdir and Publican pisi package dependencies can be listed
on the output respectively.

Ex::

    $ checklib2 Publican-2.1-1.pisi -s -m -n

In the above example you can list all system.base related dependencies
of Publican pisi package colorless.

Ex::

    $ checklib2

If the command use like above, it will be list dependencies of all packages
in the directory where it has been executed.

If the command is executed without any parameter the -u, -f, -m paramaters
take into account by default.

You can also see all the parameters with checklib2 --help

**Last Modified Date:** |today|

:Author: Fatih Arslan, Semen Cirit
