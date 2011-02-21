.. _get:

Get
~~~

:Author: Semen Cirit
:Date: |today|
:Version: 0.1


Global Functions
================

curDIR
-------

::

    get.curDIR()

Returns current work directory's path.


curKERNEL
---------

::

    get.curKERNEL()

Returns currently running kernel's version.


curPYTHON
---------

::

    get.curPYTHON()

Returns currently used python's version.


curPERL
-------

::

    get.curPERL()

Returns currently used perl's version.

ENV
---

::

    get.ENV(environ)

Returns any given environ variable.

Example::

    get.ENV("MAKE_DOC")
    get.ENV("LD_LIBRARY_PATH")

PISI Related Functions
======================

pkgDIR
------

::

    get.pkgDIR()

Returns the path of binary packages. Default is"/var/cache/pisi/packages".

workDIR
-------

::

    get.workDIR()

Returns the path of package work directory. For example it can return a path
like "/var/pisi/texlive-core-0.0_20091107-4/work".


installDIR
----------

::

  get.installDIR()

Returns the package install directory. For example it can return a path like
"/var/pisi/texlive-core-0.0_20091107-4/install"


Pardus Release Related Functions
================================

lsbINFO
-------

::

    get.lsbINFO()

Returns a dictionary filled through /etc/lsb-release.

PSPEC Related Functions
=======================


srcNAME
-------

::

    get.srcNAME()

Returns the name of source package. (i.e. flashplugin)


srcVERSION
----------

::

    get.srcVERSION()

Returns the version of source package. (i.e. 5.2_p1, 10.1.82.76)


srcRELEASE
----------

::

    get.srcRELEASE()

Returns the release number of source package. (i.e. 28)


srcTAG
------

::

    get.srcTAG()

Returns the name, version and release number of source package. (i.e. 5.2_p1-28)


srcDIR
-------

::

    get.srcDIR()

Returns the directory name of the package source under "/var/pisi/".
(i.e. teeworlds-0.5.2)

Build Related Functions
=======================

ARCH
----

::

    get.ARCH()

Returns the default arch value written at
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/configfile.py" in class
GeneralDefaults. (i.e i686)

HOST
----

::

    get.HOST()

Returns the default host value written at
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/configfile.py" in class
BuildDefaults. (i.e i686-pc-linux-gnu)

CFLAGS
------

::

    get.CFLAGS()

Return the default cflags used for Pardus. You can see them from
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/configfile.py" in class
BuildDefaults.


CXXFLAGS
--------

::

    get.CXXFLAGS()

Return the default cxxflags used for Pardus. You can see them from
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/configfile.py" in class
BuildDefaults.


LDFLAGS
-------

::

    get.LDFLAGS()


Return the default ldflags used for pardus. You can see them from
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/configfile.py" in class
BuildDefaults.


makeJOBS
--------

::

    get.makeJOBS()


Return the default jobs value used for pardus. You can see it from
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/configfile.py" in class
BuildDefaults.

buildTYPE
---------

::

    get.buildTYPE()

Return the current build type included in pspec.xml with <BuildType> tag.


Directory Related Functions
===========================

docDIR
------

::

    get.docDIR()

Returns the default doc files directory used for Pardus. You can see it from
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/actionsapi/variables.py" in
class Dirs.

sbinDIR
-------

::

    get.sbinDIR()

Returns the default sbin directory used for Pardus. You can see it from
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/actionsapi/variables.py" in
class Dirs.


infoDIR
-------

::

    get.infoDIR()

Returns the default info files directory used for Pardus. You can see it from
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/actionsapi/variables.py" in
class Dirs.

manDIR
------

::

    get.manDIR()

Returns the default man files directory used for Pardus. You can see it from
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/actionsapi/variables.py" in
class Dirs.

dataDIR
--------

::

    get.dataDIR()

Returns the default data files directory used for Pardus. You can see it from
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/actionsapi/variables.py" in
class Dirs.

confDIR
-------

::

    get.confDIR()

Returns the default configure files directory used for Pardus. You can see it from
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/actionsapi/variables.py" in
class Dirs.


localstateDIR
-------------

::

    get.localstateDIR()

Returns the default locale files directory used for Pardus. You can see it from
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/actionsapi/variables.py" in
class Dirs.

libexecDIR
----------

::

    get.libexecDIR()

Returns the default library executable directory used for Pardus. You can see it from
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/actionsapi/variables.py" in



defaultprefixDIR
----------------

::

    get.defaultprefixDIR()

Returns the default prefix directory used for Pardus. You can see it from
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/actionsapi/variables.py" in
class Dirs.

kdeDIR
------

::

    get.kdeDIR()

Returns the default kde directory used for Pardus. You can see it from
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/configfile.py" in class
DirectoriesDefaults.

qtDIR
-----

::

    get.qtDIR()

Returns the default qt directory used for Pardus. You can see it from
"http://svn.pardus.org.tr/uludag/trunk/pisi/pisi/configfile.py" in class
DirectoriesDefaults.

Binutils Related Functions
==========================

AR
--

::

    get.AR()

Return GNU ar binutil executable variable of the system where the package being
compiled. (i.e. ar)

AS
--

::

    get.AS()

Return GNU assembler binutil executable variable of the system where the package being
compiled. (i.e. as)

CC
--

::

    get.CC()

Return gcc binutil executable variable of the system where the package being
compiled. (i.e. i686-pc-linux-gnu-gcc)

CXX
---

::

    get.CXX()

Return gcc C++ binutil executable variable of the system where the package being
compiled. (i.e. i686-pc-linux-gnu-g++)

LD
--

::

    get.LD()

Return GNU linker binutil executable variable of the system where the package being
compiled. (i.e. ld)


NM
--

::

    get.NM()

Return GNU nm binutil executable variable of the system where the package being
compiled. (i.e. nm)

RANLIB
------

::

    get.RANLIB()

Return ranlib binutil executable variable of the system where the package being
compiled. (i.e. ranlib)

F77
---

::

    get.F77()

Return GNU fortran compiler binutil executable variable of the system where the package being
compiled. (i.e. g77)


GCJ
---

::

    get.GCJ()

Return GNU java compiler binutil executable variable of the system where the package being
compiled. (i.e. gcj)

