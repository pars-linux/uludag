.. _packaging-guidelines:

Packaging Guidelines
====================

**Last Modified Date:** |today|

:Author: Semen Cirit

:Version: 0.6

During package reviews the reviewer and the packager should deal with the above issues. They make sure that the package in review require a package or can be worked on after these packages is in the repository.

Please remember that any package that you submit must also conform to the Review Guidelines.

Naming
------

You should go through the :ref:`package-naming` to ensure that your package is named appropriately.

Binary Package Naming
---------------------

The proper way to use the Version and Release fields can be found here: :ref:`binary-package-naming`.

Legal
-----

Legal concerns about Pardus Linux Distribution package licensing can be found below.

Licensing
^^^^^^^^^

You should review :ref:`licensing-guidelines` to ensure that your package is licensed appropriately.

Proprietary Dependencies for Package
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Some software depends on other software. These dependencies sometimes can be non-free, legally unacceptable, or binary only (with the exception of permissible firmware), then they are not acceptable for the distribution, depending on this the dependent software is also inacceptable.

Pre-built binaries or libraries not allowed
-------------------------------------------

Every package has a source code and all program binaries and program libraries included in packages must be built from source code.

This is a requirement for the following reasons:

    #. The libraries and binaries that are not built from the source code can be a security concern. The patching of these files is also inacceptable.
    #. If these packages compiled also from the source code, these compiled ones should be taken, the ancient ones probably are not compatible with security and optimization rules that are produces with Pardus standart flags.

        The above can be helpful in order to say a file is library or binary:

        #. Is it executable? If so, it is probably a program binary.
        #. Does it contain a .so, ,so.#, or .so.#.#.# extension? If so, it is probably a program library.
        #. If in doubt, ask the reviewer.

    #. It is not permitted to compile source code has some non-open source part or it needs a propriatary compiler.

If a prebuilt binary in a package you MUST:

    * Write related code in actions.py in order to remove all these pre-built program binaries and program libraries. Examples include, but are not limited to, .class, .dll, .DS_Store, .exe, .jar, .o, .pyc, .pyo, .egg, .so files.
    * Ask upstream to remove the binaries in their next release.

Exceptions
^^^^^^^^^^

    * Some binary firmwares can be used, when it meets the `Licensing Guidelines`_ requirements.
    * Content binaries (such as .mo, .pdf, .png, .ps files) are not required to be rebuilt from the source code.

Creating a package from scratch
-------------------------------

When creating a package from scratch, you should follow the instructions of :ref:`howto-create-pisi-packages`. You should put aside your own experiences about packaging and formats and try to conform to this document as much as possible.


Modifying Existing Package
--------------------------

Modification on packages can exist in such situations: updating, bug fixing, renaming/replacing existing packages etc.


During Modifications particularly you should take care:

#. Verify that any source and patches is necessary for the package and applicable.
#. Verify that existing package licence matches with the current license of the software.
#. Revise the summary and description for typos and oddities. Look `Summary and Description`_
#. Control that the current software has new dependencies or ignore ancient ones.
#. Revise that the package use relevant pisi actionsapi instead of pure python api's. (Look :ref:`actionsapi-index`)

Architecture Support
--------------------

Pardus support two different architechtures (x86 (32 bit), x86_64 (64 bit)), packages must successfully compile and build into binary pisis on at least one supported architecture. If the package could not be compile for a specific architecture it should be specified in `pspec.xml file`_.

Build Package For a Special Architecture
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

More than one pacakge can be created from the same source code and some of these pacakges can need special architecture and buid dependency to build. In this kind of a situation, the build architecture type and dependencies can be given for relevant packages in `pspec.xml file`_ and this type can be parsed by `buildTYPE`_ () method in actions.py file.

pspec.xml Example::

   <Package>
    <Name>libfoo</Name>
    ...
    <Files>
      <Path fileType="library">/usr/lib</Path>
    <Files>
   </Package>

   <Package>
    <Name>libfoo-32bit</Name>
    <BuildType>32bit</BuildType>
    <BuildDependencies>
      <Dependency>libbar-32bit</Dependency>
    </BuildDependencies>
    ...
    <Files>
      <Path fileType="library">/usr/lib32</Path>
    <Files>
   </Package>

actions.py Example::

    if get.buildTYPE() == "32bit":
    # add -32 for LDFLAGS

