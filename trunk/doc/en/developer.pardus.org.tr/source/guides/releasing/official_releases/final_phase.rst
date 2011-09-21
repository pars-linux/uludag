.. _final-release:

Final Release
=============

:Author: Semen Cirit
:Last Modified Date: |today|
:Version: 0.2

This phase indicates that the software has reached a point that it is ready to and
has been delivered and provided to the users.

It takes about two weeks.

The Final release `tracker bugs`_ are fixed, package integrity and feasibility
are checked, last desktop and installation validation tests are done.

Final Goals
^^^^^^^^^^^

* Provide a tracker bug free final release suitable for meeting the needs of our users.

Final Release Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to do Pardus Final official, the following criterias must be met:

* All `RC release requirements`_ must be achieved.
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
* Upgrade manager should be ready for upgrade.

Final Schedule
^^^^^^^^^^^^^^
2 weeks before Final:
---------------------

#. Create release-notes
#. Prepare press release from release-notes
#. Track the production of publicity and promotion materials
#. Warn mirrors and ULAKBIM one week before

Release minus 5 days:

#. Get ready the publicity and promotion materials and start to deliver them

3 days before Final:
--------------------

#. `Final freeze`_
#. Only boot and installation urgent `tracker bugs`_ fixed and needs approval.

Final release date:
-------------------

#. Upload release-notes to developer.pardus.org.tr
#. Upload press-release to pardus.org.tr
#. Release Final

   * Upload iso to FTP servers
   * Upload iso to torrents

#. Announcement for Final release on `duyuru list`_ and `announce list`_

1 day after Final release day:
------------------------------

#. Continue new next release process

2 month after Final release day:
--------------------------------

#. EOL_ of the previous release

Final Tracker Bugs
^^^^^^^^^^^^^^^^^^

A bug is considered a final tracker bug if one of the following criterias is met:

#. If a package in the urgent package list of alpha, beta or final has a bug that can not be fixed with a future update or has a severity_ rating of high or urgent.
#. Bugs that are a blocks the testing and test process. (Bugs related to untestable products)
#. Bug relates to an unachieved `Final Release Requirements`_

Validation of Final Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Test team has the responsibility of determining whether the criteria for the
`Final Release Requirements`_ has been met. At the end of the test process,
the test team reports on `Pardus Bugzilla`_ will be reviewed and discussed
at the "where we are" meeting.

.. _RC release requirements: http://developer.pardus.org.tr/guides/releasing/official_releases/release_candidate_phase.html#rc-release-requirements
.. _YALI: http://developer.pardus.org.tr/projects/yali/index.html
.. _Kaptan: http://developer.pardus.org.tr/projects/kaptan/index.html
.. _Pardus bugzilla: http://bugs.pardus.org.tr/
.. _supported architectures: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#architecture-support
.. _urgent package list: http://svn.pardus.org.tr/uludag/trunk/scripts/find-urgent-packages
.. _EOL: http://developer.pardus.org.tr/guides/releasing/end_of_life.html
.. _severity: http://developer.pardus.org.tr/guides/bugtracking/howto_bug_triage.html#bug-importance
.. _tracker bugs: http://developer.pardus.org.tr/guides/bugtracking/tracker_bug_process.html
.. _duyuru list: http://lists.pardus.org.tr/mailman/listinfo/duyuru
.. _announce list: http://lists.pardus.org.tr/mailman/listinfo/pardus-announce
.. _Final freeze: http://developer.pardus.org.tr/guides/releasing/freezes/final_freeze.html

