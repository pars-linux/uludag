.. _libtools:

Libtools
========

:Author: Semen Cirit
:Date: |today|
:Version: 0.1


preplib
--------

::

    prelib(sourceDirectory)

Executes ldconfig command in the sourceDirectory.

Example::

    libtools.preplib()


gnuconfig_update
----------------

::

    gnuconfig_update()

Copies the newest config.sub and config.guess files to the source.

Example::

    libtools.gnuconfig_update()

libtoolize
----------

::

    libtoolize(parameters)

Makes it possible to execute libtoolize with given parameters on the source.

Examples::

    libtools.libtoolize()
    libtools.libtoolize("--force --copy")
    libtools.libtoolize("--force --install")


gen_usr_ldscript
----------------

::

    gen_usr_ldscript(dynamicLib)

Since Pardus has critical dynamic libraries in /lib, and the static versions in
/usr/lib, we need to have a dynamic lib in /usr/lib, otherwise we run
into linking problems.

Examples::

    libtools.gen_usr_ldscript("libhandle.so")
    libtools.gen_usr_ldscript("libhandle.so")
    libtools.gen_usr_ldscript("libdevmapper.so")