Building Packages
^^^^^^^^^^^^^^^^^

Pardus Linux Distribution has a build system, buildfarm. Buildfarm is automatically build the packages. During building of a package automatically, all type of information send to buildfarm@pardus.org.tr list. These package messages send by its release and architecture types.

Type of massages send:

#. When a package is started to compile
#. When a package succesfully compiled
#. When a package does not succesfully compile


If a package does not succesfully compile, the error output is given as a link in the message.


Filesystem Hierarchy
--------------------

Pardus Linux Distribution follows `Filesystem Hierarchy Standard`_ in order to define where files should be placed on the system.

Some exeptions can be found such as "libexec". Any information is given about libexec, but Pardus stores programs that are designed primarily to be run by other programs rather than by users. (exp: /usr/libexec on Pardus)

Package Commit Hook
-------------------

When a wrong format is used in the pspec.xml file, `package SVN commit hook`_ captures this error and gives the related warning.


Some Errors:
^^^^^^^^^^^^
* invalid version
* bad release number
* invalid date
* package name has invalid char
* out of order release numbers
* this is a duplicate source package of
* this source has duplicate binary package
* package depends on missing package


History Comments
----------------

Every time you make changes, that means whenever you increment a package release, you must add a history comment. (look :ref:`howto-create-pisi-packages`) The repository commit message  also the same with the history comment. This is important because the other developers and also users can follow the changes.

Therefore there are some restrictions while writing history comments

History comments and commit messages:

#. Should be in English
#. Should be short and descriptive
#. Max 80 character long
#. If a comment has multi-line description, the format like below:

::

    <Comment>
        General summary:
        - description 1
        - description 2
        .
        .
        .
    </Comment>

#. If your changes closes or affects bugs of our bugzilla or an external bugzilla, the format like below:

