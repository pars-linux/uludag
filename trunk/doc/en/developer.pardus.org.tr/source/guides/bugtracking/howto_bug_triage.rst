.. _howto-bug-triage:

Starting Bug Triage
===================

**Last Modified Date:** 03-08-2011

:Author: Semen Cirit

:Version: 0.2

First Steps to Contribute Triaging
----------------------------------

#. Track closely `bugzilla mail list`_ and read triaged bugs carefully.
#. Take an account from Pardus bugzilla_
#. Read this document carefully :)
#. Begin with writing comments little by little to the bugs on bugzilla_ for triaging
#. When you feel ready for triaging, please send a message to `test list`_ with your triaged bug ids, the experienced triagers will review your triaged bugs and approve your triaging request (At this point, you will take permissions for changing bug status, severity etc. to deeply triage).

Choosing Bugs
-------------

* Bug triage is done at product and component base. (See http://bugs.pardus.org.tr/describecomponents.cgi)
* Bug triage can be done excluding Community Services and Distribution Process classes.
* You are encouraged to use our prepared stock responses which are also valuable in order learn how to respond to bugs in certain situations. (See :ref:`stock-responses`)

Understanding Bugzilla
----------------------

* See `bug cycle`_

Check list for bugs have NEW status
-----------------------------------

This checklist is used for bugs which have **NEW** status.

#. Does the bug report mention about a real bug?

    * In some cases, users need some help about configuring or using software. These reports are not related with bug or feature request. These type of reports should be closed with **RESOLVED/INVALID** resolution, and a polite comment should be give in order to guide user to related forums or mail lists.

#. Is the bug product and component right?

    * To take technical assistance please see :ref:`correct-component`.
    * If the bug component is wrong, it should be changed.
    * In some cases, it is not possible to find correct component, until the source code is examined. In such a situation, you can take help from assigned developer.

#. Has the bug a duplicate?

    * If so, the less informed bug resolution should be set as **RESOLVED/DUPLICATE** with bug number of the most detailed report and `duplicate bug stock response`_ is given as a comment.
    * If it is not clear that a bug is a duplicate of another bug, please politely ask the reporter for more information with your comment and the suspected bug report.
    * For additional help: :ref:`finding-duplicates`.
    * Also:
          * Observe `Most frequently reported bugs`_.
          * Analyse the bugs assigned to the same component.
          * Use advanced search for the bugs assigned to different components and try to find similarities.

#. Do the bugs depend each other?

    * If a bug fix helps another bugs resolution, or vice versa, please explain it with comments on each bug.
    * If you are sure about this dependence, add the number of the bug which should be fixed first to the other bug "Depends on" part.

#. Are more then one bug is reported in one report?

    * Please send `more than one issues on same bug stock response`_ as a comment.

#. Is there enough information for developer to fix the bug?

    * If not,
          * Request for more information from the reporter (please be polite). Leave the bug status as **NEW** and state **NEEDINFO** as a keyword.
          * Please add your own ideas to the comment. Ideas generally come to mind, while trying to reproduce the bug. Additionaly you can comment according to attachments.
    * Look `Gather information from specific Bugs`_ for necessary bug information:
          * Are the steps for reproduce explained clearly?
          * Were the relevant log files and outputs added to the report?
          * If a crash occured, did the stack trace is added?

#. Does the summary help the bug?

    * If the summary part is far away from the meaning of the bug or confusing, feel free to change it.
    * Please try not to change the idea of the reporter.

#. Which severity should I use?

    * During bug triage process, it is very important to state bug severity. Most bugs assigned with severity **Normal**, but the severity of the bug should change related to different `bug importances`_.

#. Is the bug a tracker bug? (For `release tracker bugs`_)

    * Only ongoing releases has tracker bugs. If a bug is a tracker bug of one of the ongoing release it should be fixed before the release time. When it did not fix, it delays the release. Therefore the bug numbers which has a power to block the release should be set to "Depends on" part of release tracker bug.

#. How to handle bugs in multiple releases?

    If you experience that a already reported bug is also reproducible for an other Pardus release, explain it as comment.

#. How to reproduce or isolate the cause of the bug?

    In order to reproduce the bug there are two usefull questions to answer:

    - Is the bug due to a specific configuration or hardware?
    - Has the bug already been fixed?


    #. If it is a non-reproducible bug for the reporter, like a crash or intermittent failure:

       - Be sure the reporter system is up to date
       - If the reporter system is not up to date, you can offer the reporter up to date. (Some non-reproducible bugs can be fixed by updates)
       - Some specific configuration or hardware might be cause these type of bugs, so there is no guarantee than update will fix it. But running more recent code makes it more likely developers will track down the cause.


    #. If this is a reproducible bug for the original reporter, you can try to experience the bug yourself.

        - If it can be reproducible only for the releasem that reaches its end of life, resolve the bug as **RESOLVED/INVALID**.
        - If the bug can be reproduced for the stable and test repository releases at the same time, this is evidence that the bug is not due to a specific configuration or hardware.
        - If the bug can be reproduced for the stable repository release but not for test repository release this is strong evidence that the bug has already been fixed. Give a bug comment that "this bug will be fixed after the package is merged to stable". You can resolve the bug as **RESOLVED/FIXED**
        - If the bug cannot be reproduced for the stable repository release, this is strong evidence that the bug is due to something different in the environment of the reporter.
            - Make sure that the reporter's system is up to date
            - Make sure that you are using exactly the same method to reproduce the bug as the reporter.
            - If you suspect the problem may be caused by user settings, ask the reporter to create a new Unix user and try to reproduce with that user.
            - If you suspect the problem may be caused by system specific configuration, ask the reporter to try reproduction with reinstalling problematic package with moving any cached data or configuration files.
            - If you suspect a hardware-specific problem, you might request information about the relevant hardware

#. Has the bug already been reported to upstream?

    - Search the bug in the upstream Bugzilla or mailing list, if they exist.
    - If you find a report that has already reported to upstream, give **UPSTREAM** keyword and a link to Pardus bug report and leave the bug open.

    Upstream bug reporting systems:

        * `KDE Bugzilla <https://bugs.kde.org/>`_
        * `Linux Kernel Bugzilla <https://bugzilla.kernel.org/>`_
        * `Mozilla Bugzilla <https://bugzilla.mozilla.org/>`_.
        * `OpenOffice IssueZilla <http://qa.openoffice.org/issues/query.cgi>`_
        * `Gnome Bugzilla <https://bugzilla.gnome.org/>`_
        * `Xfce Bugzilla <http://bugzilla.xfce.org/>`_

Mark as triaged
----------------

If you finish triage, you should add **TRIAGED** keyword, in order to avoid re-triage.

Pursuance
---------

If you set a **NEEDINFO** keyword in a bug, you have to control the bug during 30 days if the reporter or other commenter give an additional information in order to reproduce the bug, you have to remove "NEEDINFO" keyword. If any user returns the bug during 30 days bug will automatically be closed.


EOL Bug Triage
--------------

For bugs filed against Pardus releases that have reached their End of Life (EOL):

    * If the bug appears to be occurring in a more recent (non-EOL) version, update the version number and leave the bug as is,
    * Otherwise, mark the bug **CLOSED/WONTFIX** and add the `EOL stock response`_.


General Advice
--------------

    * Please be polite when triaging bugs; we need reporters in order to improve Pardus
    * Please try to reproduce the bug before requesting additional information. Avoid requesting information and re-testing that isn't really necessary; this is obviously frustrating for them.
    * Avoid marking a bug as a duplicate that isn't really the same. If you don't have the technical expertise to be certain, just add a comment with the other bug number, and say it's a possible duplicate.
    * If the developer has commented on the bug or filed it themselves, let the bug to developer. If more information was needed, they probably would have requested it themselves.
    * You can take help from `test list`_
    * Add yourself to the CC: list of bugs you triage.
    * Please read carefully, and think before you click.
    * Use :ref:`stock-responses` as appropriate.

.. _bug cycle: ../../guides/bugtracking/bug_cycle.html
.. _bug importances: ../../guides/bugtracking/bug_cycle.html#bugzilla-severities
.. _Freeze, panics: ../../guides/bugtracking/bug_and_feature_requests.html?highlight=crash#freeze-and-panics
.. _crashes: ../../guides/bugtracking/bug_and_feature_requests.html?highlight=crash#crashes
.. _crashing: ../../guides/bugtracking/bug_and_feature_requests.html?highlight=crash#crashes
.. _bugzilla mail list: http://lists.pardus.org.tr/mailman/listinfo/bugzilla
.. _bugzilla: http://bugs.pardus.org.tr/
.. _Most frequently reported bugs: http://bugs.pardus.org.tr/duplicates.cgi
.. _Gather information from specific Bugs: ../../guides/bugtracking/bug_and_feature_requests.html#gather-information-for-specific-bugs
.. _EOL stock response: ../../guides/bugtracking/stock_responses.html#end-of-life-eol-product
.. _test list: http://lists.pardus.org.tr/mailman/listinfo/testci
.. _duplicate bug stock response: ../../guides/bugtracking/stock_responses.html#duplicate-bugs
.. _more than one issues on same bug stock response: ../../guides/bugtracking/stock_responses.html#more-than-one-issues-reported-in-one-bug
.. _release tracker bugs: ../../guides/bugtracking/tracker_bug_process.html
