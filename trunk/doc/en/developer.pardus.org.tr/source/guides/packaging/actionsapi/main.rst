.. _main:

About the document
==================

:Author: Semen Cirit
:Date: |today|
:Version: 0.1

One of the main part of pisi package is actions.py is. It is a python script
that contains information of the operations to be executed on the source code.
This document is an overview of the Actions API library which includes the
functions that are available for use in actions.py scripts.

Actions API
-----------

Actions API has a modular structure that makes the packaging process easier for
the packager. The major modules of the Actions API are:

    * :ref:`autotools`:  Standard functions for building and installing applications.
    * :ref:`cmaketools`: Functions for building the applications that are configured with cmake.
    * :ref:`get`: Functions for getting information about evnironment variables or packages needed in building and installation phases.
    * :ref:`libtools`: Pre-build and post-build operations for configuring libraries.
    * :ref:`kde`:_ Functions for configuring, building and installing KDE applications.
    * :ref:`kde4`: Functions for configuring, building and installing KDE applications.
    * :ref:`kerneltools`: Functions for configuring, building and installing kernel and kernel modules.
    * :ref:`pisitools`: Fundamentally used for moving files to install directory from work directory, the functions included in pisitools are convenient for most operations i.e. symlinking, file manipulation via sed, deleting files or directories.
    * :ref:`perlmodules`: Functions for configuring, building and installing perl modules.
    * :ref:`pythonmodules`: Functions for configuring, building and installing python modules.
    * :ref:`qt4`: Functions for configuring, building and installing Qt4.
    * :ref:`rubymodules`: Functions for configuring, building and installing ruby modules.
    * :ref:`scons`: Counterpart of autotools for the new generation building tools, scons.
    * :ref:`shelltools` Functions for specific operations. Apart from pisitools, shelltools is capable of operating in absolute paths instead of relative paths. Granting the ability to operate in the darkest corners of the system to the packager shelltools has to be used responsibly.
    * :ref:`texlivemodules` Functions for configuring, building and installing texlive modules.

