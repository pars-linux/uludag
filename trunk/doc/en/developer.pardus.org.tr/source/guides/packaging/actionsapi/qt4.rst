.. _qt4:

Qt4
===

:Author: Semen Cirit
:Date: |today|
:Version: 0.1


Default Values
--------------

You can see all of the default parameters from:
http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/actionsapi/qt4.py

basename
^^^^^^^^

The default basename value is "qt4"

prefix
^^^^^^^

The default prefix is the default prefix of Pardus (see·
`link <http://developer.pardus.org.tr/guides/packaging/actionsapi/get.html#defaultprefixdir>`_)

libdir
^^^^^^
The default library directory is the concatenation of the default prefix
directory and /lib value.

bindir
^^^^^^

The default binary directory is the concatenation of the default prefix
directory and /bin value.

datadir
^^^^^^^

The default data directory is the concatenation of the default prefix
directory, /share and basename value.

includedir
^^^^^^^^^^

The default include directory is the concatenation of the default prefix
directory and /include value.

docdir
^^^^^^

The default doc directory is the concatenation of default doc directory of
Pardus and basename value. (see `link <http://developer.pardus.org.tr/guides/packaging/actionsapi/get.html#mandir>`_)

examplesdir
^^^^^^^^^^^

The default example directory is the concatenation of the default libdir
directory, basename  value and /examples value.

demosdir
^^^^^^^^

The default demo directory is the concatenation of the default libdir
directory, basename  value and /demos value.

importdir
^^^^^^^^^

The default import directory is the concatenation of the default libdir
directory, basename  value and /imports value.

plugindir
^^^^^^^^^

The default plugin directory is the concatenation of the default libdir
directory, basename value and /plugins value.

translationdir
^^^^^^^^^^^^^^

The default translation directory is the concatenation of the default datadir
directory and /translations value.

sysconfdir
^^^^^^^^^^

This value is set  as "/etc".

qmake
^^^^^

The default qmake binary is put into default bindir.


Configure
---------

::

    configure(projectfile='', parameters='', installPrefix=prefix)

Configures the qt4 packages according to the parameters and project file given
by the user and PISI's default parameters.

Make
----

::

    make(parameters)

Builds the qt4 packages according to the parameters given by the user.

install
-------

::

    install(parameters = '', argument = 'install')

Install the qt4 packages according to the parameters given by the user.

