Package Review Process
===========================

The goal of package review process is to control that new packages are
suitable for repository policy rules.

The package review process steps on 
`Pardus Bug Tracking System <http://hata.pardus.org.tr>`_;

#. If a bug is reported for a new package on bug tracking system, the process 
   is start from this point.

#. The developer that wants to maintain this package, assigns this bug
   to him/her self and changes the bug status to ASSIGNED. This operation
   can be done only by the members of "editbugs" group.

#. For the bug report, the product is selected as "Review", and the component
   will be the appropriate repository component. The interested component
   supervisors will be added automatically to default cc.

#. If any package has also dependent packages in review process, this
   package is signed as "Dependent" on bug report.

#. When the package is ready, it is copied under the appropriate component of
   playground/review directory in package repository.

#. If any other changes have done after the review process, its SVN commit message
   should contain the following line in order to add a comment to bug report:

     BUG:COMMENT:<Bug ID>

#. In order to decide the package is suitable for the package repository, it
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

#. The package that takes the necessary ACKs, is taken to devel package repository
   and the bug status is changed to RESOLVED/FIXED.
