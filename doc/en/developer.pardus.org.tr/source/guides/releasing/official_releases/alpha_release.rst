.. _alpha-release:

Alpha Release
-------------

:Author: Semen Cirit
:Last Modified Date: |today|
:Version: 0.1

The alpha phase of the release life cycle is the first phase to begin software
testing.

Feature acceptence deadline is held during this phase and the `requested features`_
from users and developers are reported to `Pardus Bugzilla`_ before this deadline.

The requested features are reviewed and also prioritized during this period
and no more features are added to this list. The features are also started to
develop by developers.

During this phase Alpha release brockers should also be fixed.

For the packages, `urgent package list`_ is created periodically and put as text
file under the related release' `package source repository`_ `devel branch`_.
These packages are updated and merged to new `package source repository`_ at given
period and time.

As we can see during alpha phase rapid changes occur and so the software can be
unstable and could cause crashes or data loss.

Alpha Goals
^^^^^^^^^^^
#. The accepted features should be listed and prioritized at the and of Feature acceptence deadline.
#. The Alpha official release wil be a `feature complete`_ test release.
#. Test `accepted features`_ of Pardus for newly release
#. Find as many as Beta, RC, final `tracker bugs`_ as possible

Alpha Release Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^
In order to do Pardus Alpha official, the following criterias must be meet:

* All bugs blocking the Alpha tracker must be closed.
* There must be no file conflicts or unresolved package dependencies in Alpha iso install and live images.
* The iso image must boot with graphical boot menu and allow the user to select installation options.
* The installation manager (YALI_) must boot and run on all `supported architectures`_ from install and live images
* The installation manager (YALI_) must be able to complete the installation using the install options use all space or use free space
* The installation manager (YALI_) must be able to complete an installation using IDE, SATA and SCSI storage devices, with the default file system (ext4) and LVM, standart partitioning
* The rescue mode of (YALI_) must start successfully and be able to detect and mount an existing default installation
* The installed system must boot to th default desktop environment without user intervention
* The desktop greeter (Kaptan_) should start when the system boot.
* The default web browser must run and be able to download files and load extensions
* The `Package Manager`_ must have the correct repository and be able to download and install updates with with PiSi_.
* The new release artwork must either refer to the current release under maintainance, or reference to a temporary test release. This artwork should be for the installer, firstboot, graphical boot, graphical login·

Pre-Alpha (Developer Release) Tickets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#. Prepare and plan start meeting
#. Create general release schedule (give deadlines only for general relase cycles (Alpha, Beta, RC, Final))
#. Put the schedule to developer.pardus.org.tr
#. Open `devel source`_ and  `devel binary`_ repositories
#. Add new devel repository to http://packages.pardus.org.tr
#. Open `tracker bugs`_
#. Prepare buildfarm servers
#. State toolchain versions
#. State compiler flags
#. Prepare toolchain
#. Bootstrap_
#. Compile developer tools
#. Install and build buildfarm_ systems
#. Prepare pre-alpha (developer) release
#. Enable `nightly builds`_
#. Enable automatic mails about nightly build changes to `tester list`_.
#. Review package components for orphan and dead packages
#. Warn developers about their orphan and dead packages and developer release
#. Create release plan (give deadlines for milestones( submitting new features, feature freeze, string freeze, feature complete, translation freeze, repo freeze, announce final feature list))
#. Put the updated schedule to developer.pardus.org.tr
#. Prepare a developer meeting on IRC
#. Prepare and plan Alpha start meeting

Alpha Tickets
^^^^^^^^^^^^^
#. Warn users and developers about `feature request`_ deadline one week before
#. Warn developers about `feature submission`_ deadline one week before
#. Create accepted feature list
#. Put feature list to developer.pardus.org.tr
#. Send weekly emails about `urgent package list`_
#. Warn about `feature freeze`_ one week before
#. Warn about Alpha freeze one week before
#. Plan for artwork Pardus
    * Wallpapers
    * Icon theme
    * Splash screens
#. Create Alpha Test Release for Alpha validation tests
    * Installation media
    * Live media
#. Prepare and make "where we are meeting" after validation tests
#. Create release-notes
#. Upload release-notes to developer.pardus.org.tr
#. Release Alpha
    * Upload iso to FTP servers
    * Upload iso to torrents
#. Send an announcement mail for Alpha release
#. Prepare and plan Beta start meeting

Alpha Tracker Bugs
^^^^^^^^^^^^^^^^^^

A bug is considered an alpha tracker bug if one of the following criterias is met:

#. If a package in the urgent package list of alpha has a bug that can not be fixed with a future update or has a severity_ rating of high or urgent.
#. Bugs that are a blocks the testing and test process. (Bugs related to untestable products)
#. Bug relates to an unachieved `Alpha Release Requirements`_

Alpha Postponement
^^^^^^^^^^^^^^^^^^

#. One week before the release day, if all of the `Alpha Release Requirements`_ are not achieved, the release will be delayed one week o that the `Alpha Release Requirements`_ can be achieved.
#. This delay will be added all remaining tasks and final release date.
#. The decision for the delay will be made on "where we are" meeting that be held 2 weeks prior to the shipping date of the releases.

Validation of Alpha Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Test team has the responsibility of determining whether the criteria for the
`Alpha Release Requirements`_ has been met. At the end of the test process,
the test team reports on `Pardus Bugzilla`_ will be reviewed and discussed
at the "where we are" meeting.


.. _requested features: http://developer.pardus.org.tr/guides/newfeature/index.html
.. _Pardus Bugzilla: http://bugs.pardus.org.tr/
.. _urgent package list: http://svn.pardus.org.tr/uludag/trunk/scripts/find-urgent-packages
.. _package source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#package-source-repository
.. _devel branch: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#devel-folder
.. _component based: http://developer.pardus.org.tr/guides/packaging/package_components.html
.. _accepted features: http://bugs.pardus.org.tr/buglist.cgi?query_format=advanced&bug_severity=newfeature&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&resolution=REMIND
.. _feature complete: http://developer.pardus.org.tr/guides/releasing/feature_freeze.html
.. _supported architectures: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#architecture-support
.. _YALI: http://developer.pardus.org.tr/projects/yali/index.html
.. _Kaptan: http://developer.pardus.org.tr/projects/kaptan/index.html
.. _Package Manager: http://developer.pardus.org.tr/projects/package-manager/index.html
.. _Pisi: http://developer.pardus.org.tr/projects/pisi/index.html
.. _severity: http://developer.pardus.org.tr/guides/bugtracking/bug_cycle.html
.. _tester list: http://lists.pardus.org.tr/mailman/listinfo/testci
.. _Bootstrap: http://developer.pardus.org.tr/guides/releasing/bootstrapping.html
.. _buildfarm: http://developer.pardus.org.tr/guides/releasing/preparing_buildfarm.html
.. _nightly builds: http://developer.pardus.org.tr/guides/releasing/generating_nightly_builds.html
.. _devel source: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#devel-folder
.. _devel binary: http://developer.pardus.org.tr/guides/releasing/repository_concepts/software_repository.html#devel-binary-repository
.. _tracker bugs: http://developer.pardus.org.tr/guides/bugtracking/tracker_bug_process.html#open-tracker-bug-report
.. _feature request: http://developer.pardus.org.tr/guides/newfeature/newfeature_requests.html#how-do-i-propose-a-new-feature-that-i-do-not-contribute
.. _feature submission: http://developer.pardus.org.tr/guides/newfeature/newfeature_requests.html#how-my-new-feature-request-is-accepted
.. _feature freeze: http://developer.pardus.org.tr/guides/releasing/feature_freeze.html
