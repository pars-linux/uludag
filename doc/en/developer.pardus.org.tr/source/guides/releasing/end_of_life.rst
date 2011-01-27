.. _end-of-life:

End of Life
============

Releases for which updates are no longer provided are considered to be
unmaintained and thus end of life or commonly referred to as EOL.

.. Each release of Pardus is maintained as written in `release_life_cycle.rst`_ document. 
At the end of this maintenance period, Pardus reaches its end of life.

This document explains the steps for which a release has reached EOL status.

Setting EOL date
----------------

The EOL date will be determined according to followings:

.. * The `release_life_cycle.rst`_ stages should be taken to account.
* The relational projects with the EOL release should be taken to account.

Anouncement
-----------

The following anouncement will be made:

* Last update date
* Last security update date
* Actual end of life date

See `an example anouncement has made for Pardus EOL <http://liste.pardus.org.tr/pardus-devel/2010-August/001908.html>`_.

Subversion Tasks
----------------

The unmaintained release is moved from main package repository
(http://svn.pardus.org.tr/pardus/) to package tags repository
(http://svn.pardus.org.tr/pardus/tags/).

Packages Web Site Tasks
-----------------------

The package informations about the release that reaches its end of life will be
removed from the packages web site.

The example rsync.conf that changed in servers::

    [pardus-2009]
        path =  /home/pardus/depo/pardus-2009
        comment = 2009 Pardus Repository

The EOL release information in rsync.conf file is removed, and the packages web
site directly sync and its information is disappeared.

Bugzilla Tasks
--------------

Pardus does not track or review bugs for releases where there will be no more
updates that means which reaches its EOL.

All open bugs about the EOL release is controlled. If they are not reproducible
on the actual release they will be closed with the below message:

::

    With the upcoming Pardus X release, Pardus Y which was in security-only
    mode for a while will soon reach its end-of-life and the current bug reports
    concerning Pardus Y will become invalid. If you can still reproduce the bug
    on Pardus X, you can reopen the bug and update the version information. Thanks.

Also the tracker bugs related to release will be closed. (alfa, beta, RC, final release blockers.)

**Last Modified Date:** |today|

:Author: Semen Cirit