::

    <Comment>
        - description 1
        - description 2
        - Fixes bugs (pb#9021, pb#9038, pb#9020, pb#4113, pb#9089, pb#8811, pb#8361, pb#9101, pb#8845, pb#8123, pb#6157, pb#9156, pb#9083)
    </Comment>


The bug format changes according to bugzilla source:

    - If the bug is in Pardus Bugzilla, the comments about this bug referenced with only "#" and the bug number.
    - If the bug is in external bugzillas, the comments contains used bug references of relevant bugzillas:
        - KDE bugs kde#<bugnumber>
        - Redhat bugs rhbz#<bugnumber>
        - SUSE bugs bnc#<bugnumber>
        - Pardus bugs pb#<bugnumber>
        - Launchpad lp:<bugnumber>
        - freedesktop.org  fdo#<bugnumber>
        - bugzilla.novell.com bnc#<bugnumber>

Buildtime Dependencies
----------------------

In package development and testing, please verify that your package is not missing any necessary build dependencies. Having proper build requirements saves the time of all developers and testers as well as autobuild systems because they will not need to search for missing build requirements manually.

Buildtime dependencies is also important to use programs full-featured. For example, an application special support may be excluded because of an absent build dependency.

The best way to find exact buildtime dependencies is to build the package in a proper system. You can use virtual systems in order to manage proper systems.

Runtime Dependencies
--------------------

Runtime dependencies is important in order a program run properly. You can check your runtime dependencies with `checkelf script`_.  You can find proper runtime dependencies, undefined symbols,  if you run it on a proper system.

You can find the usage from :ref:`checkelf`.

Strict Dependencies
-------------------

Strict dependencies can be needed in some cases:

#. If a package needs a exactly specific version "version" attribute is used.

    **Example:**
    ::

        <Dependency version="3.1.4">module-virtualbox</Dependency>

#. If a package needs one of the below versions of a package "versionTo" attribute is used. It is generally used for conflicting packages.

    **Example:**
    ::

         <Conflicts>
         <!-- /usr/kde/4/share/apps/kdevappwizard/templates/qmake_qt4guiapp.tar.bz2 file is common till 3.9.95 -->
            <Package versionTo="3.9.94">kdevelop</Package>
         </Conflicts>

#. If a package needs one of the above versions of a package "versionFrom" attribute is used.

    **Example:**
    ::

        <Dependency versionFrom="1.0.20">alsa-headers</Dependency>

#. Sometimes "versionFrom", "versionTo" or "version" are not enough for strict dependencies, for example a package needs only a patch in order to depend a package while its version can remain the same. At this time we need to use release numbers:
    #. If a package needs a exactly specific release "release" attribute is used.

         **Example:**
         ::

             <Dependency release="130">kernel-module-headers-pae</Dependency>

    #. If a package needs one of the below releases of a package "releaseTo" attribute is used. It is generally used for conflicting packages.

        **Example:**
        ::

            <Conflicts>
                <Package releaseTo="5">gwenview-i18n</Package>
            </Conflicts>


    #. If a package needs one of the above releases of a package "releaseFrom" attribute is used.

        **Example:**
        ::

            <Dependency releaseFrom="27">x264</Dependency>


#. If more than one package are produced from same source (same pspec.xml) and some of the packages in that source depend each other. Pardus use value "current" for the strict release or version tags, in order to automatically assign the release or version number of the needed package.

    **Example:**
    ::

        <Dependency release="current">freetype</Dependency>
        <Dependency version="current">git</Dependency>


Any Dependency
--------------

In some cases the dependency of the package can related to the system, in other words due to some hardware differences package can depend different packages. In these type of cases the <AnyDependency> tag is used  for runtime dependencies in pspec.xml.

**Example:** If the system has a pae support the module-pae-kvm package will be installed, if not module-kvm package will be installed.

    ::

     <AnyDependency>
         <Dependency>module-kvm</Dependency>
         <Dependency>module-pae-kvm</Dependency>
     </AnyDependency>


Dependencies Excepted
---------------------

Generally there are no need to include following dependencies as buildtime dependencies because these packages are considered as minimum build environment:

::

    autoconf
    automake
    binutils
    bison
    catbox
    ccache
    chrpath
    cmake
    dietlibc
    diffstat
    gcc
    gmp
    gnuconfig
    icecream
    intltool
    klibc
    libpthread-stubs
    libsigsegv
    libtool
    m4
    make
    mpfr
    nasm
    patch
    pkgconfig
    quilt
    scons
    swig
    unifdef
    util-macros
    xcb-proto
    xorg-proto
    xtrans
    yacc
    yasm

But any package above may have a dependency in each other.

Summary and Description
-----------------------

The summary should be a short and concise description of the package. The summary should not include the name of the package.

Description Hints
^^^^^^^^^^^^^^^^^
#. The description expands upon summary.
#. Do not include installation instructions in the description; it is not a manual.
#. Please make sure that there are no lines in the description longer than 80 characters.

The description and summary should be in English. Please also include in translations.xml file summary and description translations of other languages supported by Pardus that you know.

Code Legibility
---------------

The packages source code must be legible. The package reviewer can simply read the codes.

Taking SHA-1 Hash
-----------------

In order to verify integrity of packages, `SHA-1`_ hash is used. This has code is added <Archive> tag in pspec.xml.

In order to take the package hash, we need to download the souce code archive of the package and run the below command:

::

    sha1sum source_code_archive

Giving Mirrors
--------------

In order to download source code of the package, the link is included between <Archive> tag in pspec.xml. We generally use mirrors for dowload links. The common mirrors used for Pardus are included in /etc/pisi/mirrors.conf file. You can find the relevant mirror from this file and can use it with "mirrors:" prefix (Found the used mirror value in /etc/pisi/mirrors and removed it from the download link and add  "mirrors:" prefix.).

Example::

    http://ftp.gnu.org/gnu/freefont/freefont-sfd-20090104.tar.gz (The download link)
    mirrors://gnu/freefont/freefont-sfd-20090104.tar.gz (with mirror prefix)



Documentation
-------------

Any necessary documentation included in the source package, excluded build instructions, INSTALL file, documentations for non-Linux systems etc. API documentations generally are splitted from the package and get name packagename-devel. Or they also are splitted to a new package as packagename-doc.

The documentation files is also placed under "/usr/share/doc/packagename". For some packages the documents are placed under "/usr/share/doc/packagename-version" automatically, you should move these files under "/usr/share/doc/packagename".


Devel Packages
--------------

If the software has some files solely for development, those files should be put in a packagename-devel subpackage. The header files and unversioned shared libraries should be in packagename-devel package.

The pkgconfig files generally used for developement, so they should be included in a packagename-devel package. But for example if the base package is a developement tool it can be included in base package.

Compiler Flags
--------------

Package configuration need applicable compiler flags are set in order to be built. During the package build these flags are used for optimization, linking, security, small register usage, specific architectures etc. You can see 

Debug packages
--------------

Debug packages are very usefull in order to track a problem, because they have special symbols to generate `stack traces`_. Therefore exact line number of the source file where things went wrong can be seen simply. There exist compiler CFLAGS_ and LDFLAGS_ on Pardus.

Shared Libraries
----------------

Shared libraries are libraries that are loaded by programs when they start. When a shared library is installed properly, all programs that start afterwards automatically use the new shared library. The approach used by Linux permits you to:

    * update libraries and still support programs that want to use older, non-backward-compatible versions of those libraries
    * override specific libraries or even specific functions in a library when executing a particular program
    * do all this while programs are running using existing libraries

Whenever possible (and feasible), Pardus Packages containing libraries should build them as shared libraries.

Static Libraries
----------------

The static libraries should not be included in packages, but they may have some exceptions. The applications that links against static libraries should as far as possible link against shared versions by configuring with --disable-static.

.la libtool archives  should not be included in packages. Packages that produce .la files while building with --disable-static configuration parameter, thay may need to be removed from the packages after build. ın some circumstances programs may need these files and it is not possible to remove them. This should be fixed in the source code of the program.


Duplication of system libraries
-------------------------------

A local copy of the library that already exists on the system should not be included or build against by a package. The package should be patched to use the system libraries. The security and high priority bugs related to system libraries can directly be fixed thanks to this. Some packages may be granted an exception to this. (Please contact with `developer mail list`_ for further questions.)

.. Configuration files
.. -------------------

.. Initscripts
.. -----------

Desktop files
-------------

When a package has a GUI application, then it needs to include a .desktop file. While creating a .desktop file,  please pay attention for correct usage of Name, GenericName, Categories.

.desktop File Format
^^^^^^^^^^^^^^^^^^^^
If the pacakge does not have its own .desktop file, you need to make your own. You need to create and put it under "files" directory of the pacakage. The name format of the .desktop will be packagename.desktop. The format is like the below:

::

    [Desktop Entry]
    Encoding=UTF-8
    Name=gdpc
    Comment=Show Molecular Simulations
    Comment[tr]=Moleküler Simulasyonları Gösterir
    GenericName= Molecular Simulation Showing Tool
    GenericName[tr]= Moleküler Simulasyon Aracı
    Exec=gdpc
    Icon=gdpc.png
    StartupNotify=false
    Terminal=false
    Type=Application
    Categories=Qt;KDE;Education;Science;

Add icon and .desktop File as a Additional File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The desktop icon and the .desktop file path should be gived in the pacakge. In Pardus packaging format it can be gived as an additional package in pspec.xml file.

::

    <AdditionalFiles>
            <AdditionalFile owner="root" permission="0644" target="/usr/share/pixmaps/gdpc.png">gdpc.png</AdditionalFile>
            <AdditionalFile owner="root" permission="0644" target="/usr/share/applications/gdpc.desktop">gdpc.desktop</AdditionalFile>
    </AdditionalFiles>


Handling Locale Files
---------------------

Packages sometimes include translations. If it has translations in source code by default, it does not need to make additional changes in package scripts. If a package has an external translation file, you need to add it as a patch or additional file. If you add as an additional file, you need to put it the source part in pspec.xml.

Parallel make
-------------

Parallel make is genereally useful to speed up builds. If you want to build your packages with support parallel make, you need to change the "jobs"  parameter as "-j3" of /etc/pisi/pisi.conf file in your system.

Content of a Package
--------------------

The contents in the package should enhance the user experience. Therefore fonts, themes, clipart, and wallpaper etc., which are freely distributable, and have not offensive, discriminatory, or derogatory content are allowed.

Conflicting Packages
--------------------

Pardus packages should avoid conflicting with each other and as a Pardus package maintainer, we try to make both packages will install and run. But this is not always possible, so we let the user to decide which package to enable when they install the new package.

Therefore  <`Conflicts`_> tag is used, for the conflicting packages. And dependencies should not be confused with the conflicts. If the software links to the libraries of another package or the software does not function properly without another package, it must use <`Dependency`_> instead of <`Conflicts`_> to mark that dependency.


Conflicting Files
-----------------

There are many types of files which can conflict between different packages. Most of the problems can be resolved using <`Conflicts`_>. But some other cases can also be used for specific files without using <`Conflicts`_> tag. Some file names can be renamed, symbolic links can be used etc.


Symlinks
--------

When you want to easily access folders and files from different folders without maintaining duplicate copies, the symbolic links can be used.


Renaming/replacing existing packages
------------------------------------

Sometimes it is necessary to rename or replace an existing package. The new pacage(s) should make the change without user intervention.

If a package is renamed without any functional changes or package(s) replace with an existing package, the necessary changes should be made on relevant files:


    * The package(s) that will not exist after the changes, should be tagged between  <Obsoletes> </Obsoletes>  in distribution.xml file as below:

    ::

        <Obsoletes>
        <!--A comment should be gived for package(s) that removed from repository-->
            <Package>oldpackage</Package>
            .
            .
            .
        </Obsoletes>
    ::

        Example:
          <!-- Replaced by texlive-core  texlive-latex texlive-latexextra texlive-latexrecommended texlive-omega -->
          <Package>tetex</Package>

    * The obsoleted packages in distribution.xml should be added under below information:

    ::

            <!--
            ************************************************************
            not gone to binary stable yet, please don't remove this mark
            ************************************************************
            -->

    * The new packages' pspec.xml file should include the old package(s) that are renamed or replaced. The format of this change:

    ::

         <Replaces>
            <Package>oldpackage</Package>
            .
            .
            .
         </Replaces>

    ::

        Example:
         <Replaces>
            <Package>tetex</Package>
            <Package>tetex-texmf</Package>
            <Package>tetex-extra</Package>
         </Replaces>

Package Setup, Post Install, Post and Pre Remove, Cleanup  and Post Cleanup
---------------------------------------------------------------------------

Some packages need special operation before or after they installed. Pardus handles this situation with COMAR scripts. There are two scripts used for these operations in pisi packages, (package.py and pakhandler.py)

If the operation effects only a specific package, package.py is used. This script settles down /var/db/comar3/scripts/System.Package. When it recieve an operation about that package, it applies the related operation followed in the script.


If an operation effects the packages that installed after a specific package, pakhandler.py is used for that package. This script settles down under /var/db/comar3/scripts/System.PackageHandler and search packages for a specific rule and apply the related operation followed in the script.


Operation types:
^^^^^^^^^^^^^^^^

- setupPackage: Execute package handler setup scripts
- cleanupPackage: Execute package handler cleanup scripts before installation
- postcleanupPackage: Execute package handler postcleanup scripts after installation
- postInstall: Execute post-install script of a package after installation
- preRemove: Execute pre-remove script of a package before installation
- postRemove: Execute post-remove script of a package after installation

Special Packages
----------------

Texlive Packages
^^^^^^^^^^^^^^^^

Texlive has special packaging rules these can be found from `texlive packaging`_.

.. _stack traces: http://developer.pardus.org.tr/guides/bugtracking/stack_traces.html
.. _CFLAGS: http://developer.pardus.org.tr/guides/releasing/bootstrapping.html#c-compiler-flags-cflags
.. _LDFLAGS: http://developer.pardus.org.tr/guides/releasing/bootstrapping.html#linker-flags-ldflags
.. _Licensing Guidelines: http://developer.pardus.org.tr/guides/licensing/licensing_guidelines.html#binary-firmware
.. _pspec.xml file: http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html#different-pspec-xml-file-tags
.. _Filesystem Hierarchy Standard: http://www.pathname.com/fhs/
.. _package SVN commit hook: http://svn.pardus.org.tr/uludag/trunk/scripts/repokit/src/ismail2.py
.. _checkelf script: http://svn.pardus.org.tr/uludag/trunk/scripts/checkelf
.. _SHA-1: http://www.w3.org/PICS/DSig/SHA1_1_0.html
.. _developer mail list: http://liste.pardus.org.tr/mailman/listinfo/gelistirici
.. _Conflicts: http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html#different-pspec-xml-file-tags
.. _Dependency: http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html#different-pspec-xml-file-tags
.. _buildTYPE: http://developer.pardus.org.tr/guides/packaging/actionsapi/get.html#buildtype
.. _texlive packaging: http://developer.pardus.org.tr/guides/packaging/texlive_packaging.html
