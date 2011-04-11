.. _final-release:

Final Release
=============

:Author: Semen Cirit
:Last Modified Date: |today|
:Version: 0.1


Relase Canditate
----------------

The term release candidate (RC) refers to a version with potential to be a
final product, ready to release unless fatal bugs emerge. At the start point
of this  stage all bugs are reviewed and marked as RC release blocker or
Final release brocker.

Release canditate is called code complete when the development team agrees
that no entirely new source code will be added to this release. There may
still be source code changes to fix defects. There may still be changes
to documentation and data files, and to the code for test cases or utilities.
New code may be added in a future release.

Therefore, at the end of this stage all RC release blocker bugs should be fixed.

Final Release
-------------

This phase indicates that the software has reached a point that it is ready to or
has been delivered or provided to the users.

The Final release blocker bugs are fixed, package integrity and feasibility
are checked, last desktop and installation validation tests are done.

Final Goals
^^^^^^^^^^^

* Provide a blocker bug free final release suitable for meeting the needs of our users.

Final Release Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to do Pardus Final official, the following criterias must be met:

* All `beta release requirements`_ must be achieved.
* All bugs blocking the Final tracker must be closed.
* The installation manager (YALI_) must be able to complete an installation using IDE, SATA, SCSI and iSCSI storage devices
* The installation manager (YALI_) must be able to create partition tables using any file system offered in installer configuration and complete installation for LVM, software, hardware or BIOS RAID, or  IDE, SATA, SCSI and iSCSI storage devices.
* The installation manager (YALI_) must boot and run on all `supported architectures`_ from install and live images
* All known bugs can cause corruption of user data be fixed or marked as "High" on `Pardus bugzilla`_
* The following criterias should be met on both live and default installed system for desktop validation
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

Final Tickets
^^^^^^^^^^^^^
#. Decide for RC code name and its Wallpaper
#. Send weekly emails about `urgent package list`_
#. Warn about Final artwork deadlines of each task one week before

   * Final Wallpapers
   * Final Icon theme
   * Final Splash screens
   * Final Web banners
   * DVD, CD cover, guide design
   * Brochures, stand and roll-up design
   * Promotion products design
#. Update feature list according to completed features
#. Warn about Final Freeze (RC Phase) one week before
#. Create Final Test Release for RC validation tests

   * Installation media
   * Live media
#. Prepare and make "where we are meeting" after validation tests
#. Create release-notes
#. Upload release-notes to developer.pardus.org.tr
#. Prepare press release from release-notes
#. Upload press-release to pardus.org.tr
#. Plan the date of product publicity (launching)
#. Track the production of publicity and promotion materials
#. Make stock plan for publicity and promotion materials
#. Create Release Candidate (RC)

   * Installation media
   * Live Media
#. Release RC

   * Upload iso to FTP servers
   * Upload iso to torrents
#. Send an announcement mail for Final release
#. Release Final

   * Open stable binary repository
   * Add stable repository to packages.pardus.org.tr
   * Warn mirrors and ULAKBIM one week before
   * Upload iso to FTP servers
   * Upload iso to torrents
#. Send an announcement mail for Final release
#. Propose Schedule for Next Release
#. Plan tasks for EOL_

Final Tracker Bugs
^^^^^^^^^^^^^^^^^^

A bug is considered an final tracker bug if one of the following criterias is met:

#. If a package in the urgent package list of alpha, beta or final has a bug that can not be fixed with a future update or has a severity_ rating of high or urgent.
#. Bugs that are a blocks the testing and test process. (Bugs related to untestable products)
#. Bug relates to an unachieved `Final Release Requirements`_

Final Postponement
^^^^^^^^^^^^^^^^^^

#. One week before the release day, if all of the `Final Release Requirements`_ are not achieved, the release will be delayed one week that the `Final Release Requirements`_ can be achieved.
#. This delay will be added all remaining tasks and final release date.
#. The decision for the delay will be made on "where we are" meeting that be held 2 weeks prior to the shipping date of the releases.

Validation of Final Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Test team has the responsibility of determining whether the criteria for the
`Final Release Requirements`_ has been met. At the end of the test process,
the test team reports on `Pardus Bugzilla`_ will be reviewed and discussed
at the "where we are" meeting.

.. _beta release requirements: http://developer.pardus.org.tr/guides/releasing/official_releases/beta_release.html#beta-release-requirements
.. _YALI: http://developer.pardus.org.tr/projects/yali/index.html
.. _Kaptan: http://developer.pardus.org.tr/projects/kaptan/index.html
.. _Pardus bugzilla: http://bugs.pardus.org.tr/
.. _supported architectures: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#architecture-support
.. _urgent package list: http://svn.pardus.org.tr/uludag/trunk/scripts/find-urgent-packages
.. _EOL: http://developer.pardus.org.tr/guides/releasing/end_of_life.html
.. _severity: http://developer.pardus.org.tr/guides/bugtracking/bug_cycle.html

