Release Process
===============

Pardus releases occur nearly every 8 months. Each release cycle follow general release plan template. Every  Pardus contributor will track these planned points carefully and be sure that their work is in sync with others. Pardus follow a time based release, thus coordination is very important to finish work on time.

General Freezes
---------------

Open developement
^^^^^^^^^^^^^^^^^

- Unrestrained general development activity, new packages and versions are automatically taken and merge without any permission.

Repo Freeze
^^^^^^^^^^^
- At the end of this phase all packages of previous Pardus release packages merge process should be finished.
- After this period, new packages and new versions can be merged under some permissions and restrictions.
- In this freeze time devel branched and testing repository open.

Feature Acceptence Deadline
^^^^^^^^^^^^^^^^^^^^^^^^^^^

- All features from users should be reported to Bugzilla before this deadline

Feature freeze
^^^^^^^^^^^^^^
- New features can not be added to the repositories, only bug fixes can be done. (See `feature freeze`_)

User interface freeze
^^^^^^^^^^^^^^^^^^^^^
- User interface can not be chaged after this time
- It is needed for documentation and screenshots stabilization.

Beta freeze
^^^^^^^^^^^

- The repository is freezed until beta is released, in order to stabilize beta for tests and reach beta to a level similar to final release.
- Bug fixes taken to repository with release manager approval

String freeze
^^^^^^^^^^^^^
- In order to stabilize translations, strings should be freezed on repositories.

Toolchain freeze
^^^^^^^^^^^^^^^^
Last date for toolchain changes.

Kernel freeze
^^^^^^^^^^^^^
- No new kernel versions in order to enable last final hardware compatibility checks, deadline for kernel regression fixes

Translation freeze
^^^^^^^^^^^^^^^^^^
- No translations permitted after this point in order to enable final stabilization and last final tests.

RC freeze
^^^^^^^^^^

- The repository is freezed until Final is released, in order to stabilize RC for tests and reach RC to a level similar to final release.
- Bug fixes taken to repository with release manager approval


General Milestones
------------------

Planning
^^^^^^^^
(about 2 months)

- Package build system up
- Toolchain organized
- Features proposed, discussed on developer meeting, technical group review them and select relevant packages and technologies that fits (`Feature Acceptence Deadline`_)
- Planned feature list announced
- Release plan announced
- New branch officially announce and open for merging packages

See details from `Planning Phase`_.

Alpha 1
^^^^^^^

Intrusive changes phase completed (about 2 months)

- `Open developement`_
- High priority features and tasks finished

See details from `Alpha phase`_

Alpha 2
^^^^^^^
(about 2 weeks)

- `Open developement`_
- Medium priority tasks and features finished
- At the end of this period, all remamined features reviewed and reprioritized or ignored if needed.

See details from `Alpha phase`_

Alpha 3
^^^^^^^
Feature development phase completed (about 2 weeks)

- `Open developement`_
- Where we are meeting to review bugs and possibility to prolonge release.
- Low priority tasks and features finished
- `Feature freeze`_
- `Repo freeze`_ for main/base repo
- `String freeze`_

See details from `Alpha phase`_

Beta 1
^^^^^^
Stabilization phase (about 3 week)

- Review Beta `tracker bugs`_
- No urgent and high bugs present
- Fix high priority `tracker bugs`_
- `Toolchain freeze`_ ?
- `User interface freeze`_
- Announce EOL of 2 previous release
- Translation and user documentation check

See details from `Beta phase`_

Beta 2
^^^^^^
Stabilization phase completed (about 2 week)

- Where we are meeting to review bugs and possibility to prolonge release.
- All normal, low priority `tracker bugs`_ fixed
- `Beta freeze`
- Preperation for final release announcement and marketing materials

See details from `Beta phase`_

RC
^^
(about 2 weeks)

- Where we are meeting to review bugs and possibility to prolonge release.
- Fixing only urgent release tracker bugs, bug fix needs approval.
- `Kernel freeze`_
- `Translation freeze`_
- Repo freeze for contributors
- Request contributor release notes
- Testing targets achieved (All features functional and bug free)
- `RC freeze`_
- Final Marketing and announcement ready

See details from `RC phase`_

Final
^^^^^
(about 2 weeks)

- Only boot and installation urgent release `tracker bugs`_ fixed and needs approval.
- Start new release cycle for the next release

See details from `Final phase`_

LTS technological updates (point releases)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Adding support for new hardware
- Implementing a missing functionality in a component which will probably be needed to satisfy the original reasons for LTS creation
- Reduce download for ongoing updates.
- All work have to finish one month before the release in order to give time for tests

Maintainance
^^^^^^^^^^^^

The maintenance time of a release is about 2 previous release + 1 month (~13 months) (2n +1).

Package maintainers MUST:

- Fix security vulnerability bugs
- Fix severe regressions from the previous release. This includes packages which are totally unusable, like being uninstallable or crashing on startup.
- Fix bugs that directly cause a loss of user data
- Avoid new upstream versions of packages which provide new features, but don't fix critical bugs, a backport should be requested instead.
- Avoid ABI breakage or API changes if at all possible.
- Avoid changing the user experience if at all possible.
- Avoid updates that are trivial or don't affect any user.
- Avoid adding new packages

Package maintainers SHOULD:

- Push only major bug fixes and security fixes to previous release (n-1).

EOL
^^^

- The EOL announce of a release is done at second next release beta 1 version.
- The EOL announce date of a release 2 next release + 1 month (2n +1).

See details from `EOL`_

.. _Planning Phase: http://developer.pardus.org.tr/guides/releasing/official_releases/planning_phase.html
.. _tracker bugs: http://developer.pardus.org.tr/guides/bugtracking/tracker_bug_process.html
.. _feature freeze: http://developer.pardus.org.tr/guides/releasing/feature_freeze.html
.. _Alpha phase: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html
.. _Beta phase: http://developer.pardus.org.tr/guides/releasing/official_releases/beta_phase.html
.. _RC phase: http://developer.pardus.org.tr/guides/releasing/official_releases/release_candidate_phase.html
.. _Final phase: http://developer.pardus.org.tr/guides/releasing/official_releases/final_phase.html
.. _EOL: http://developer.pardus.org.tr/guides/releasing/end_of_life.html
