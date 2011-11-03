.. _bug-cycle:


**Last Modified Date:** |today|

:Author: Semen Cirit

:Version: 0.2

Bug Cycle
~~~~~~~~~

 .. image:: images/bugcycle2.png

This document gives information about Pardus bug tracking system process.

Bugzilla Status
===============

Status gives the bug state.

**NEW**  When the bug is newly submitted it takes **NEW** status. Some details needed when reporting a bug, see http://bugs.pardus.org.tr/page.cgi?id=bug-writing.html

**ASSIGNED** When a developer starts to deal with the bug he/she changes the status to **ASSIGNED**.

**RESOLVED**  It can be set by a triager, but the triagers may not rechange the status, when the assignee and/or package maintainer change the initial status chosen by the triager.
     - WONTFIX: Bugs are not related to Pardus and will never be fixed
     - DUPLICATE: Bugs which have duplicates which are already been reported
     - REMIND: Bugs can be fixed for the next release or for a later time
     - LATER: Bugs fixed and can be merged for the next release or for a later time
     - INVALID: Bugs that are not really a bug
     - WORKSFORME: Bugs could not be reproduced
     - NEXTRELEASE: Bugs are already fixed in current release, but will not be fixed for (n-1) previous release
     - FIXED: When the developer is sure that the bug is fixed, he/she should mark the bug as fixed via SVN commits:

          The SVN commit should include::

            "BUG:FIXED:<BUGID>"

          This commmit will automatically change the resolution of the bug as **RESOLVED/FIXED**
**VERIFIED**
     - FIXED: The fixed bug is pass the test, the bug resolution is changed to **VERIFIED/FIXED**

**REOPENED** A bug can be reopened with **REOPENED** status by anyone, if the reason for marking the report as **RESOLVED** seems insufficient or the problem persists.

**CLOSED** If the bug fix passes the test and is merged to stable Pardus repositories.


Bugzilla Severities
===================

Severity is used to set how severe the bug is. It can be set by a triager, but the triagers may not rechange the severity, when the assignee and/or package maintainer change the initial severity level chosen by the triager.

**Urgent:** Freeze, panics and crashes that are reproducible on all type of systems, make *the whole system* unusable and security related bugs. These bugs should be fixed promptly.

**High:** Bugs that are reproducible on all type of systems and make *the program* unusable (packages which are totally unusable and have missing dependency, like being uninstallable or crashing on startup, bugs cause that cause loss of user data). These bugs should be fixed in 1 month.

**Normal:** Bugs that are reproducible on all type of systems and make *a part of the program* unusable. These bugs will probably be fixed in 6 months.

**New feature:** New feature requests. These requests will probably be done for the next release.

**Low:** The others - a cosmetic problem, such as a misspelled word or misaligned text or an enhancement, bugs that are not reproducible on all systems. These bugs are not schduled to be fixed in the next 6 months. This is not the same as planning not to fix the bug; it means that we don’t know when we will fix it, if at all.

Notes: Hardware specific bugs are generally seen as urgent, but it should be generally high. Because urgent severity is used when the entire system does not work, but a bug restricted to a specific hardware usually has a high severity.

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

**EXCEPTION**   Use when the bug needs a new feature or new bug exception.

.. **MERGEREQUEST** Use when the bug fix needs a merge request for testing source repository.

**APPROVED** Use when the merge or exception request is approved.

**MERGED** Use when the bug is merged to testing source repository.

**COMPILED** Use when the bug is fixed, merged and compiled in testing source repository.

**JUNIORJOBS**  Use when a bug is chosen as a junior job for expected developers.

**NEEDSMENTORING** Use when the expected developer choosed a bug and fixed it, and wants to see fix in Pardus repositories.

**MENTORED** Use when the developer takes review and merge responsibility of an expected developer.

**REVIEWED** Use when the expected developer work review is finished and work is ready for merge.

**MENTORASSIGNED**  Use when assigning a mentor to a developer applicant.

**ACKS** Use when a component supervisor gives an approvement for package review.

**ACKD** Use when a developer gives an approvement for package review.

.. _alpha: ../releasing/official_releases/alpha_phase.html
.. _Alpha 1: ../releasing/official_releases/alpha_phase.html#alpha-1
.. _Alpha 2: ../releasing/official_releases/alpha_phase.html#alpha-2
.. _Alpha 3: ../releasing/official_releases/alpha_phase.html#alpha-3
.. _beta: ../releasing/official_releases/alpha_phase.html
.. _Beta 1: ../releasing/official_releases/alpha_phase.html#beta-1
.. _Beta 2: ../releasing/official_releases/alpha_phase.html#beta-2

