Package Reviewing Process
=========================

The aim of the package reviewing process is to control that new packages are
suitable for repository policy rules.

The package reviewing process steps on `Pardus Bug Tracking System
<http://hata.pardus.org.tr>`_;

#. When the developer thinks that his/her new package is ready for the reviewing
   process, he/she should copy it under the appropriate component of the
   'playground/review' directory under pardus SVN repository.

#. If a bug is reported for requesting this new package on the bug tracking system,
   the process is starting from this point.

#. The developer who wants to maintain this new package, assigns the bug report
   to himself/herself and changes the bug status to ASSIGNED. This operation
   can only be done by the members of bugzilla "editbugs" group.

#. After the developer assigns the bug to (him/her)self, A new bug report which
   will block the package request bug will be created. (From now on, this new bug
   report will be mentioned as "the bug report")

#. The product of the bug report should be "Review". The component of the
   bug report should be the appropriate repository component for being able to
   notify the relevant component responsibles by e-mail about this new package
   reviewing request.

#. The "Summary" part of the bug report should contain the full path of the
   package after review folder (ex: desktop/toolkit/gtk/gtkimageview). The
   "Details" part of the bug should contain the description of the package, e.g. a
   detailed phrase which explains the main objective of the package, what it does,
   etc.

#. If the package is taken to the reviewing process because of a specific
   reason (e.g. the package may be a dependency of an available package in the
   repository or of another to-be-reviewed package), this reason should be
   indicated in the "Details" part of the bug report.

#. The repository of the package (contrib, pardus etc.) which the developer is
   willing to maintain the package in, should be indicated in the "Details" part
   of the bug report.

#. If the package depends on other packages currently in reviewing process,
   the bug report should "depend" on those other packages' bug reports to
   establish a dependency relationship between them.

#. All changes done to the package during the reviewing process (e.g. All
   modifications committed under 'playground/review') should be reflected as
   a comment to the relevant bug report using the following special keyword
   in the SVN commit messages:

     BUG:COMMENT:<Bug ID>

#. In order to decide that the package is suitable for a package repository, it
   should take necessary number of approvals. The approval comments will be given firstly
   by the supervisor of the package component, then by an other package
   maintainer.

   In order to complete the package reviewing process two approval is necessary.
   One of these approvals should be given by component supervisor. If the package
   maintainer is also the component supervisor, the other package maintainers
   can give these two approvals.

#. If the reviewer find any problem about the package in review, he/she should
   wait for this problem to be fixed by the maintainer. In other words the
   conditional approval is forbidden.

   Example: Bad:    After changing the directory paths, it will be ACK.
            Good:   It should change the directory paths.

   After the package maintainer has fixed the problem, the reviewer verifies
   the problem and gives an "ACK" as a approval comment.

#. The package that takes the necessary approvals, is taken to package repositories,
   removed from the review directory and the bug status is changed to
   RESOLVED/FIXED.

#. After the package is merged into Pardus Repositories and the review bug report
   is closed, package request bug will be closed too. RESOLVED/FIXED solution can 
   also be applied for this bug. Ideally, closing both review and request bugs at
   the same commit is preferred.
