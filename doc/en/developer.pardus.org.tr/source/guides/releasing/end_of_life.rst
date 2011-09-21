.. _end-of-life:

End of Life
============

Releases for which updates are no longer provided are considered to be
unmaintained and thus end of life or commonly referred to as EOL. It is
recommended to upgrade a recent version of Pardus at this point.

Each short term support Pardus release is maintained about 1 year and
during this time there will be security and critical fixes. The EOL announce
date of a release is next release + 2 month (n + 2).

For long term support releases, the maintainence is about 4 years, the last
one year only security fixes are held.

At the end of this maintenance period, Pardus reaches its end of life.

This document explains the steps for which a release has reached EOL status.

EOL Goals
*********

Warn users and contributors about the ending time of the maintained release
and give a recommendation for the upgrade to the new release of Pardus.

EOL Schedule
************

4 weeks before EOL:
-------------------

- Warn users and contributors on announce_, duyuru_, gelistirici_, developer_ lists about:
    * Last update date
    * Last security update date
    * Actual end of life date

EOL day:
########

Anouncement
-----------

- Announce EOL of the current release on announce_, duyuru_, gelistirici_, developer_ lists.

See `an example anouncement has made for Pardus EOL <http://liste.pardus.org.tr/pardus-devel/2010-August/001908.html>`_.    * Actual end of life date

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
updates, that means which reaches its EOL.

All open bugs about the EOL release is controlled. If they are not reproducible
on the actual release, they will be closed with the below message:

::

    With the upcoming Pardus X release, Pardus Y which was in security-only
    mode for a while will soon reach its end-of-life and the current bug reports
    concerning Pardus Y will become invalid. If you can still reproduce the bug
    on Pardus X, you can reopen the bug and update the version information. Thanks.

Also the `tracker bugs`_ related to release will be closed. (alfa, beta, RC, final release blockers.)

Redmine Tasks
-------------

All opened issues should be closed or moved to new release issues on `Pardus tracker`_.

.. _tracker bugs: http://developer.pardus.org.tr/guides/bugtracking/tracker_bug_process.html
.. _duyuru: http://lists.pardus.org.tr/mailman/listinfo/duyuru
.. _announce: http://lists.pardus.org.tr/mailman/listinfo/pardus-announce
.. _gelistirici: http://lists.pardus.org.tr/mailman/listinfo/gelistirici
.. _devel: http://lists.pardus.org.tr/mailman/listinfo/pardus-devel
.. _Pardus tracker: http://tracker.pardus.org.tr/
.. _release life cycle: http://developer.pardus.org.tr/guides/releasing/official_releases/release_process.html

**Last Modified Date:** |today|

:Author: Semen Cirit
