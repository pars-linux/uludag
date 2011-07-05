Planning Phase
==============

:Author: Semen Cirit
:Last Modified Date: |today|
:Version: 0.1

The planning phase is a phase to giving a start to a new release and takes
about 2 months.

Feature acceptence deadline is held during this phase and the `requested features`_
from users and developers are reported to `Pardus Bugzilla`_ before this deadline.

The requested features are reviewed and also prioritized during this period
and no more features are added to this list.

The roadmap of the release is planned during this phase. Requirements and
specifications freeze and reported on `Pardus Bugzilla`_.

Planning Phase Goals
--------------------

#. Toolchain organized
#. Features proposed, discussed on developer meeting, technical group review them
    and select relevant packages and technologies that fits (Feature Acceptence Deadline)
#. Planned feature list announced
#. Release plan announced
#. New branch officially announce and open for merging packages (Ready for all developers)

Alpha Release Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^
In order to do Pardus Developer Release official, the following criterias must be meet:

* There must be no file conflicts or unresolved package dependencies in developer release iso images
* The iso image must boot.
* The installation manager (YALI_) must be able to complete the installation using the install options use all space or use free space.
* PiSi_ must have the correct repository and be able to download and install updates

Planning Phase (Developer Release) Tickets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#. Prepare and plan start meeting
#. Open `devel source`_ and  `devel binary`_ repositories
#. Add new devel repository to http://packages.pardus.org.tr
#. Open `tracker bugs`_ for Alpha, Beta, Final
#. Warn users and developers about `feature request`_ deadline one week before
#. Prepare buildfarm servers
#. State toolchain versions
#. State compiler flags
#. Prepare toolchain
#. Bootstrap_
#. Compile developer tools
#. Install and build buildfarm_ systems
#. Enable `nightly builds`_
#. Enable automatic mails about nightly build changes to `tester list`_.
#. Review package components for orphan and dead packages
#. Warn developers about their orphan and dead packages and developer release
#. Plan for artwork pardus
   * Final Wallpapers
   * Final Icon theme
   * Final Splash screens
Release minus 3 week:
#. Warn developers about `feature submission`_ deadline
#. Create accepted feature list
#. Put feature list to developer.pardus.org.tr
#. Create detailed release schedule (priotirize feaute list, give other details for development, artwork, documentation etc.)
#. Update schedule on developer.pardus.org.tr

Release minus 1 week:
#. Warn mirrors and ULAKBIM one week before

Release minus 2 day:
#. Plan and announce a developer meeting on IRC
#. Prepare and plan Alpha start meeting

Release:
#. Publish the image
    #. Upload iso to FTP servers
    #. Upload iso to torrents
#. Announce pre-alpha (developer) release on `developer list`_ and `gelistirici list`_

.. _requested features: http://developer.pardus.org.tr/guides/newfeature/index.html
.. _Pardus Bugzilla: http://bugs.pardus.org.tr/
.. _tracker bugs: http://developer.pardus.org.tr/guides/bugtracking/tracker_bug_process.html#open-tracker-bug-report
.. _devel source: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#devel-folder
.. _devel binary: http://developer.pardus.org.tr/guides/releasing/repository_concepts/software_repository.html#devel-binary-repository
.. _Bootstrap: http://developer.pardus.org.tr/guides/releasing/bootstrapping.html
.. _buildfarm: http://developer.pardus.org.tr/guides/releasing/preparing_buildfarm.html
.. _nightly builds: http://developer.pardus.org.tr/guides/releasing/generating_nightly_builds.html
.. _severity: http://developer.pardus.org.tr/guides/bugtracking/howto_bug_triage.html#bug-importance
.. _tester list: http://lists.pardus.org.tr/mailman/listinfo/testci
.. _feature request: http://developer.pardus.org.tr/guides/newfeature/newfeature_requests.html#how-do-i-propose-a-new-feature-that-i-do-not-contribute
.. _feature submission: http://developer.pardus.org.tr/guides/newfeature/newfeature_requests.html#how-my-new-feature-request-is-accepted
.. _developer list: http://lists.pardus.org.tr/mailman/listinfo/pardus-devel
.. _gelistirici list: http://lists.pardus.org.tr/mailman/listinfo/gelistirici
.. _YALI: http://developer.pardus.org.tr/projects/yali/index.html

