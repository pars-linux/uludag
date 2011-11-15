.. _rc-release:

Release Candidate Phase
=======================

:Author: Semen Cirit
:Last Modified Date: |today|
:Version: 0.1


The term release candidate (RC) refers to a version with potential to be a
final product, ready to release unless fatal bugs emerge.

RC takes about 2 weeks.

The translation freeze should also be held at the end of this stage.

At the end of this stage all Final `tracker bugs`_ should be fixed.

RC Goals
^^^^^^^^

* Provide a tracker bug free and well tested release intended for Final release and suitable for meeting the needs of our users.

RC Release Requirements
^^^^^^^^^^^^^^^^^^^^^^^

In order to do Pardus RC official, the following criteria must be met:

* All `beta release requirements`_ must be achieved.
* All Final `tracker bugs`_ must be closed.
* The installation manager (YALI_) must be able to complete an installation using IDE, SATA, SCSI and iSCSI storage devices
* The installation manager (YALI_) must be able to create partition tables using any file system offered in installer configuration and complete installation for LVM, software, hardware or BIOS RAID, or  IDE, SATA, SCSI and iSCSI storage devices.
* The installation manager (YALI_) must boot and run on all `supported architectures`_ from install and live images
* All known bugs can cause corruption of user data be fixed or marked as "High" on `Pardus bugzilla`_
* The following criteria should be met on both live and default installed system for desktop validation
    - The icons of desktop menu applications all should exist and have a consistent appearance and sufficiently high resolution to avoid appearing blurry
    - All desktop menu applications must start successfully
    - All desktop menu applications must pass basic functionality tests and not crash after a few minutes of normal use.
    - All desktop menu applications have a working help.
    - Any application can exist twice in desktop menu.
* The default panel configuration must function correctly
    - Show desktop
    - Show different desktops
    - Show external device
    - Sound Mixer
    - Date & Time
    - Network connection
* Release notes should open automatically on other operating systems.
* The policy settings must work successfully
* Final release must include default artwork by default for the installation manager (YALI_), graphical boot, firstboot, graphical login, desktop background and splash screens.
* Pardus icon theme must be supported by the desktop greeter (Kaptan_) and should load successfully if selected.
* All supported languages should be announced on mail lists and the translations of these supported languages should be finished and tested before RC released.
* Upgrade manager should be ready for upgrade

RC Schedule
^^^^^^^^^^^

2 weeks before RC:
------------------

#. All Final `tracker bugs`_ fixed
#. Kernel freeze start
#. Warn contributors about:

   * `Translation freeze`_
   * `Kernel freeze`_
   * `RC freeze`_
   * Package file conflicts or unresolved package dependencies

#. Begin Release Upgrade tests
#. Plan the date of product publicity (launching)

7 days before RC:
-----------------

#. Review problems and mark as RC tracker bug which need resolution before release

   * Package conflicts or unresolved package dependencies
   * Installation bugs
   * Release Upgrade bugs
   * High severity bugs

#. Selectively accept package merges to resolve Final tracker bugs
#. `Translation freeze`_
#. `Kernel freeze`_
#. `RC freeze`_
#. Create Final Test Release for Final validation tests

   * Installation media
   * Live media

#. Prepare and make "where we are meeting" after validation tests in order to review bugs possibility to prolonge release.
#. Decide for RC code name and its Wallpaper
#. Create release-notes
#. Make stock plan for publicity and promotion materials
#. Preperation for final release announcement and marketing materials
#. Last check for update feature list according to completed features
#. Warn mirrors and ULAKBIM one week before
#. Test and fix Final `tracker bugs`_
#. Testing targets achieved (All features functional and bug free)
#. Track the production of publicity and promotion materials
#. Open `stable binary repository`_

3 days before RC:
-----------------

#. Review Final `tracker bugs`_ and take final decision what to fix or defer
#. Fixing only urgent release `tracker bugs`_, bug fix needs approval. (See `testing source repository merge process`_)
#. Prepare press release from release-notes
#. Warn about `Final freeze`_

RC release day:
---------------

#. Upload release-notes to developer.pardus.org.tr
#. Upload press-release to pardus.org.tr
#. Release RC

   * Upload ISO to FTP servers
   * Upload ISO to torrents

#. Announcement for RC release on `duyuru list`_ and `announce list`_

Final Tracker Bugs
^^^^^^^^^^^^^^^^^^

A bug is considered a final tracker bug if one of the following criteria is met:

#. If a package in the urgent package list of alpha, beta or final has a bug that can not be fixed with a future update or has a severity_ rating of high or urgent.
#. Bugs that are a blocks the testing and test process. (Bugs related to untestable products)
#. Bug relates to an unachieved `RC Release Requirements`_

Final Postponement
^^^^^^^^^^^^^^^^^^

#. One week before the release day, if all of the `RC Release Requirements`_ are not achieved, the release will be delayed one week that the `RC Release Requirements`_ can be achieved.
#. This delay will be added all remaining tasks and final release date.
#. The decision for the delay will be made on "where we are" meeting that be held 2 weeks prior to the shipping date of the releases.
Validation of Final Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Test team has the responsibility of determining whether the criteria for the
`RC Release Requirements`_ has been met. At the end of the test process,
the test team reports on `Pardus Bugzilla`_ will be reviewed and discussed
at the "where we are" meeting.

.. _beta release requirements: ../../guides/releasing/official_releases/beta_phase.html#beta-release-requirements
.. _YALI: ../../projects/yali/index.html
.. _Kaptan: ../../projects/kaptan/index.html
.. _Pardus bugzilla: http://bugs.pardus.org.tr/
.. _supported architectures: ../../guides/packaging/packaging_guidelines.html#architecture-support
.. _urgent package list: http://svn.pardus.org.tr/uludag/trunk/scripts/find-urgent-packages
.. _EOL: ../../guides/releasing/end_of_life.html
.. _severity: ../../guides/bugtracking/howto_bug_triage.html#bug-importance
.. _tracker bugs: ../../guides/bugtracking/tracker_bug_process.html
.. _duyuru list: http://lists.pardus.org.tr/mailman/listinfo/duyuru
.. _announce list: http://lists.pardus.org.tr/mailman/listinfo/pardus-announce
.. _Translation freeze: ../../guides/releasing/freezes/translation_freeze.html
.. _Repo branching: ../../guides/releasing/freezes/repo-freeze.html
.. _RC freeze: ../../guides/releasing/freezes/rc_freeze.html
.. _Final freeze: ../../guides/releasing/freezes/final_freeze.html
.. _Kernel freeze: ../../guides/releasing/freezes/kernel-freeze.html
.. _stable binary repository: ../../guides/releasing/repository_concepts/software_repository.html#stable-binary-repository
.. _testing source repository merge process: tp://developer.pardus.org.tr/guides/packaging/package_update_process.html#merging-to-testing-source-repository:

