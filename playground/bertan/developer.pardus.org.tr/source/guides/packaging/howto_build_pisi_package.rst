.. _building-pisi-package:

Howto Build PiSi Package
========================

**Last Modified Date:** |today|

:Author: Semen Cirit

:Version: 0.1

These are some guidelines in order to help new Pardus developers to get started with PiSi package building.

Structure of a PiSi Package
---------------------------

A pisi package is essentially a zipped file. Let's download one and examine it::

    $ wget http://packages.pardus.org.tr/pardus/2011/devel/x86_64/knazar-1.1-10-p11-x86_64.pisi
    $ unzip knazar-1.1-10-p11-x86_64.pisi -d package
      Archive:  knazar-0.2-3-3.pisi
      inflating: apackage/metadata.xml
      inflating: apackage/files.xml
      inflating: apackage/install.tar.lzma
    $ cd package
    $ ls
      files.xml  install.tar.xz  metadata.xml

``files.xml`` contains locations, types, sizes and sha1sums of all files in the package.
``metadata.xml`` contains general information like package name, homepage, packager, etc.
``install.tar.lzma`` contains compressed files which will be installed under the system.

::

    $ xz --decompress install.tar.lzma
    $ tar xvf install.tar

Building PiSi Package
---------------------

In order to build a pisi package we need to prepare at least three files by hand:
pspec.xml_ and actions.py_ and translations.xml_.

The pspec.xml_ file provides information about the software being packaged. The
actions.py_ file includes the scripts in order to build the package. The
translations.xml_ file has the summary and description translations for different
languages supported for the related release.

Additionaly some other directories can be needed in order to build a package: comar_
and files directory (see AdditionalFiles on additional-files_).

After preparing the package, you can build it with below command:
(You can look for the parameters given with "pisi bi --help")

::

    pisi bi pspec.xml -vd

PiSi package can be built in different stages:


  #. **--fetch:** Finish building after source archive is downloaded.
  #. **--unpack:** Finish building after source archive is decompressed and the
     patches are applied.
  #. **--setup:** Finish building after the configuration.
  #. **--build:** Finish building after compiling.
  #. **--check:** Finish building after testing.
  #. **--install:** Finish building after instllation of the package.
  #. **--package:** Creating the .pisi file

This different stages enable to build the package progressively. For instance
if building of a package takes too long, and you now that you have experienced
with an error on installation step. You can only run the package from that step
and you can gain time.

After the unpack step, the package is unpacked under ``/var/pisi/<packagename>``
on your system and a work directory is created under it. This directory has a
pisiBuildState file which includes the current build state and the source code
of the package.

After the installation step the install directory is also created under
``/var/pisi/<packagename>`` directory. This directory has the files that will
be installed under a Pardus system when the package is installed.

After the packaging step the files.xml and metadata.xml files are also created
under ``/var/pisi/<packagename>``.

.. _pspec.xml: http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html#creating-pspec-xml
.. _actions.py: http://developer.pardus.org.tr/guides/packaging/actionsapi/index.html
.. _translations.xml: http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html#creating-translations-xml
.. _comar: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#package-setup-post-install-post-and-pre-remove-cleanup-and-post-cleanup
.. _additional-files: http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html#different-pspec-xml-file-tags
