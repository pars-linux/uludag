.. _reviewing-guidelines:

Things To Check While Reviewing
===============================

**Last Modified Date:** |today|

:Author: Semen Cirit

:Version: 0.2

In order to review a new package, there are a lot of things to check. The below
list only provides some guidelines for new rewievers in order to identify a way
to follow. But of course this list is not enough. Reviewers should also use their
own experiences when reviewing a package.

    #. The package name must be suitable to `package naming`_.
    #. The package must meet the `packaging guidelines`_.
    #. The package must meet `licensing guidelines`_.
    #. The license tag in the pspec.xml file must match the actual `license short names`_.
    #. The source code of the package and comments must be written in `english`_.
    #. The source code of the package must be `legible`_.
    #. The package must successfully compile and build into pisi for at least one `architecture supported`_.
    #. If the package could not successfully compile, build or work on a specific architecture, then those architectures should be specified in pspec.xml file with `ExcludeArch tag`_.
    #. All `build dependencies`_ must be listed in `pspex.xml file`_, except for any that are listed in the `dependencies excepted document`_.
    #. The `translations.xml file`_ must be added to package. 
    #. Almost every pisi package (or subpackage) have shared library files, you must run `checkelf`_ for every package and find broken links.
    #. Packages must not `bundle copies`_ of system libraries.
    #. Permissions on files must be set properly. Executables should be set with executable permissions, See `Additional Files`_.
    #. Each package must use related actionsapi modules rather than recreating similar modules in `main`.
    #. Package must contain code, or `permissable content`_.
    #. If the size or the quantity of the `documentation files`_ are large, they must go in a packagename-doc subpackage.
    #. `Header files or unversioned shared libraries`_ must be in a packagename-devel subpackage.
    #. `Libtool archives`_ .la must not be included in packages, these must be removed in the actions.py if they are built.
    #. The GUI application pacakges must contain `packagename.desktop file`_, and the `icon tag`_ of this application should also be defined in pspec.xml file.
    #. The reviewer should test the package in a related proper Pardus system.
    #. The reviewer should test that the application runs as described. For example the applcation should not be crashed or give a segfault.
    #. Usually, subpackages require the base package as a dependency, it should be defined as a `strict dependency`_ for subpackages as needed.
    #. `Pkgconfig(.pc)`_ situation should be examined and their package placement should be decided. 

.. _package naming: http://developer.pardus.org.tr/guides/packaging/package_naming_guidelines.html
.. _packaging guidelines: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html
.. _licensing guidelines: http://developer.pardus.org.tr/guides/licensing/licensing_guidelines.html
.. _license short names: http://svn.pardus.org.tr/uludag/trunk/doc/en/licenses/
.. _english: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#summary-and-description
.. _legible: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#code-legibility
.. _architecture supported: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#architecture-support
.. _ExcludeArch tag: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#architecture-support
.. _pspex.xml file: http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html#different-pspec-xml-file-tags
.. _build dependencies: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#buildtime-dependencies
.. _dependencies excepted document: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#dependencies-excepted
.. _translations.xml file: http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html#creating-translations-xml
.. _bundle copies: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#duplication-of-system-libraries
.. _Additional Files: http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html#different-pspec-xml-file-tags
.. _permissable content: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#summary-and-description
.. _documentation files: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#documentation
.. _Header files or unversioned shared libraries: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#devel-packages
.. _Libtool archives: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#static-libraries
.. _packagename.desktop file: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#desktop-files
.. _icon tag: http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html#different-pspec-xml-file-tags
.. _strict dependency: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#strict-dependencies
.. _Pkgconfig(.pc): http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#devel-packages
.. _checkelf: http://developer.pardus.org.tr/guides/packaging/checkelf.html
