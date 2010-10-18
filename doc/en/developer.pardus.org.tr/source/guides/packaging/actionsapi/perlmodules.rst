.. _perlmodules:

Perlmodules
===========

configure
---------

::

    configure(parameters)

Configures the perl source code with the given parameters.

Exmamples::

    perlmodules.configure("/usr")
    perlmodules.configure()


make
----

::

    make(parameters)

Builds the perl source code with the given parameters.

Example::

    perlmodules.make()
    perlmodules.make("test")


install
-------

::

    install(parameters)

Installs the perl source code with the given parameters.

Example::

    perlmodules.install()

