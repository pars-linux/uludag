Package Reviewing Process
===========================

The aim of the package reviewing process is to control that new packages are
suitable for repository policy rules.

The package reviewing process steps on
`Pardus Bug Tracking System <http://hata.pardus.org.tr>`_;

#. If a bug is reported for a new package on the bug tracking system, the process
   is starting from this point.

#. The developer that wants to maintain this new package, assigns the bug report
   to himself/herself and changes the bug status to ASSIGNED. This operation
   can only be done by the members of bugzilla "editbugs" group.

#. The "Summary" part of the bug report should contain the name of the package.
   The "Details" part of the bug should contain the description of the package,
   e.g. a detailed phrase which explains the main objective of the package, what it does, etc.

#. If the package is taken to the reviewing process because of a specific reason (e.g.
   the package may be a dependency of an available package in the repository or of another
   to-be-reviewed package), this reason should be indicated in the "Details" part of the bug report.

#. If the developer is willing to maintain the package in the contribution repositories,
   this should be indicated in the "Details" part of the bug report.

#. The product of the bug report should be "Review".
   The component of the bug report should be the appropriate repository component for being able
   to notify the relevant component responsables by e-mail about this new package reviewing request.

#. If the package depends on other packages currently in reviewing process, the bug report should
   "depend" on those other packages' bug reports to establish a dependency relationship between
   them.

#. When the developer thinks that its new package is ready for the reviewing process, he/she should copy
   it under the appropriate component of the 'playground/review' directory under pardus SVN repository.

#. All changes done to the package during the reviewing process (e.g. All modifications committed under 'playground/review')
   should be reflected as a comment to the relevant bug report using the following special keyword in the SVN commit messages:

     BUG:COMMENT:<Bug ID>

#. In order to decide that the package is suitable for a package repository, it
   should take necessary number of ACKs. The ACK comments will be given firstly
   by the supervisor of the package component, then by an other package
   maintainer.

   In order to complete the package review process two ACKs is necessary.
   One of these ACKs should be given by component supervisor. If the package
   maintainer is also the its component supervisor, the other package maintainers
   can give these two ACKs.

#. If the reviewer find any problem about the package in review, he/she should
   wait for this problem fixed by the maintainer. In other words the conditinal
   ACK is forbidden.

   Example: Bad: After changing the directory paths, it will be ACK.
            Good: It should change the directory paths.

   After the package maintainer has fixed the problem, the reviewer verify the
   problem and give an ACK as a comment.

#. The package that takes the necessary ACKs, is taken to devel package repository,
   removed from review directory and the bug status is changed to RESOLVED/FIXED.
