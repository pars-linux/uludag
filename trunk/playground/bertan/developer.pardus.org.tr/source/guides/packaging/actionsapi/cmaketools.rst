.. _cmaketools:

Cmaketools
==========

:Author: Semen Cirit
:Date: |today|
:Version: 0.1


configure
---------

::

    configure(parameters, sourceDir, installPrefix = '%s' % get.defaultprefixDIR())

Configures the source with the given cmake parameters.

Examples::

    cmaketools.configure()
    cmaketools.configure(installPrefix = "%s" % (get.kdeDIR()))
    cmaketools.configure("-DCMAKE_BUILD_TYPE=None -DKDEDIR=%s" % get.kdeDIR(), sourceDir = "..") 


make
----

::

    make(parameters)

Builds the source with the given parameters.

Example::

    cmaketools.make()
    cmaketools.make("LIBS=%s" % get.LDFLAGS())
    cmaketools.make("-j1") 


install
-------

::

    install(parameters, argument = 'install')

Installs the source with the parameters given by the user and PISI's default
parameters.

Example::

    cmaketools.install()
    cmaketools.install("libdir=%s/usr/lib" % get.installDIR()) 


rawInstall
----------

::

    rawInstall(parameters, argument = 'install')

Installs the source with the parameters given by the user.

Example::

    cmaketools.rawInstall("PREFIX=%s" % get.installDIR()) 


