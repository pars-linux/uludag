.. _howto-bug-triage:

Starting Bug Triage
===================

**Last Modified Date:** |today|

:Author: Semen Cirit

:Version: 0.1

Choosing Bugs
-------------

* Bug triage is done at product and component base. (See http://bugs.pardus.org.tr/describecomponents.cgi)
* Bug triage can be done excluding Community Services and Distribution Process classes.
* The prepared stock responses are so valuable in order to tackle bugs. (See :ref:`stock-responses`)

Understanding Bugzilla
----------------------

    * See :ref:`bug-cycle`

Check list for bugs have NEW status
-----------------------------------

This checklist is used for bugs which have NEW status.

#. Does the bug report mention about a real bug?

    * In some cases, users need some help about configuring or using software. These reports are not related with bug or feature request. These type of reports should be closed with RESOLVED/INVALID resolution, and a polite comment should be give in order to guide user to related forums or mail lists.
    * New package request severities should be "Low"
    * New feature request severties should be "newfeature"

#. Is the bug product and component right?

    * To take technical assistance please see :ref:`correct-component`.
    * If the bug component is assigned to wrong, it should be changed.
    * In some cases, it is not possible to find correct component, until the source code is examined. In such a situation, you can take help from assigned developer.

#. Has the bug a duplicate?

    * If so, the less informed bug resolution should be set as "RESOLVED/DUPLICATE" with bug number of the most detailed report and `related stock response <http://developer.pardus.org.tr/guides/bugtracking/stock_responses.html#duplicate-bugs>`_ is gived as a comment.
    * If it is not clear that a bug is a duplicate of another bug, please politeliy convince reporter with your comment.
    * For additional help: :ref:`finding-duplicates`.
    * Also:
          * Observe `Most frequently reported bugs <http://bugs.pardus.org.tr/duplicates.cgi>`_.
          * Analyse the bugs assigned same component.
          * Use advance search for the bugs assigned different components and try to find similarities.

#. Do the bugs depend each other?

    * If a bug fix helps another bugs resolution, or vice versa, please explain it with comments on each bug.
    * If you are sure about this dependence, add the number of the bug which should be fixed first to the other bug "Depends on" part.

#. Are more then one bug is reported in one report?

    * Please send `related stock response <http://developer.pardus.org.tr/guides/bugtracking/stock_responses.html#more-than-one-issues-reported-in-one-bug>`_ as a comment.

#. Is there enough information for developer to fix the bug?

    * If not,
          * Request for more information from the reporter (please be polite). Leave the bug status as "NEW" and state "NEEDINFO" as a keyword.
          * Please add your own idea to the comment. This idea generally comes into mind, while trying to reproduce the bug. Additionaly you can comment according to attachments.
    * Look `Gather information from specific Bugs <http://developer.pardus.org.tr/guides/bugtracking/bug_and_feature_requests.html#gather-information-for-specific-bugs>`_ for necessary bug information:
          * Are the steps for reproduce explained clearly?
          * Were the relevant log files and outputs added to the report?
          * If a crash occured, did the stack trace is added?

#. Do the summary helps the bug?

    * If the summary part is far away from the meaning of the bug or confusing, feel free to change it. 
    * Please try not to change the idea of the reporter.

#. Which severity should I use?

    During bug triage process, it is very important to state bug severity. Most bugs assigned with severity "normal", but the severity of the bug should change related to following criterias.

    * Urgent: Bugs which make the whole system unusable.
    * High: Bugs which make the program unusable
    * Normal: Bugs which make a part of the program unusable.
    * Low: A cosmetic problem, such as a misspled word or missaligned text or an enhancement
    * New Features: New feature requests.

    Hardware specific bugs generally seemed as urgent, but it should be generally high. Because urgent severity is used when the entire distribution does not work, but a bug restricted to a specific hardware usually has a high severity.

#. Is the bug a blocker bug? (For release tracker bugs)

    Only ongoing releases has tracker bugs. If a bug is a tracker bug of one of the ongoing release it should be fixed before the release time. When it did not fix, it delays the release. Therefore the bug numbers which has a power to block the release should be set to "Depends on" part of release tracker bug. 

#. How to resolve bugs?

    Many bugs can be fixed unintentially or by upstream. If you realised that the bug is fixed by an update, mark it "RESOLVED/FIXED".

    When a bug fixed by its maintainers, the bug will be marked as "RESOLVED/FIXED" autmatically via commit messages.

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

        - If it can be reproducible only for the release reaches its end of life, relove the bug as "RESOLVED/INVALID".
        - If the bug can be reproduced for the stable and test repository release at the same time, this is evidence that the bug is not due to a specific configuration or hardware.
        - If the bug can be reproduced for the stable repository release but not for test repository release this is strong evidence that the bug has already been fixed. Give a bug comment that "this bug will be fixed after the package merges to stable". You can resolve the bug as "RESOLVED/FIXED"
        - If the bug cannot be reproduced for the stable repository release, this is strong evidence that the bug is due to something different in the environment of the reporter.
            - Make sure that the reporter system is up to date
            - Make sure that you are using exactly the same method to reproduce the bug as the reporter.
            - If you suspect user specific operation, ,ask the reporter to create a new Unix user and try to reproduce with that user.
            - If you suspect machine specific operation, ask the reporter to try reproduction with reinstalling problematic package with moving any cached data or configuration files. 
            - If you suspect a hardware-specific problem, you might request a information about the relevant hardware

#. Has the bug already been reported to upstream?

    - Search the bug in the upstream Bugzilla or mailing list, if they exist.
    - If you find a duplicate report, give a link to Pardus bug report and leave the bug open.

    Upstream bug reporting systems:

        * `KDE Bugzilla <https://bugs.kde.org/>`_
        * `Linux Kernel Bugzilla <https://bugzilla.kernel.org/>`_
        * `Mozilla Bugzilla <https://bugzilla.mozilla.org/>`_.
        * `OpenOffice IssueZilla <http://qa.openoffice.org/issues/query.cgi>`_
        * `Gnome Bugzilla <https://bugzilla.gnome.org/>`_
        * `Xfce Bugzilla <http://bugzilla.xfce.org/>`_

.. Mark as triaged
.. ----------------

.. If you finish triage, you should add "TRIAGED" keyword, in order to avoid retriage.

Pursuance
---------

If you set a NEEDINFO keyword in a bug, you have to control the bug during 30 days if the reporter or other commenter give an additional information in order to reproduce the bug, you have to remove "NEEDINFO" keyword. If any user return the bug durin 30 days bug will automatically closed.


EOL Bug Triage
--------------

For bugs filed against Pardus releases that have reached their End of Life (EOL):

    * If the bug appears to be occurring in a more recent (non-EOL) version, update the version number and leave the bug open,
    * Otherwise, mark the bug CLOSED/WONTFIX and add the `EOL stock response <http://developer.pardus.org.tr/guides/bugtracking/stock_responses.html#end-of-life-eol-product>`_.


General Advice
--------------

    * Please be polite when triaging bugs; we need reporters in order to improve Pardus
    * Please try to reproduce the bug before requesting additional infor mation. Avoid requesting information and re-testing that isn't really necessary; this is obviously frustrating for them.
    * Avoid marking a bug as a duplicate that isn't really the same. If you don't have the technical expertise to be certain, just add a comment with the other bug number, and say it's a possible duplicate.
    * If the developer has commented on the bug or filed it themselves. Let the bug to developer, if more information was needed, they probably would have requested it themselves.
    * You can take help from `testing list <http://lists.pardus.org.tr/mailman/listinfo/testci>`_ 
    * Add yourself to the CC: list of bugs you triage.
    * Please read carefully, and think before you click.
    * Use :ref:`stock-responses` as appropriate.

