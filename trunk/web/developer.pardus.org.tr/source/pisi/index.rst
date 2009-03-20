.. _pisi-index:

######################
  Package Management
######################

:Date: |today|

PiSi
----

PiSi is the package manager for Pardus. It integrates all commands to build, retrieve and manage your packages in the distribution.

Command basics
--------------

All PiSi commands are invoked in the command-line trough the ``pisi`` executable. To explore or remind commands, and if you can only remember two, those are the essentials

.. code-block:: bash

    $ pisi help
    $ pisi some_command --help

The PiSi packages are located in repositories. You can add or remove them by command-line

.. code-block:: bash

    $ pisi lr
        pardus-2008
            http://paketler.pardus.org.tr/pardus-2008/pisi-index.xml.bz2

To install a package, just use ``pisi install`` as root. You can also install foreign packages but it is not recommended. When you give a package name, it will be looked up in the previously mentioned repositories

.. code-block:: bash

    $ sudo pisi install your_package
    $ sudo pisi install http://host.tld/path/package-ver.pisi

To remove a package, it works exacly the contrary

.. code-block:: bash

    $ sudo pisi remove your_package

.. toctree::

    pisi-structure.rst

