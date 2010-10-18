.. _stock-responses:

Bugzilla Stock Responses
========================

To make Pardus better, the bugzilla bug tracking tool is used. But many bugs in Pardus
bugzilla needs additional information in order to be fixed by developers. We create
stock responses based on our previous experiences, in order to give quick responses to
problematic bug reports. This helps bug triagers and developers request missing
information quickly in a clear, friendly, and consistent manner.

Insufficient Report
-------------------
If the description of the bug is incomplete, please add "NEEDINFO" keyword and give
the following response:

::

    Thank you for the bug report. Unfortunately, we do not reproduce and  understand
    the problem you are having. If you have time and can still reproduce the bug,
    please read http://developer.pardus.org.tr/guides/bugtracking/bug_and_feature_request.html
    and add a description along those lines to this bug report so we can diagnose the
    problem. Thank you.

If you can request more specific thingd than this, that would be very helpful for the
reporter.


Duplicate Bugs
--------------

If the bug has a duplicate, please mark the less informed bug as "DUPLICATE", and
give the following message:

::

    Thank you for the bug report. This bug has already been reported into our bug
    tracking system, but please feel free to report any further bugs you find.

More than one issues reported in one bug
----------------------------------------

::

    Thank you for the bug report. In order to track bugs appropriately, the bug writing
    guidelines (https://bugs.pardus.org.tr/page.cgi?id=bug-writing.html) say that reporters
    file one bug per issue. It seems that this bug contains multiple issues. If you have
    time and can still reproduce the bug (or bugs), please submit them as separate bugs
    for each of your separate issues. One bug can remain in this report; simply edit
    the summary to reflect this. You can note the new bug numbers in a comment for this
    bug. Thank you.

Users generally need more information about the separation of the bugs, please give specific
informations and be polite.

Wrong Component
---------------

If the bug has been reported to the incorrect component, you can use this message
inserting the appropriate component names:

::

    Thank you for the report. It seems that this has been reported to the incorrect
    component. Therefor it is reassigned from <oldcomponent> to <newcomponent>. Feel
    free to report any further bugs you find to our bug tracking system. In order to
    find the correct component, you can refer to: 
    http://developer.pardus.org.tr/guides/bugtracking/correct_component.html


Bugs already fixed
------------------

If the bug may no longer exist, please resolve the bug as "FIXED", and give the
following response:

::

    Thank you for the bug report. Unfortunately we can not reproduce the bug,it may have
    already been fixed. If you have time to update the package and re-test, please do
    so and report the results here.

Bug will be fixed for the next stable update
--------------------------------------------

If the bug is fixed in testing repository and it will be merged to stable repository
in the next update, please resolve the bug as "FIXED", and give the following response:

::

    Thank you for the bug report. This bug was fixed in testing repository and it will
    be published with new stable update. Please feel free to report any further bugs you
    find, or make further reports if this bug is not fixed after you install the update.

Upstream Bugs
-------------

If the bug is not about packaging problems and the maintainer has no plan to work on
this in the near feauture, and the buggy product has an own bug tracking system, please
resolve the bug as "WONTFIX", and give the following response:

::

    Thank you for the bug report. This bug is not about a packaging problem, and at the
    moment, the Pardus developers are busy fixing other issues and may not have time to
    work on issues about upstream. You may report it to the authors (upstream) of the
    program.

    Bug tracking systems are used by most upstream authors, and more people who know
    the code will be looking at the bug report there.

    The upstream bug tracking system to use is:
    <link>

    You can add the upstream link to this bug, please make sure that the bug is not
    already been reported in the upstream bug tracking system.

Most used Upstream Bug Tracking List
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

+-------------+-------------------------------------------------------------+
| Gnome       | http://bugzilla.gnome.org/                                  |
+-------------+-------------------------------------------------------------+
|  KDE        | http://bugs.kde.org/                                        |
+-------------+-------------------------------------------------------------+
|  Mozilla    | https://bugzilla.mozilla.org/                               |
+-------------+-------------------------------------------------------------+
| Freedesktop | http://bugs.freedesktop.org/                                |
+-------------+-------------------------------------------------------------+
| OpenOffice  | http://qa.openoffice.org/issue_handling/project_issues.html |
+-------------+-------------------------------------------------------------+

Duplicate Upstream Bugs
-----------------------

If the bug is not about a packaging problem, and it has already been reported to upsream
bug tracking system, please resolve it as "WONTFIX", and give the following response:

::

    Thank you for the bug report. This particular bug has already been reported to the
    upstream of the software. You can add any additional information to the upstream
    bug report at:
    <link>
    If you want to follow what happens to the bug, you can add yourself to the upstream
    report.

End of Life (EOL) product
-------------------------

If a release comes to its end of life, its bugs resolution will be "WONTFIX":

::

    Thank you for your bug report. Unfortunately, with the upcoming Pardus <new release name>
    release, Pardus <EOL release name> which was in security-only mode for a while will soon
    reach its end-of-life and the current bug reports concerning Pardus <EOL release name>
    will become invalid. If you can still reproduce the bug on Pardus <new release name>,
    you can reopenthe bug and update the version information. Thanks.


Unmaintained Packages by Upstream
---------------------------------

If the upstream no longer maintains the software, the resolution for these reports is "WONTFIX":

::

    Thank you for your report. The uptream of this software are no longer maintain it so
    Pardus does not provide or support it also. You can see from <upstream url> that it
    does not seem to have been updated since <last date>. Therefore there is unfortunately
    nothing the Pardus project can do to help you with this problem.


Stack Trace
-----------

If the bug caused by a crash, but a stack trace is missing in the bug report:

::

    Thank you for the bug report. But we need a stack trace from the crash. It is
    impossible to analyse the cause without any stack trace. Please see 
    http://developer.pardus.org.tr/guides/bugtracking/stack_traces.html
    for more information about getting a useful stack trace with debugging symbols.

Extra information for some bugs
-------------------------------

X Server Bugs
^^^^^^^^^^^^^

Some files can be needed for X11 server bugs:

::

    Thanks for the bug report. Your report have been reviewed, wee need some additional
    information that will be helpful in order to analyse this issue.

    Please attach your X server config file (/etc/X11/xorg.conf), X server log file
    (/var/log/Xorg.*.log) and the output of "dmesg" to the bug report as individual
    uncompressed text/plain file attachments using the bugzilla file attachment link
    above called "Add an attachment". Thanks.

.. ATI/AMD and Nvidia Driver Bugs
.. ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


.. KMS/Radeon Bugs
.. ^^^^^^^^^^^^^^^^

**Last Modified Date:** |today|

:Author: Semen Cirit

