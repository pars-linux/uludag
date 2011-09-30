.. _beta-release:

Beta Release
============

:Author: Semen Cirit
:Last Modified Date: |today|
:Version: 0.2

Beta phase is bug fixing and detailed test phase in order to stabilize new
release and takes about 1 month.

At the end of the beta phase, software should be `code complete`_, indicating
that there only left critical bug fixes left. Code complete version of a software
is almost similar to final.

During this phase Beta `tracker bugs`_ should also be fixed.

Beta phase has also rapid changes and so the software can be unstable and could
cause crashes or data loss.

Beta Goals
^^^^^^^^^^
#. The Beta official release will be a `code complete`_ test release
#. Produce a release almost bug free and well tested
#. Find as many as RC and final `tracker bugs`_ as possible

Beta Release Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^

In order to do Pardus Beta official, the following criterias must be meet:

* All `alpha release requirements`_ must be achieved.
* All bugs blocking the Beta tracker must be closed.
* The installation manager (YALI_) must boot and run on all `supported architectures`_ from install and live images
* The installation manager (YALI_) must  be able to complete the installation using the shrink option supported different file systems.
* The installation manager (YALI_) must boot and run on systems using EFI
* The installation manager (YALI_) must be able to create and install to software, hardware or BIOS RAID-0, RAID-1 or RAID-5 partitions for anything except /boot
* The rescue mode of (YALI_) must start successfully and be able to detect and mount LVM, and RAID (BIOS, hardware, software) installation
* The installed system must be able to boot with desktop environment sound
* The all `Pardus technologies`_ must be able to work with new features and almost bug free.
* The default browser must run video and music
* The default video player must run videos with supported extentions from disks, DVD, VCD etc.
* The default music player must run songs with supported music extentions from disks, DVD, CD etc.
* The default desktop environment must mount removable media
* The desktop environment must succesfully shutdown, reboot, hibernate, logout etc.
* Beta release must include default artwork by default for the installation manager (YALI_), graphical boot, firstboot, graphical login, desktop background and splash screens.
* Release Upgrade should be stabilized and get almost ready to Final Release.
* The upgrade manager should complete the upgrade from a clean updated previous Pardus release.

Beta Schedule
^^^^^^^^^^^^^

Beta 1
######

1 week before Beta 1:
-----------------------

#. Review `tracker bugs`_ and no urgent and high bugs present
#. Finish high (P1) priority `tracker bugs`_
#. Create a list for promotion and publicity materials
#. Plan and start for artwork pardus

   * Final Web banners
   * DVD, CD cover, guide design
   * Brochures, stand and roll-up design
   * Promotion products design
#. Translation and user documentation check

Beta 1 release day:
-------------------

#. Release Beta

   * Upload iso to FTP servers
   * Upload iso to torrents

#. Announcement for Beta release on `gelistirici list`_ and `developer list`_
#. Announcement for Beta release on `duyuru list`_ and `announce list`_

Beta 2
######

1 week before Beta 2:
---------------------

#. Finish all normal (P2), low (P3) priority `tracker bugs`_
#. `Toolchain freeze`_ start
#. Warn developers about:

   * `User interface freeze`_
   * Package file conflicts or unresolved package dependencies

#. Begin Release Upgrade tests
#. Warn aout EOL of previous release

1 week before Beta 2:
---------------------

#. `User interface freeze`_ (artwork)
#. `Beta freeze`_ (`code complete`_) on (`testing source repository`_)
#. From this point bug fixes taken to repository with release team approval
#. Review problems and mark as Beta tracker bug which need resolution before release

   * Package conflicts or unresolved package dependencies
   * Installation bugs
   * Release Upgrade bugs
   * High severity bugs

#. Selectively accept package merges to resolve Beta `tracker bugs`_
#. Create Beta Test Release for Beta validation tests

   * Installation media
    Live media

#. Prepare and make "where we are meeting" after validation tests, in order to review bugs and possibility to prolonge release.
#. Create release-notes
#. Warn mirrors and ULAKBIM one week before
#. Preperation for final release announcement and marketing materials

3 days before Beta 2:
---------------------

#. Resolve image based problems

   * Package conflicts or unresolved package dependencies
   * Installation bugs
   * High severity bugs

