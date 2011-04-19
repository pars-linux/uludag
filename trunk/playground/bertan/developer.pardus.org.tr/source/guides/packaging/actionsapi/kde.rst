.. _kde:

KDE
===

:Author: Semen Cirit
:Date: |today|
:Version: 0.1


configure
---------

::

    configure(parameters)

Configures the kde packages according to the parameters given by the user and PISI's
 default parameters.

The default parameters: (You can see the these defaults from
http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/configfile.py and
http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/actionsapi/variables.py)

::

      --prefix
      --build
      --with-x
      --enable-mitshm
      --with-xinerama
      --with-qt-dir
      --enable-mt
      --with-qt-libraries
      --disable-dependency-tracking
      --disable-debug

Example::

    kde.configure("--without-included-sqlite")
    kde.configure("--with-libsamplerate")
    kde.configure()

make
----

::

    make(parameters)

Builds the kde packages according to the parameters given by the user.

Example:::

    kde.make("-f admin/Makefile.common")
    kde.make()

install
-------

::

    install(parameters='install')

Install the package according to the parameters given by the user and PISI's
default parameters.

Example::

    kde.install()

