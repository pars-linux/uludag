.. _autotools:

Autotools
=========

:Author: Semen Cirit
:Date: |today|
:Version: 0.1


configure
---------

::

    configure(parameters)

Configures the package according to the parameters given by the user and PISI's
default parameters.

The default parameters: (You can see the these defaults from 
http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/configfile.py and
http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/actionsapi/variables.py)

::

    --prefix
    --build
    --mandir
    --infodir
    --datadir
    --sysconfdir
    --localstatedir
    --libexecdir

Examples::

    autotools.configure()
    autotools.configure("--with-libusb")


rawConfigure
------------

::

    rawConfigure(parameters)

Configures the package according to the parameters given by the user.

Examples::

    autotools.rawConfigure()
    autotools.rawConfigure("--prefix=/usr --libdir=/usr/lib --with-doxywizard")
    autotools.rawConfigure("--enable-nls --enable-freetype --disable-xmltest) 


compile
-------

::

    compile(parameters)

Compile the package with default GCC binutils, C flags and the parameters given
by the user.

Example::

    autotools.compile("-I/usr/include/dvdread -o dvdbackup src/dvdbackup.c -ldvdread")


make
----

::

    make(parameters)

Builds the package according to the parameters given by the user.

Examples::

    autotools.make()
    autotools.make("local-all")
    autotools.make("LIBS=%s" % get.LDFLAGS())
    autotools.make("-j1") 


install
-------

::

    install(parameters)

Install the package according to the parameters given by the user and PISI's
default parameters.

Examples::

    autotools.install()
    autotools.install("libdir=%s/usr/lib" % get.installDIR())


rawInstall
----------

::

    rawInstall(parameters)

Install the package according to the parameters given by the user.

Exmples::

    autotools.rawInstall("DESTDIR=%s" % get.installDIR())
    autotools.rawInstall("DESTDIR=\"%s\" docdir=/usr/share/doc/%s/html" % (get.installDIR(), get.srcTAG())) 


aclocal
-------

::

    aclocal(parameters)

Creates an aclocal.m4 file according to the configure.in file.

Examples::

    autotools.aclocal("-I cmulocal -I config")
    autotools.aclocal("-I m4")
    autotools.aclocal()


autoconf
--------

::

    autoconf(parameters)

Creates the configure script, with given parameters.

Example::

    autotools.autoconf()


autoreconf
----------

::

    autoreconf(parameters)

Recreates the configure script with given parameters.

Example::

    autotools.autoreconf()


automake
---------

::

    automake(parameters)

Creates the makefile with given parameters.

Examples::

    autotools.automake("-afc")
    autotools.automake("--add-missing")
    autotools.automake() 


autoheader
----------

::

    autoheader(parameters)

Creates the header file for the configure script.

Examples::

    autotools.autoheader()
