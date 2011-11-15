.. _alpha-release:

Alpha Phase
===========

:Author: Semen Cirit
:Last Modified Date: |today|
:Version: 0.2

The alpha phase of the release life cycle is the phase to begin software
testing and takes about 3 months. About 2 months for Alpha 1 and 4 weeks
for Alpha 2 and 3.

At the end of the alpha phase, software should be `feature complete`_, indicating
that no more features will be added to the software. A feature complete version
of a software is not yet final, (it has lots of bugs) but contains all intended
functionality of the final version.

All new package additions should be finished before feature freeze time.

According to this feature completeness, string freeze is also realized..

During this phase Alpha release `tracker bugs`_ should also be fixed.

For the packages, `urgent package list`_ is created periodically and put as text
file under `package source repository`_ `devel branch`_.
These packages are updated to required versions and merged to `package source
repository`_ at given period and time.

As we can see during alpha phase rapid changes occur and so the software can be
unstable and could cause crashes or data loss.

Alpha Goals
^^^^^^^^^^^
#. The Alpha official release will be a `feature complete`_ test release.
#. Test `accepted features`_ of Pardus for newly release
#. Find as many as Beta, RC, final `tracker bugs`_ as possible

Alpha Release Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^
For each Pardus Alpha releases (Alpha 1, 2, 3), the following criterias must be met:

* All bugs blocking the Alpha tracker must be closed.
* There must be no file conflicts or unresolved package dependencies in Alpha ISO install and live images.
* The ISO image must boot with graphical boot menu and allow the user to select installation options.
* The installation manager (YALI_) must boot and run on all `supported architectures`_ from install and live images
* The installation manager (YALI_) must be able to complete the installation using the install options "use all space" or "use free space"
* The installation manager (YALI_) must be able to complete an installation using IDE, SATA and SCSI storage devices, with the default file system (ext4) and LVM, standart partitioning
* The rescue mode of (YALI_) must start successfully and be able to detect and mount an existing default installation
* The installed system must boot to the default desktop environment without user intervention
* The desktop greeter (Kaptan_) should start when the system boot.
* All `Pardus technologies`_ must be able to work with new features (they may have bugs)
* All urgent packages should be updated to required versions
* All strings of `Pardus technologies`_ should be finished before Alpha released.
* The default web browser must run and be able to download files and load extensions
* Default applications that exist on desktop menu must be listed.
* The `Package Manager`_ must have the correct repository and be able to download and install updates with with PiSi_.
* The new release artwork must either refer to the current release under maintainance, or reference to a temporary test release. This artwork should be for the installer, firstboot, graphical boot, graphical login
* Release Upgrade tests should start and upgrade can be possible with some existed bugs.

Alpha Schedule
^^^^^^^^^^^^^^

Alpha 1
#######

8-4 week before the Alpha 1:
----------------------------

#. Intrusive changes phase completed (All high (P1) priority features and tasks finished)
#. Create default applications list for desktop menu
#. Send weekly emails about `urgent package list`_
#. Start for artwork Pardus

   * Wallpapers
   * Icon theme
   * Splash screens

1 week before Alpha 1:
----------------------

#. Warn mirrors and ULAKBIM

Alpha 1 release day:
--------------------

#. Release Alpha

   * Upload ISO to FTP servers
   * Upload ISO to torrents


#. Announcement for Alpha release on `gelistirici list`, `developer list`_ and `duyuru list`_, `announce list`_


Alpha 2
#######

3-2 week before Alpha 2:
------------------------

#. Medium (P2) priority tasks and features finished
#. At the end of this period, all remained features reviewed and reprioritized or ignored if needed.

1 week before Alpha 2:
----------------------

#. Warn mirrors and ULAKBIM one week before

Alpha 2 release day:
--------------------

#. Release Alpha

   * Upload ISO to FTP servers
   * Upload ISO to torrents

#. Announcement for Alpha release on `gelistirici list`, `developer list`_

Alpha 3
#######

2-1 week before Alpha 3:
------------------------

#. "Where we are meeting" to review bugs and possibility to prolonge release.
#. Low (P3) priority tasks and features finished
#. Warn about `Feature freeze`_ one week before
#. Warn about `Repo branching`_ one week before
#. Warn about `String freeze`_

1 week before Alpha 3:
----------------------

#. `Feature freeze`_
#. `String freeze`_
#. Create release-notes
#. Warn mirrors and ULAKBIM

4 days before Alpha 3:
----------------------

#. `Repo branching`_ for main/base repo

   * Open testing source_ and binary_ repositories
   * Add new testing repository to packages.pardus.org.tr

#. Announce repo freeze on #pardus-devel and `gelistirici list`_ and `developer list`_
#. Create Alpha Test Release for Alpha validation tests

   * Installation media
   * Live media

