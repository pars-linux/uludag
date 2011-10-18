.. _bug-cycle:


**Last Modified Date:** |today|

:Author: Semen Cirit

:Version: 0.2

Bug Cycle
~~~~~~~~~

 .. image:: images/bugcycle.png

This document gives information about Pardus bug tracking system process.

Bugzilla Status
===============

Status gives the bug state.

**NEW**  When the bug is newly submitted it takes **NEW** status. Some details needed when repoting a bug, see http://bugs.pardus.org.tr/page.cgi?id=bug-writing.html

**ASSIGNED** When a developer starts to deal with the bug he/she changes the status to **ASSIGNED**.

**RESOLVED**  It can be set by a triager, but the triagers may not rechange the this status, when the assignee and/or package maintainer change the initial status chosen by the triager.
     - WONTFIX: Bugs are not related to Pardus and will never be fixed
     - DUPLICATE: Bugs which have duplicates which are already been reported
     - REMIND: Bugs can be fixed for the next release or for a later time
     - LATER: Bugs fixed and can be merged for the next release or for a later time
     - INVALID: Bugs that are not realy a bug
     - WORKSFORME: Bugs could not be reproduced
     - NEXTRELEASE: Bugs are already fixed in current release, but will not fixed for (n-1) previous release
     - FIXED: When the developer has been sure that the bug fixed, he/she should be fixed bug via SVN commits:

          The SVN commit should include::

            "BUG:FIXED:<BUGID>"

        This commmit will automatically change the resolution of the bug as **RESOLVED/FIXED**
**VERIFIED**
        - FIXED: The fixed bug is pass the test, the bug resolution is changed to **VERIFIED/FIXED**

**REOPENED** If the fixed bug test fail, the bug resolution is changed to **REOPENED**

**CLOSED** If the bug pass test and merge to stable Pardus repositories


Bugzilla Severities
===================

Severity is used to set how sewere the bug is. It can be set by a triager, but the triagers may not rechange the severity, when the assignee and/or package maintainer change the initial severity level chosen by the tria
ger.

**Urgent:** Freeze, panics and crashes that reproducible on all type of systems and makes the whole system unusable and security related bugs. These bugs should fixed promptly.

**High:** Bugs that are reproducible on all type of systems and makes the program unusable (packages which are totally unusable and have missing dependency, like being uninstallable or crashing on startup, bugs cause that cause loss of user data). These bugs should be fixed in 1 months.

**Normal:** Bugs that are reproducible on all type of systems and makes a part of the program unusable. These bugs are probably be fixed in 6 months.

**New feature:** New feature requests. These requests will probably be done for the next release.

**Low:** The others - a cosmetic problem, such as a misspelled word or misaligned text or an enhancement, bugs that are not reproducible on all systems. These bugs are not schduled to fix in the next 6 months. This is not the same as planning not to fix the bug; it means that we don’t know when we will fix it, if at all.

Notes: Hardware specific bugs generally seemed as urgent, but it should be generally high. Because urgent severity is used when the entire distribution does not work, but a bug restricted to a specific hardware usually has a high severity.

Bugzilla Priorities
===================

Priority is used in release cycle operations and give timeline and precedence of work for alpha_ and beta_ phases. Pardus use 3 priority level in order to give the time interval of the issues.

**P1** High priority features that should be fixed before `Alpha 1`_ release time. High priority bugs that should be fixed before `Beta 1`_ release time.

**P2** Normal priority features that should be fixed before `Alpha 2`_ release time. Normal priority bugs that should be fixed before `Beta 2`_ release time.

**P3** Low priorty features that should be fixed before `Alpha 3`_ release time. Low priority bugs that should be fixed before `Beta 2`_ release time.

Bugzilla Keywords
=================

**NEEDINFO**    Use when a bug needs and information or feedback from user.

**TRIAGED**     Use when the bug is triaged and ready for developer.

**UPSTREAM**    Use when the bug is filed to upstream developer and wait for the fix.

**EXCEPTION**   Use when the bug needs a new feature or new bug exception

**MERGEREQUEST** Use when the bug fix needs a merge request for testing source repository

**APPROVED** Use when the merge or exception request is approved

**MERGED** Use when the bug is merged to testing source repository

**COMPILED** Use when the bug is fixed, merged and compiled in testing source repository

**JUNIORJOBS**  Use when a bug is chosen as a junior job for expected developers

**NEEDSMENTORING** Use when the expected developer choosed a bug and fixed it, and wants to see fix in Pardus repositories

**MENTORED** Use when the developer takes review and merge responsibility of an expected developer bug

**REVIEWED** Use when the expected developer job review was finished and job is ready for merge

**MENTORASSIGNED**  Use when assigne a mentor to developer applicant

**ACKS** Use when a component supervisor gives an approvement for package review

**ACKD** Use when a developer gives an approvement for package review

.. _alpha: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html
.. _Alpha 1: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html#alpha-1
.. _Alpha 2: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html#alpha-2
.. _Alpha 3: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html#alpha-3
.. _beta: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html
.. _Beta 1: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html#beta-1
.. _Beta 2: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html#beta-2

