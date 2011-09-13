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

#. Proposed features are discussed by developers, reviewed by technical group and the final feature list is determined. (Feature Acceptence Deadline)
#. The planned feature list and the release plan/schedule should be announced
#. Pre-alpha should be released

Planning Phase Requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^
In order to release the pre-alpha, the following criteria should be met:

* There must be no unhandled file conflicts and missing package dependencies in the repository
* Pre-alpha image should boot correctly into a working development environment

Planning Phase (Pre-alpha) Schedule
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

8-4 weeks before the Pre-alpha release:
---------------------------------------

#. Prepare and schedule kickoff meeting
#. Open empty `tracker bugs`_ for Alpha, Beta, RC and Final releases
#. Warn the community about the upcoming `feature request`_ and `feature submission`_ deadlines
#. Inform the developers about the toolchain components and compiler/linker flags that will be used
#. Prepare, patch, build recursively (Bootstrap_ if necessary) and test the toolchain components (gcc, glibc, binutils, llvm, etc.)
#. Update, prepare, patch, build and test the system.* packages
#. Prepare the additional packages that can ease the development process (vim, strace, svn, git, etc.)
#. Plan for Pardus artwork
   * Wallpapers
   * Icon Theme
   * Splash Screens/Plymouth

4 weeks before the Pre-alpha release:
-------------------------------------

#. `feature request`_ deadline
#. Start evaluating `feature request`_

3 weeks before the Pre-alpha release:
-------------------------------------

#. `feature submission`_ deadline
#. Announce feature list on developer.pardus.org.tr
#. Create detailed release schedule (prioritize feature list, give other details for development, artwork, documentation etc.) and announce on developer.pardus.org.tr

1 week before the Pre-alpha release:
------------------------------------

#. Warn mirrors and ULAKBİM (hosting agency)

2 days before the Pre-alpha release:
------------------------------------

#. Plan and announce a developer meeting on IRC
#. Prepare and plan Alpha kick-off meeting

Pre-alpha release day:
----------------------

#. Publish the image

    * Upload to FTP servers
    * Upload to torrents

#. Announce pre-alpha release on `developer list`_ and `gelistirici list`_

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
.. _PiSi: http://developer.pardus.org.tr/projects/pisi/index.html
