.. _kde4:

KDE4
====

:Author: Semen Cirit
:Date: |today|
:Version: 0.1


Default Parameters
------------------
You can see all of the default parameters from:
`<http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/actionsapi/kde4.py>`_

basename
^^^^^^^^

The base name is gived as "kde4".

prefix
^^^^^^

The default prefix is the default prefix of Pardus (see 
`link <http://developer.pardus.org.tr/guides/packaging/actionsapi/get.html#defaultprefixdir>`_

libdir
^^^^^^

The default library directory is the concatenation of the default prefix
directory and /lib value.

bindir
^^^^^^

The default binary directory is the concatenation of the default prefix
directory and /bin value.

modulesdir
^^^^^^^^^^

The default module directory is the concatenation of the default libdir
directory and basename value.

libexecdir
^^^^^^^^^^

The default libexec directory is the concatenation of the default modulesdir
directory and /libexec value.

iconsdir
^^^^^^^^

The default icon directory is the concatenation of the default prefix
directory and /share/icons value.

applicationsdir
^^^^^^^^^^^^^^^

The default application directory is the concatenation of the default prefix
directory, /share/applications/ and basename value.

mandir
^^^^^^

The default man dirrectory is the default man directory of Pardus (see 
`link <http://developer.pardus.org.tr/guides/packaging/actionsapi/get.html#mandir>`_)

sharedir
^^^^^^^^

The default share directory is the concatenation of the default prefix
directory, /share/ and basename value.

appsdir
^^^^^^^

The default apps directory is the concatenation of the default sharedir
directory and /apps value.

configdir
^^^^^^^^^

The default config directory is the concatenation of the default sharedir
directory and /config value.

sysconfdir
^^^^^^^^^^

This id /etc value

servicesdir
^^^^^^^^^^^

The default service directory is the concatenation of the default sharedir
directory and /services value.

servicetypesdir
^^^^^^^^^^^^^^^

The default service types directory is the concatenation of the default sharedir
directory and /servicetypes value.

includedir
^^^^^^^^^^

The default include directory is the concatenation of the default prefix
directory, /include/ and basename value.

docdir
^^^^^^

The default doc directory is the concatenation of the default man directory of
Pardus (see `link <http://developer.pardus.org.tr/guides/packaging/actionsapi/get.html#mandir>`_) and basename value.

htmldir
^^^^^^^

The default html directory is the concatenation of the default docdir
directory and /html value.
= "%s/html" % docdir

wallpapersdir
^^^^^^^^^^^^^

The default wallpaper directory is the concatenation of the default prefix
directory and /share/wallpapers value.

configure
---------

::

    configure(parameter)

Configures the kde4 packages according to the parameters given by the user and PISI's
default parameters.

The default parameters:(You can see the assigned values from
`here <http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/actionsapi/kde4.py>`_)

::

       -DDATA_INSTALL_DIR:PATH
       -DINCLUDE_INSTALL_DIR:PATH
       -DCONFIG_INSTALL_DIR:PATH
       -DLIBEXEC_INSTALL_DIR:PATH
       -DSYSCONF_INSTALL_DIR:PATH
       -DHTML_INSTALL_DIR:PATH
       -DMAN_INSTALL_DIR:PATH
       -DCMAKE_SKIP_RPATH:BOOL
       -DLIB_INSTALL_DIR:PATH

Examples::

    kde4.configure()

make
----

::

    make(parameter)

Builds the kde4 packages according to the parameters given by the user.

install
-------

::

    install(parameters = '', argument = 'install')

Install the kde4 packages according to the parameters given by the user.

