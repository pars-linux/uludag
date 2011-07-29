.. _point-release:

Point Release (Technological updates)
=====================================

:Author: Semen Cirit
:Last Modified Date: |today|
:Version: 0.1

This phase is the continuation of long term support releases and released once a year. 

It takes about 6 months.

The point release `tracker bugs`_ are fixed, package integrity and feasibility
are checked, last desktop and installation validation tests are done.

Point Release Goals
^^^^^^^^^^^^^^^^^^^
- Adding support for new hardware
- Implementing a missing functionality in a component which will probably be needed to satisfy the original reasons for LTS creation
- Reduce download for ongoing updates.
- All work have to finish one month before the release in order to give time for tests


Point Release Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to do Pardus Point release official, the following criterias must be met:

* All `Final release requirements`_ must be achieved.
* All bugs blocking Point release tracker must be closed.
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

Point Release Tickets
^^^^^^^^^^^^^^^^^^^^^
Between release 6 months and 3 months:

#. Continue stable repo updates as normal
#. Decide about what will be done for the technological update and take decisions from
    #. External project coordinator
    #. Customers
    #. Base team
    #. Technology coordinator
#. Open a point release tracker bug and depend decided specifications to this bug
#. Review and triage these bugs

Release minus 3 moths:

#. Continue stable repo updates as normal
#. Start to fix point release `tracker bugs`_

Relase minus 1 month:

#. Test all `tracker bugs`_ and fix regressions

Release minus 3 weeks:

#. Create release-notes
#. Prepare press release from release-notes
#. Warn mirrors and ULAKBIM
#. Create Test Release for validation tests

   * Installation media
   * Live media
#. Prepare and make "where we are meeting" after validation tests, in order to review bugs and possibility to prolonge release.
#. Review problems and mark as Point release tracker bug which need resolution before release

   * Package conflicts or unresolved package dependencies
   * Installation bugs
   * High severity bugs
#. Fix release urgent `tracker bugs`_

Release:

#. Upload release-notes to developer.pardus.org.tr
#. Upload press-release to pardus.org.tr
#. Release Point release

   * Upload iso to FTP servers
   * Upload iso to torrents

#. Announcement for  release on `duyuru list`_ and `announce list`_

Point Release Tracker Bugs
^^^^^^^^^^^^^^^^^^^^^^^^^^

A bug is considered a point release tracker bug if one of the following criterias is met:

#. If a package in the urgent package list of alpha, beta or final has a bug that can not be fixed with a future update or has a severity_ rating of high or urgent.
#. Bugs that are a blocks the testing and test process. (Bugs related to untestable products)
#. Bug relates to an unachieved `Point Release Requirements`_

Validation of Point Release Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Test team has the responsibility of determining whether the criteria for the
`Point Release Requirements`_ has been met. At the end of the test process,
the test team reports on `Pardus Bugzilla`_ will be reviewed and discussed
at the "where we are" meeting.

.. _YALI: http://developer.pardus.org.tr/projects/yali/index.html
.. _Kaptan: http://developer.pardus.org.tr/projects/kaptan/index.html
.. _Pardus bugzilla: http://bugs.pardus.org.tr/
.. _supported architectures: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#architecture-support
.. _urgent package list: http://svn.pardus.org.tr/uludag/trunk/scripts/find-urgent-packages
.. _EOL: http://developer.pardus.org.tr/guides/releasing/end_of_life.html
.. _severity: http://developer.pardus.org.tr/guides/bugtracking/howto_bug_triage.html#bug-importance
.. _tracker bugs: http://developer.pardus.org.tr/guides/bugtracking/tracker_bug_process.html
.. _duyuru list: http://lists.pardus.org.tr/mailman/listinfo/duyuru
.. _Final release requirements: http://developer.pardus.org.tr/guides/releasing/official_releases/final_phase.html#final-release-requirements
.. _announce list: http://lists.pardus.org.tr/mailman/listinfo/pardus-announce
