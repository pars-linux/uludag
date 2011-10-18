.. _package-review-process:

Package Reviewing Process
=========================

:Author: Semen Cirit, Ozan Çağlayan
:Date: |today|
:Version: 0.1


Aim of Review
-------------

Pardus `stable repository`_ is officially maintained, supported and recommended
by Pardus. Security updates are provided for them and standart fixing process
is applied to these packages. (See `severity based fixing times`_)

Thus, before adding new packages to a Pardus `stable repository`_, special attention
should be given.

Package review is a must before it is added to Pardus repositories. The aim of this
process is to be ensure the package satisfies packaging rules.

The requirements below should be checked by reviewers:

    - The package must be suitable to `package review requirements`_ and pass package review
    - The package must build on all architectures
    - The existed upstream bugs of the package and upstream support should be considered
    - GUI applications must be translatable and produce a proper PO template
    - GUI applications should not have turkish language problems
    - GUI applications must have a standart desktop file
    - Package security vulnerabilities must be checked

      - Search package name on http://cve.mitre.org/cve/cve.html and http://secunia.com/advisories/search/
      - Check Pardus `security website`_.

One of the following retionale can be a reason for inclusion of the package:
    - The package is useful for large part of our users
    - The package is a new built or runtime dependency of a package that already in Pardus `stable repository`_
    - The package replaces another package that already exists in Pardus `stable repository`_ and promise higher quality and functionality. (The old package should be obsolete_)


Package Review Guidelines
-------------------------

The person who want to put his package in review and add it to Pardus Repositories, he
should be a Pardus developer. (see :ref:`newcontributor-index` and :ref:`developer-roles` )

Package maintainer and the reviewer must follow the package review process and they
should pay attention that the package adheres to :ref:`package-naming`,
:ref:`packaging-guidelines` and :ref:`licensing-guidelines`.

They also pay attention that the package in review has not in repositories already.

Review Process
--------------

The package reviewing process steps on `Pardus Bug Tracking System
<http://hata.pardus.org.tr>`_;

#. When the developer thinks that his/her new package is ready for the reviewing
   process, he/she should copy it under the appropriate component of the
   ``playground/review`` directory under pardus SVN repository.

#. If a bug is reported for requesting this new package on the bug tracking system,
   the process starts at this point.

#. The developer who wants to maintain this new package, assigns the bug report
   to (him/her)self and changes the bug status to ``ASSIGNED``. This operation
   can only be done by the members of bugzilla "**editbugs**" group.

#. After the developer assigns the bug to (him/her)self, A new bug report which
   will block the package request bug will be created. (From now on, this new bug
   report will be mentioned as **the bug report**)

#. The product of the bug report should be ``Package Review``. The component of the
   bug report should be the appropriate repository component for being able to
   notify the relevant component responsibles by e-mail about this new package
   reviewing request.

#. The ``Summary`` part of the bug report should contain the full path of the
   package after review folder (ex: ``desktop/toolkit/gtk/gtkimageview``). The
   ``Details`` part of the bug should contain the description of the package, e.g. a
   detailed phrase which explains the main objective of the package, what it does,
   etc.

#. If the package is taken to the reviewing process because of a specific
   reason (e.g. the package may be a dependency of an available package in the
   repository or of another to-be-reviewed package), this reason should be
   indicated in the ``Details`` part of the bug report.

#. The repository of the package (contrib, pardus etc.) which the developer is
   willing to maintain the package in, should be indicated in the ``Details`` part
   of the bug report.

#. If the package depends on other packages currently in reviewing process,
   the bug report should ``depend`` on those other packages' bug reports to
   establish a dependency relationship between them.

#. All changes done to the package during the reviewing process (e.g. All
   modifications committed under ``playground/review``) should be reflected as
   a comment to the relevant bug report using the following special keyword
   in the SVN commit messages::

     BUG:COMMENT:<Bug ID>

#. In order to decide that the package is suitable for a package repository, it
   should take necessary number of approvals. The approval comments will be given firstly
   by the supervisor of the package component, then by an other package
   maintainer.

   In order to complete the package reviewing process **2 approval is necessary**.
   One of these approvals should be given by component supervisor. If the package
   maintainer is also the component supervisor, the other package maintainers
   can give these two approvals.

#. If the reviewer finds any problem about the package in review, he/she should
   wait for this problem to be fixed by the maintainer. In other words, the
   conditional approval is forbidden.

   - Example:

     - **Bad:**    After changing the directory paths, it will be ``ACK``.
     - **Good:**   It should change the directory paths.

   After the package maintainer has fixed the problem, the reviewer verifies
   the problem and gives an ``ACK`` as an approval comment.

#. When supervisors give ACK, they will add keyword **ACKS** to the bug. After the bug
    gets an **ACKS** it needs one more ACK from a developer.  When developers give ACK,
    they will add keyword **ACKD** to the bug.

#. The package that takes the necessary approvals, is taken into the package repositories,
   removed from the review directory and the bug status is changed to
   ``RESOLVED/FIXED``.

#. After the package is merged into Pardus Repositories and the review bug report
   is closed, package request bug will be closed too. ``RESOLVED/FIXED`` solution can
   also be applied for this bug. Ideally, closing both review and request bugs at
   the same commit is preferred.

.. _stable repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/software_repository.html#stable-binary-repository
.. _severity based fixing times: http://developer.pardus.org.tr/guides/bugtracking/bug_cycle.html#bugzilla-severities
.. _package review requirements: http://developer.pardus.org.tr/guides/packaging/reviewing_guidelines.html
.. _obsolete: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html?highlight=obsolete#renaming-replacing-existing-packages
.. _security website: http://security.pardus.org.tr/

