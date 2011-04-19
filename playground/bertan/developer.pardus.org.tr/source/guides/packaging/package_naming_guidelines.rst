.. _package-naming:

=========================
 Package Naming Guideline
=========================

**Last Modified Date:** |today|

:Author: Fatih Aşıcı

:Version: 0.1

This document describes the package naming rules used in Pardus repositories.
If you think these guidelines are not sufficient to choose a name for your
package, please ask on developer mail lists.


---------------
 General Rules
---------------

This section describes the general naming rules. Things might change for
some package groups. These exceptions are described in the section titled with
"Rules Spesific to Some Package Groups".

Character Set
=============

All packages must be named using the following characters:

::

    abcdefghijklmnopqrstuvwxyz
    ABCDEFGHIJKLMNOPQRSTUVWXYZ
    0123456789-_+

Case Sensitivity
================

The preference of upstream maintainers must be respected. This means the case
preference in archive names must be kept in package names. e.g. For a python
module "Foo", "python-Foo" must be used.

Multiple Versions
=================

If multiple versions of a software will exist in the same repository, legacy
packages should reflect the version. The common to provide this is to append
major version numbers to the package name.

Example::

    The most recent version of qt:  qt
    3.x series of qt:               qt3

If multiple version levels are needed, seperate them with an underscore.

Example::

    4.4.x series:   docbook-sgml4_4
    4.5.x series:   docbook-sgml4_5

Addons
======

The main application/library (in other words parent application/library) name
must be followed by the component/addon name.

Example::

    Qt bindings for avahi:  avahi-qt (main package: avahi)

Some words may be added before component name. Following examples show these
words.

Examples::

    Consider "foo" as a main application name and "bar" as the name of an
    extension. One of the following names should be used for the extension
    package:

     - foo-bar
     - foo-addon-bar
     - foo-applet-bar
     - foo-backend-bar
     - foo-extension-bar
     - foo-plugin-bar


-------------------
 Splitted Packages
-------------------

For many reasons, it is useful to split packages whenever possible. This
section mentions the naming of sub-packages coming from the same source.

Development Files
=================

These are the packages containing files needed for building applications.
"-devel" suffix must be used for these packages.

Example::

    libX11-devel: libX11 headers and pkgconfig files

Libraries
=========

Sometimes it might be useful to separate libraries in one package. For these
packages "-libs" suffix must be used.

Common Files
============

If a sub-package is needed by other sub-packages and this package itself does
not provide a functionality, you can use "-common" suffix.

Example::

    php-common: PHP config files used by cli and apache module

Documentation
=============

Packages containg documentation files should be suffixed with "-docs".

Example::

    qt-docs: Qt documentation files

Suites
======

Some meta packages could be desired to install all sub-packages together. This
king of packages should be suffixed with "-suite".

Example::

    koffice-suite: Meta package which depends on all koffice applications

Localization Files
==================

Localization packages must be suffixed with "-l10n-xx" where xx is the locale
code.

Example::

    kde-l10n-tr: Turkish localization package for KDE


---------------------------------------
 Rules Spesific to Some Package Groups
---------------------------------------

Some package groups have their own rules for naming. This section describes
these exceptions for each group.

Apache Modules
==============

Packages containg Apache modules should use "mod\_" prefix. This naming scheme
is already used by many of the upstream maintainers.

Example::

    mod_php: PHP module for Apache

Cursor Themes
=============

For packages containg cursor themes "cursor-theme-" prefix must be used.

Example::

    cursor-theme-oxygen-zion: Oxygen Zion cursor theme

Django Modules
==============

The rules for Python packages do not apply for Django modules. These packages
must have a "django-" prefix in their names.

Example::

    django-tagging:     Tagging module for Django


Fonts
=====

Names of the font packages must end with "-fonts".

Example::

    dejavu-fonts

Icon Themes
===========

Names of the packages containg an icon theme must start with "icon-theme-".

Example::

    icon-theme-hicolor: Hicolor icon theme

KDE Styles
==========

KDE styles must be kept in packages whose names start with "kde-style-".

Example::

    kde-style-oxygen: Oxygen style for KDE

Kernel Modules
==============

Names of packages containing kernel modules must be prefixed with "module-x"
where x is the name of kernel flavor (pae, rt, etc.). If files needed by
userspace applications (such as udev and modprobe configurations) are also
needed, these must be separated with another sub-package whose name is also
suffixed with "-common".

Example::

    module-alsa:        ALSA kernel modules (kernel objects)
    module-alsa-common: udev and modprobe.conf files needed by ALSA drivers

KDE Thumbnailers
================

KDE thumbnailer packages must have a name prefixed with "kde-thumbnailer-".

Example::

    kde-thumbnailer-ffmpeg

KWin Decorations
================

KWin decoration packages must have a name prefixed with "kwin-decoration-".

Example::

    kwin-decoration-aurorae

Latex Packages
==============

Latex packages must have a prefix of "latex-" in their names.

Example::

    latex-mh: Additional LaTeX math tools

NSS Modules
===========

Packages containg NSS modules should use "nss\_" prefix. This naming scheme
is already used by many of the upstream maintainers.

Example::

    nss_ldap: NSS module for querying user information from LDAP

PAM Modules
===========

Packages containg PAM modules should use "pam\_" prefix. This naming scheme
is already used by many of the upstream maintainers.

Example::

    pam_ldap: PAM module for LDAP authentication

Pear Packages
==============

Pear packages must have a prefix of "PEAR-" in their names.

Example::

    PEAR-Net_Socket: Network Socket Interface

Perl Modules
============

Perl packages must have a prefix of "perl-" in their names.

Example::

    perl-YAML: YAML module for Perl

Plasma Applets
==============

For packages providing Plasma applets, "plasma-applet-" prefix must be used.

Example::

    plasma-applet-network: Network configuration plasmoid for Plasma

Python Modules
==============

If the upstream name includes the word "python", the package name is not
changed.

Examples::

    dbus-python:            Python bindings for dbus
    gnome-python-desktop:   Python bindings for GNOME desktop libraries

If the upstream name does not include the word "python" and the project is a
binding of another library, the library name with the prefix "python-" is
used as the package name. In this case, the upstream name must be included
in the package summary and description.

Examples::

    python-gtk:     Python bindings for GTK (pygtk)
    python-qt:      Python bindings for Qt (PyQt)

When the name does not comply with the rules above, "python-" prefix must be
added to the upstream name.

Examples::

    python-numpy:       The fundamental package needed for scientific computing
                        with Python
    python-FormEncode:  A validation and form generation package for Python
    python-pyaspects:   Aspect-Oriented development for Python

For modules built for Python3, "python3" must be used instead of the word
"python".

Examples::

    dbus-python3:           Python3 bindings for dbus
    gnome-python3-desktop:  Python3 bindings for GNOME desktop libraries
    python3-liblzma:        Python3 bindings for liblzma (pyliblzma)


R Modules
=========

R packages must have a prefix of "R-" in their names.

Example::

    R-mathlib: mathlib module for R


.. TeX Packages
.. ============

.. TeX packages must have a prefix of "tex-" in their names.

.. Example::

..     tex-basic: TeXLive Essential programs and files

