.. _pythonmodules:

Pythonmodules
=============

:Author: Semen Cirit
:Date: |today|
:Version: 0.1


configure
---------

::

    configure(parameters)

Configure python packages with given parameters.

compile
-------

::

    compile(parameters)

Builds the python packages with the given parameters.


install
-------

::

    install(parameters)

Executes python setup.py install command in the install directory with the
given parameters.

run
---

::

    (parameters)

Runs the python binary with the given parameters.

fixCompiledPy
-------------

::

    fixCompiledPy(lookInto = '/usr/lib/%s/' % get.curPYTHON())

Cleans .py[co] from python packages. The default lookInto parameter is
'/usr/lib/%s/' % get.curPYTHON().

Example::

    pythonmodules.fixCompiledPy("/usr/kde/4/share/apps/frescobaldi/lib/frescobaldi_app")
    fixCompiledPy()
