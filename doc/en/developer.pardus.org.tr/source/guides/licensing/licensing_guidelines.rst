.. _licensing-guidelines:

Licensing Guidelines
~~~~~~~~~~~~~~~~~~~~

The aim of Pardus Linux Distribution is to create a complete, general purpose operating system entirely from Free and Open Source software.

Package Licensing Guidelines
============================

The software which is approved by `Free Software Foundation <http://www.gnu.org/licenses/license-list.html>`_ and has a licence under `Licence List <http://svn.pardus.org.tr/uludag/trunk/doc/en/licenses/>`_, can be exist under Pardus Project repositories.

Licence File
------------

The package source code must include its own licence file. This file must be added as a document in the pisi package under /usr/share/doc/<package-name>. If the source code does not include this file, the package maintainer should inform upstream about that mistake.

Splitted Package Licensing
^^^^^^^^^^^^^^^^^^^^^^^^^^

If a package is splitted into subpackages (docs, development files, libraries etc.), and is dependent upon a base package, there is no need to add same licence file into the pisi package for the spiltted package.

License Tag
-----------

Every pisi package has a Licence tag. The contents of the Licence tag are specific for each licence of the packages. The licence field is refer to the licences of pisi package. Maintainers should ask the experienced maintainers for the licence, when in doubt.

Valid License Abbreviations
^^^^^^^^^^^^^^^^^^^^^^^^^^^

License tag must be filled with the appropriate abbreviation of the licence which is listed `here <http://svn.pardus.org.tr/uludag/trunk/doc/en/licenses/>`_. If the licence of your package is not in the list, you should ask it to `Pardus developer list <http://liste.pardus.org.tr/mailman/listinfo/pardus-devel>`_. If the licence is suitable with Pardus Licencing, it will put under this list and also the abbreviation also added to `pisi rng file`_.

Versioned licenses
^^^^^^^^^^^^^^^^^^

Sometimes licences has version, and while a version of a package has is compatible with the old licence, the other version may compatible with the later one. So the maintainers should be careful also about the versions of the licenses. The versioned licence abbreviations also found in `Licence List <http://svn.pardus.org.tr/uludag/trunk/doc/en/licenses/>`_.

Multiple Licensing
^^^^^^^^^^^^^^^^^^

Sometimes packages have more than one licenses distinct and independent from other, maintainers should also take into account this option. If a pacakage has more than one license, for each licence the Licence tag should be added.

Software Types
==============

Some specific software types are examined from a licensing/legal perspective.

Shareware
---------

Shareware applications also known as trialware or demoware have not Open Source code, they refer to proprietary software that is provided to users without payment on a trial basis and is often limited by any combination of functionality, availability  or convenience. These type of software are not acceptable for Pardus repositories.

Emulators
---------

If the emulator needs ROMs or any image files copyrighted which have not any freely redistributable permission written by their owners, then it is not permitted in Pardus Repositories.

Binary Firmware
---------------

Some hardware or drivers may need some binary-only software, if below requirements are provided, these software can include in Pardus repositories:

    * The files of this software are under an accaptable firmware licence
    * The files are non-executable
    * The files are not libraries
    * The files are standalone, not embedded in executable or library code
    * The files must be necessary for the functionality of open source code being included in Pardus and there is not any open source alternative.

A firmware licence is acceptable for Pardus if it allows some form of royalty-free use and it does not restrict redistribution.

The redistribution restrictions for firmware that acceptable by Pardus Licensing:

    * requiring that the firmware be redistributed only as incorporated in the redistributor's product
    * prohibitions on modification
    * prohibitions on reverse engineering, disassembly or decompilation
    * restricting to use in conjunction with the hardware associated with the firmware license

If the maintainer unsure about the firmare licence, he can ask `Pardus developer list <http://liste.pardus.org.tr/mailman/listinfo/pardus-devel>`_, and the other experienced maintainers will examine this.

**Last Modified Date:** |today|

:Author: Semen Cirit


.. _pisi rng file: http://svn.pardus.org.tr/uludag/trunk/pisi/pisi-spec.rng
