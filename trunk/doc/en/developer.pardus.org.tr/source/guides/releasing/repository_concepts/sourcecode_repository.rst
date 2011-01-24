.. _sourcecode-repository:

Source Code Repository
~~~~~~~~~~~~~~~~~~~~~~

:Author: Semen Cirit
:Date: |today|
:Version: 0.2

Pardus developers may be located all around the world. We keep the source code in
an internet-accessible version control system called Subversion `SVN`_, in order
to enable our developers to work together on Pardus Distribution.

Pardus has source code repositories and use SVN for source of packages,
technologies and web pages. See `Pardus svn web page`_.


Before explaining Pardus repositories structures, we need to explain first
general `subversion branch maintainance`_:

The **trunk** is the main line of development in a SVN repository.

A **branch** is a side-line of development created to make larger, experimental
or disrupting work without annoying users of the trunk version. Also, branches
can be used to create development lines for multiple versions of the same product,
like having a place to backport bugfixes into a stable release.

Finally, **tags** are markers to highlight notable revisions in the history of
the repository..

Special folder names can also be used as trunk, branch, or tags that can be more
meaningful to use.

Package Source Repository
=========================

distribution Folder
--------------------

Each developed Pardus distribution has a special folder name in Pardus
`Package source repository`_ and these folders are used as trunks. Each distribution
on this `Package source repository`_ has a specific folder tree.

devel Folder
^^^^^^^^^^^^

The under development package source files are included in this folder. This means
whenever a package maintainer changes some code on his/her packages, it should
be committed a related devel repository folder.

This folder may contain alfa, beta or latest ubstable releases of packages.

testing Folder
^^^^^^^^^^^^^

This folder includes package source files which obtains their stable releases. In
other words while devel folder can contain unstable packages stable can not.

But some exceptions can also be exist, if you are not sure please ask Pardus
`devel list`_.

These two folders also has a specific folder tree. In this tree, the folders are
named with Pardus `package components`_.

devel 

playground Folder
-----------------

`Package source repository`_ includes also an other folder `playground`_. When
a new package is wants to be added to Pardus repositories or a new release of
a complicated package will be implemented, the package maintainer use subfolder
of the `playground`_ which is named with his/her name to commit the changes of
packages.

review Folder
^^^^^^^^^^^^^
The `playground`_ has also a `review`_ folder. This folder also has folders
named as package components. Whenever a package is ready for `package review`_,
the package maintainer should move packages from his/her named folder under
`playground`_ to package component named folder under `review`_.

tags Folder
-----------
`Package source repository`_ includes also an other folder `tags`_. This folder
includes distribution folders which reached their `end of life`_.


Core Projects Source Repository
===============================

`core projects source repository`_ includes the projects which are included in at
least one Pardus distribution.

There exist also the `developer scripts`_ and `developer docs`_ under this
repository.

This repository use general subversion branch maintainance as mentioned above:

trunk Folder
------------

This `trunk`_ folder includes the maintained projects, scripts, and documents of Pardus
distribution.

branches Folder
---------------

Some projects need branches in order to create development lines for multiple
versions, therefore these projects can be branched under this `branches`_.

tags Folder
-----------

`tags folder`_ is used for unmaintained projects or unmaintained versions of a
project.

External Projects Source Repository
===================================

`external projects source repository`_ includes the projects of Pardus developers,
but these projects are not related any Pardus distribution. In other words Pardus
developers use this repository to commit their self open source projects. When a
project in that repository is decided to take place in a Pardus distribution, it
should be moved to `core projects source repository`_.

Özgürlük İçin Source Repository
===============================

`oi source repository`_ includes Özgürlük için projects and web page source codes.

This repository has also the folders trunk and branches.

Web Source Repository
=====================

`web source repository`_ includes the web page contents and codes of Pardus web
pages.

.. _subversion branch maintainance: http://svnbook.red-bean.com/nightly/en/svn.branchmerge.html
.. _devel list: http://liste.pardus.org.tr/mailman/listinfo/pardus-devel
.. _SVN: http://subversion.tigris.org/
.. _Pardus svn web page: http://svn.pardus.org.tr/
.. _Package source repository: http://svn.pardus.org.tr/pardus/
.. _playground: http://svn.pardus.org.tr/pardus/playground/
.. _review: http://svn.pardus.org.tr/pardus/playground/review/
.. _package review: http://developer.pardus.org.tr/guides/packaging/package-review-process.html
.. _tags: http://svn.pardus.org.tr/pardus/tags/
.. _end of life: http://developer.pardus.org.tr/guides/releasing/end_of_life.html#subversion-tasks
.. _core projects source repository: http://svn.pardus.org.tr/uludag/
.. _developer scripts: http://svn.pardus.org.tr/uludag/trunk/scripts/
.. _developer docs: http://svn.pardus.org.tr/uludag/trunk/doc/
.. _trunk: http://svn.pardus.org.tr/uludag/trunk/
.. _branches: http://svn.pardus.org.tr/uludag/branches/
.. _tags folder: http://svn.pardus.org.tr/uludag/tags/
.. _external projects source repository: http://svn.pardus.org.tr/projeler/
.. _oi source repository: http://svn.pardus.org.tr/oi/
.. _web source repository: http://svn.pardus.org.tr/web/
.. _package components: http://developer.pardus.org.tr/guides/packaging/package_components.html
