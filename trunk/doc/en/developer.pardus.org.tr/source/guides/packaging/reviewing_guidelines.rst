.. _reviewing-guidelines:

Things To Check While Reviewing
===============================

**Last Modified Date:** |today|

:Author: Semen Cirit

:Version: 0.1

In order to review a package, there are a lot of things to check. The below
list only provides some guidelines for new rewievers in order to identify a way
to follow. But ofcourse this list is not enough. Reviewers should also use their
own experiences when reviewing a package.

    #. The package name must be suitable to `package naming <http://developer.pardus.org.tr/guides/packaging/package_naming_guidelines.html>`_.
    #. The package must meet the `packaging guidelines <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html>`_.
    #. The package must meet `licensing guidelines <http://developer.pardus.org.tr/guides/licensing/licensing_guidelines.html>`_.
    #. The license tag in the pspec.xml file must match the actual `license short names <http://svn.pardus.org.tr/uludag/trunk/doc/en/licenses/>`_.
    #. The source code of the package and comments must be written in `english <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#summary-and-description>`_.
    #. The source code of the package must be `legible <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#code-legibility>`_.
    #. The package must successfully compile and build into pisi for at least one `architecture supported <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#architecture-support>`_.
    #. If the package could not successfully compile, build or work on a specific architecture, then those architectures should be specified in pspec.xml file with `ExcludeArch tag <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#architecture-support>`_.
    #. All `build dependencies <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#buildtime-dependencies>`_ must be listed in `pspec.xml file <http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html#different-pspec-xml-file-tags>`_, except for any that are listed in the `dependencies excepted document <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#dependencies-excepted>`_.
    #. The `translations.xml file <http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html#creating-translations-xml>`_ must be added to package. 
    #. Almost every pisi package (or subpackage) have shared library files, you must run `checkelf` for every package and find broken links.
    #. Packages must not `bundle copies <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#duplication-of-system-libraries>`_ of system libraries.
    #. Permissions on files must be set properly. Executables should be set with executable permissions, See `Additional Files <http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html#different-pspec-xml-file-tags>`_.
    #. Each package must use related actionsapi modules rather than recreating similar modules in `main`.
    #. Package must contain code, or `permissable content <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#summary-and-description>`_.
    #. If the size or the quantity of the `documentation files <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#documentation>`_ are large, they must go in a packagename-doc subpackage.
    #. `Header files or unversioned shared libraries <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#devel-packages>`_ must be in a packagename-devel subpackage.
    #. `Libtool archives <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#static-libraries>`_ .la must not be included in packages, these must be removed in the actions.py if they are built.
    #. The GUI application pacakges must contain `packagename.desktop file <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#desktop-files>`_, and the `icon tag <http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html#different-pspec-xml-file-tags>`_ of this application should also be defined in pspec.xml file.
    #. The reviewer should test the package in a related proper Pardus system.
    #. The reviewer should test that the application runs as described. For example the applcation should not be crashed or give a segfault.
    #. Usually, subpackages require the base package as a dependency, it should be defined as a `strict dependency <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#strict-dependencies>`_ for subpackages as needed.
    #. `Pkgconfig(.pc) <http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#devel-packages>`_ situation should be examined and their package placement should be decided. 
