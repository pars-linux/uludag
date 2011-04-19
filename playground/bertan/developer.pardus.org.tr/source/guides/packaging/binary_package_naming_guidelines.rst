.. _binary-package-naming:

Binary Package Naming
---------------------

**Last Modified Date:** |today|

:Author: Semen Cirit

:Version: 0.4

The binary packages in Pardus Linux Distribution have .pisi extention. The
pacakges with this format has a specific format. Generally between every unit,
'-' character exist.

Version Number
^^^^^^^^^^^^^^

Next to the package name, the version number exists. This version number should
be same with the upstream version. This information includes in pspec.xml file
under <History> tag with <Version>versionno</Version> format.

::

    packagename-versionno

Example:  ::

            gimp-2.6.8
            texlive-0.0_20080816

There exists also some suffix for some versioning systems and at this time the
versioning format change like

::

    versionno_suffixNumber

If the upstream version includes alpha, beta, pre, rc, milestone, patch-level
information they should be used as alpha, beta, pre, rc, m, p respectively in
versioning tag.

This versioning should be in this order p > (no suffix) > m > rc > pre > beta > alpha.

Example::

        gimp-2.6.8_alpha1
        gimp-2.6.8_beta2
        gimp-2.6.8_rc1
        gimp-2.6.8_p3
        gimp-2.6.8_m5

        2.6.8_p3 > 2.6.8_m5 > 2.6.8 > 2.6.8_rc1 > 2.6.8_beta2 > 2.6.8_alpha1

Release Number
^^^^^^^^^^^^^^

Next to the version number, the release number exists. This number is count the
update number of a package during all Pardus Linux Distribution releases. This
information includes in pspec.xml file under <History> tag with <Update release="releaseno">
format. For every package update the package maintainer should increase this number.

::

    packagename-versionno-releaseno

Example: ::
            gimp-2.6.8-26
            texlive-0.0_20080816-5

Distribution Abbreviation
^^^^^^^^^^^^^^^^^^^^^^^^^

Next to the release number the relevant distribution abbreviation also exists.
This abbreviationis important in order to determine for which Pardus Linux
Distribution the package is built.

::

    packagename-versionno-releaseno-distabbr

Example:    ::

       gimp-2.6.8-26-4-p11
       texlive-0.0_20080816-5-p11

Architecture
^^^^^^^^^^^^

Next to the distribution abbreviation, architecture information is given. This
information is important in order to determine the package build architecture.

::

   packagename-versionno-releaseno-distabbr-archabbr

Example:::

           gimp-2.6.8-26-4-p11-i686
           texlive-0.0_20080816-5-p11-x86_64
