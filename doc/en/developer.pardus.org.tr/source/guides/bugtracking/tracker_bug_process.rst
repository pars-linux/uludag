.. _tracker-bug-process:

**Last Modified Date:** |today|

:Author: Semen Cirit

:Version: 0.1

Tracker Bug Process
===================

Tracker bugs are used to keep track of release blocker bugs. These bugs must be
fixed before related release has shipped.

Each release requirements are used to determine whether a bug is a tracker bug
for given release (see alpha_, beta_, final_ requirements)

This document includes how bugs are proposed, reviewed and accepted as tracker
bugs, and how tracker bugs are then tracked.

Open Tracker Bug Report
-----------------------

Tracker bug report shoul be opened by release manager at the start time of
a new release.

There are four tracker bugs for each release cycle. These reports should be
opened for relevant release product baselayout component and they should be
assigned to relevant release manager.

After that these reports should be depend each other with that order:

::

    -> means depends
    Final -> RC -> Beta -> Alpha

Proposing Tracker Bugs
----------------------

If you think that the bug that you find is a tracker bug for a release, you
should mark it as blocker to the related release. To do this: enter the bug ID
of the tracker bug into the "Blocks:" field in Bugzilla.

When proposing a bug as a tracker, please control whether the bug violates the
relevant release requirements.
See:

    - alpha_ requirements
    - beta_ requirements
    - rc_ requirements
    - final_ requirements

Reviewing Tracker Bugs
----------------------

The tracker bugs are approved or rejected by the collaboration of three groups:
Test_, Development_, Release Team.


The review process can be done on weekly meetings, generally occur on Monday
during release. We plan to make also public weekly IRC meetings for tracker bug
reviews. These reviews can also be done on "where are we" meetings in order to
decide whether a test release for validation should be approved as an `official
release`_ or delayed.

The Bug ID's that are rejected as trackers will be removed from tracker bugs. If
the bug not rejected but will be done for the next release it should be marked
as **RESOLVED/LATER** for fixed bugs and **RESOLVED/REMIND** for bugs not fixed yet.

The accepted bugs as tracker will continue to block the tracker bug, and will be
fixed before the release time.

Tracking Tracker Bugs
---------------------

Tracking tracker bugs and controlling that they are fixed is again an collaborative
affort between Test_, Development_, Release Managing.

The fixing process are `new feature`_, `new package`_, `package update`_ processes.

.. _alpha: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html#alpha-release-requirements
.. _beta: http://developer.pardus.org.tr/guides/releasing/official_releases/beta_phase.html#beta-release-requirements
.. _final: http://developer.pardus.org.tr/guides/releasing/official_releases/final_phase.html#final-release-requirements
.. _rc: http://developer.pardus.org.tr/guides/releasing/official_releases/release_candidate_phase.html#final-release-requirements
.. _Development: http://developer.pardus.org.tr/guides/newcontributor/areas-to-contribute.html#development
.. _Test: http://developer.pardus.org.tr/guides/newcontributor/areas-to-contribute.html#test
.. _official release: http://developer.pardus.org.tr/guides/releasing/official-releases/index.html
.. _bug cycle: http://developer.pardus.org.tr/guides/bugtracking/bug_cycle.html
.. _new feature: http://developer.pardus.org.tr/guides/newfeature/newfeature_requests.html
.. _new package: http://developer.pardus.org.tr/guides/newfeature/new_package_requests.html
.. _package update: http://developer.pardus.org.tr/guides/packaging/package_update_process.html