#. Prepare and make "where we are meeting" after validation tests, in order to review bugs and possibility to prolonge release.
#. Review problems and mark as Alpha tracker bug which need resolution before release

   * Package conflicts or unresolved package dependencies
   * Bugs that breaks default installation
   * High severity bugs

#. Selectively accept package merges to resolve Alpha tracker bugs
#. Prepare and plan Beta start meeting

1 day before Alpha 3:
---------------------

#. Resolve any remaining Alpha `tracker bugs`_
#. Begin Release Upgrade tests (all new package merges and features completed and from now on repo is consistent.)

Alpa 3 release day:
-------------------

#. Upload release-notes to developer.pardus.org.tr
#. Release Alpha

   * Upload ISO to FTP servers
   * Upload ISO to torrents


#. Announcement for Alpha release on `gelistirici list`, `developer list`_

Release plus 1 week:

#. Update release notes and feature list if necessary (if a feature could not be done during alpha phase it should be removed from feature list)

Alpha Tracker Bugs
^^^^^^^^^^^^^^^^^^

A bug is considered an alpha tracker bug if one of the following criteria is met:

#. If a package in the urgent package list of alpha has a bug that can not be fixed with a future update or has a severity_ rating of high or urgent.
#. Bugs that are a blocks the testing and test process. (Bugs related to untestable products)
#. Bug relates to an unachieved `Alpha Release Requirements`_

Alpha Postponement
^^^^^^^^^^^^^^^^^^

#. One week before the release day, if all of the `Alpha Release Requirements`_ are not achieved, the release will be delayed one week that the `Alpha Release Requirements`_ can be achieved.
#. This delay will be added all remaining tasks and final release date.
#. The decision for the delay will be made on "where we are" meeting that be held 1 weeks prior to the shipping date of the releases.

Validation of Alpha Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Test team has the responsibility of determining whether the criteria for the
`Alpha Release Requirements`_ has been met. At the end of the test process,
the test team reports on `Pardus Bugzilla`_ will be reviewed and discussed
at the "where we are" meeting.


.. _requested features: ../../guides/newfeature/index.html
.. _Pardus Bugzilla: http://bugs.pardus.org.tr/
.. _urgent package list: http://svn.pardus.org.tr/uludag/trunk/scripts/find-urgent-packages
.. _package source repository: ../../guides/releasing/repository_concepts/sourcecode_repository.html#package-source-repository
.. _devel branch: ../../guides/releasing/repository_concepts/sourcecode_repository.html#devel-folder
.. _component based: ../../guides/packaging/package_components.html
.. _accepted features: http://bugs.pardus.org.tr/buglist.cgi?query_format=advanced&bug_severity=newfeature&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&resolution=REMIND
.. _feature complete: ../../guides/releasing/freezes/feature_freeze.html
.. _supported architectures: ../../guides/packaging/packaging_guidelines.html#architecture-support
.. _YALI: ../../projects/yali/index.html
.. _Kaptan: ../../projects/kaptan/index.html
.. _Package Manager: ../../projects/package-manager/index.html
.. _Pisi: ../../projects/pisi/index.html
.. _severity: ../../guides/bugtracking/howto_bug_triage.html#bug-importance
.. _tester list: http://lists.pardus.org.tr/mailman/listinfo/testci
.. _Bootstrap: ../../guides/releasing/bootstrapping.html
.. _buildfarm: ../../guides/releasing/preparing_buildfarm.html
.. _nightly builds: ../../guides/releasing/generating_nightly_builds.html
.. _devel source: ../../guides/releasing/repository_concepts/sourcecode_repository.html#devel-folder
.. _devel binary: ../../guides/releasing/repository_concepts/software_repository.html#devel-binary-repository
.. _tracker bugs: ../../guides/bugtracking/tracker_bug_process.html#open-tracker-bug-report
.. _feature request: ../../guides/newfeature/newfeature_requests.html#how-do-i-propose-a-new-feature-that-i-do-not-contribute
.. _feature submission: ../../guides/newfeature/newfeature_requests.html#how-my-new-feature-request-is-accepted
.. _Feature freeze: ../../guides/releasing/freezes/feature_freeze.html
.. _duyuru list: http://lists.pardus.org.tr/mailman/listinfo/duyuru
.. _announce list: http://lists.pardus.org.tr/mailman/listinfo/pardus-announce
.. _developer list: http://lists.pardus.org.tr/mailman/listinfo/pardus-devel
.. _gelistirici list: http://lists.pardus.org.tr/mailman/listinfo/gelistirici
.. _binary: ../../guides/releasing/repository_concepts/software_repository.html#testing-binary-repository
.. _source: ../../guides/releasing/repository_concepts/sourcecode_repository.html#testing-folder
.. _Pardus technologies: ../../projects/index.html
.. _Repo branching: ../../guides/releasing/freezes/repo-freeze.html
.. _String freeze: ../../guides/releasing/freezes/string-freeze.html