#. Test and fix Beta `tracker bugs`_

1 day before Beta 2:
--------------------

#. Review Beta `tracker bugs`_ and take final decision what to fix or defer
#. Prepare and plan RC start meeting

Beta 2 release day:
-------------------

#. Upload release-notes to developer.pardus.org.tr
#. Release Beta

   * Upload iso to FTP servers
   * Upload iso to torrents

#. Announcement for Beta release on `gelistirici list`_ and `developer list`_

1 day after Beta 2 release day:
-------------------------------

#. Warn about `Translation freeze`_
#. Warn about `Final freeze`_
#. Begin the plan of `next new release`_

Beta Tracker Bugs
^^^^^^^^^^^^^^^^^

A bug is considered an beta tracker bug if one of the following criterias is met:

#. If a package in the urgent package list of alpha and beta has a bug that can not be fixed with a future update or has a severity_ rating of high or urgent.
#. Bugs that are a blocks the testing and test process. (Bugs related to untestable products)
#. Bug relates to an unachieved `Beta Release Requirements`_

Beta Postponement
^^^^^^^^^^^^^^^^^

#. One week before the release day, if all of the `Beta Release Requirements`_ are not achieved, the release will be delayed one week that the `Beta Release Requirements`_ can be achieved.
#. This delay will be added all remaining tasks and final release date.
#. The decision for the delay will be made on "where we are" meeting that be held 2 weeks prior to the shipping date of the releases.

Validation of Beta Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Test team has the responsibility of determining whether the criteria for the
`Beta Release Requirements`_ has been met. At the end of the test process,
the test team reports on `Pardus Bugzilla`_ will be reviewed and discussed
at the "where we are" meeting.


.. _requested features: http://developer.pardus.org.tr/guides/newfeature/index.html
.. _Pardus Bugzilla: http://bugs.pardus.org.tr/
.. _urgent package list: http://svn.pardus.org.tr/uludag/trunk/scripts/find-urgent-packages
.. _package source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#package-source-repository
.. _devel branch: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#devel-folder
.. _component based: http://developer.pardus.org.tr/guides/packaging/package_components.html
.. _alpha release requirements: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html#alpha-release-requirements
.. _severity: http://developer.pardus.org.tr/guides/bugtracking/howto_bug_triage.html#bug-importance
.. _supported architectures: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#architecture-support
.. _YALI: http://developer.pardus.org.tr/projects/yali/index.html
.. _Kaptan: http://developer.pardus.org.tr/projects/kaptan/index.html
.. _Pardus technologies: http://developer.pardus.org.tr/projects/index.html
.. _code complete: http://developer.pardus.org.tr/guides/releasing/freezes/feature_freeze.html
.. _tracker bugs: http://developer.pardus.org.tr/guides/bugtracking/tracker_bug_process.html#open-tracker-bug-report
.. _accepted features: http://bugs.pardus.org.tr/buglist.cgi?query_format=advanced&bug_severity=newfeature&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&resolution=REMIND
.. _testing source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#testing-folder
.. _duyuru list: http://lists.pardus.org.tr/mailman/listinfo/duyuru
.. _announce list: http://lists.pardus.org.tr/mailman/listinfo/pardus-announce
.. _User interface freeze: http://developer.pardus.org.tr/guides/releasing/freezes/user_interface_freeze.html
.. _Beta freeze: http://developer.pardus.org.tr/guides/releasing/freezes/beta_freeze.html
.. _next new release: http://developer.pardus.org.tr/guides/releasing/official_releases/release_process.html
.. _Toolchain freeze: http://developer.pardus.org.tr/guides/releasing/freezes/toolchain_freeze.html
.. _Translation freeze: http://developer.pardus.org.tr/guides/releasing/freezes/translation_freeze.html
.. _Final freeze: http://developer.pardus.org.tr/guides/releasing/freezes/final_freeze.html
.. _Repo branching: http://developer.pardus.org.tr/guides/releasing/freezes/repo_freeze.html
.. _developer list: http://lists.pardus.org.tr/mailman/listinfo/pardus-devel
.. _gelistirici list: http://lists.pardus.org.tr/mailman/listinfo/gelistirici
