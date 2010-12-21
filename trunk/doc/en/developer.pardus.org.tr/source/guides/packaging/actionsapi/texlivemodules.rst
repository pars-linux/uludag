.. _texlivemodules:

Texlivemodules
==============

:Author: Semen Cirit
:Date: |today|
:Version: 0.1


compile
-------

::

    compile(parameters)

Compiles texlive packages with given parameters. It first moves tlpobj sources,
then it generatea configure files and builds format files.

install
-------

::

    install(parameters)

Installs texlive packages with given parameters. It fist creates symlinks for
the formats. Then it installs doc, config and texmf files to the system.


createSymlinksFormat2Engines
----------------------------

::

    createSymlinksFormat2Engines()

Creates symlinks for the engine names in /usr/texmf/fmtutil/format*.cnf files.

addFormat
---------

::

    addFormat()

Adds new formats created via new config files.

moveSources
-----------

::

    moveSources()

Moves unneccessary sources under /usr/share/tlpkg/tlpobj/ files.

buildFormatFiles
----------------

::

    buildFormatFiles()

Builds format files with running fmutil.

generateConfigFiles
-------------------

::

    generateConfigFiles()

Generates .cfg, -config, -config.ps, .def, .dat files.

makeLanguagesDefDatLines
------------------------

::

    makeLanguagesDefDatLines()

Add lines to .def and .dat files for each generated language.

installDocFiles
---------------

::

    installDocFiles()

Installs doc files of texlive packages.

installTexmfFiles
-----------------

::

    installTexmfFiles()


Installs Installing texmf, texmf-dist, tlpkg, texmf-var directories.

installConfigFiles
------------------

::

    installConfigFiles()

Installs .cfg, -config, -config.ps, .def, .dat files.

handleConfigFiles
-----------------

::

    handleConfigFiles()

Handles files ends with cfg or cnf and create their symbolic links.


