.. _freeze exception:

Freeze Exceptions
=================

There may exist some exceptions at some points of the Pardus Releases. These exceptions are controlled by release group based on the information gived by the developer who proposes the exception.

Exception Process
-----------------

Each freeze exception should have a bug report for the relevant package (if the package does not exist yet, file a bug about the exception).

All exception bugs should be marked as **EXCEPTION** and cc'ed to release group mail list.

All freeze exception bugs must include the following information, in order to provide enough information to decrease the risk of regressions against the benefit of the changes:

   #. Give description of what you want to change in order to presume potential impact on the distribution.
   #. Rationale for why the change is important enough to be allowed in after the Freeze.

We expect that the requested exceptions have already been prepared.

When the release manager group approves the exception, the bug keyword is changed to **APPROVED**, otherwise the bug report remains in **EXCEPTION** keyword state and wait for the nxt new Pardus release.

Feature Freeze Exceptions for new upstream versions
---------------------------------------------------

If you want to update a package to a new upstream version with new features or ABI/API changes:

#. File or triage the bug as explained at `Exception Process`_
#. Attach diff of upstream **ChangeLog** and **NEWS** if you think is needed
#. Mention what testing is needed in order to show that it works
#. Depend all related bugs to exception bug

Feature Freeze Exceptions for new packages
-------------------------------------------

Additions of new packages for the new Pardus release up until Feature Freeze time at milestone `Alpha 3`_ stage. You should follow `new package process`_ before asking for an exception.

#. Follow `new package process`_
#. File or triage the bug as explained at `Exception Process`_

User Interface and String Freeze Exceptions
-------------------------------------------

User interface and string freezes are important to stabilize documentation and translations, so these exceptions should be approved also by translation and documentation groups. The bug report should include the reason why it is needed at that point and cause documentation and translation changes.

#. File or triage the bug as explained at `Exception Process`_
#. Add cc of `translation mail list`_ and documentation mail list.

Milestone Freeze Exceptions
---------------------------

Beta, RC, final etc. freezes are the milestone freezes. The milestone and final freeze times are critically important dates, therefore act prudently while considering exceptions.

Such below things can cause a milestone freeze exception:

#. Insufficient tests
#. A regression or high severity `tracker bug`_ that have a strong rationale and minimal risk for the release

The exception request will be sent to release group list and after it is approved it should be announced on developer, gelistirici and announce list.

.. release grup mail listesi açılmalı
.. documentation mail list and group açılmalı

.. _Alpha 3: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html#alpha-3
.. _new package process: http://developer.pardus.org.tr/guides/newfeature/new_package_requests.html
.. _translation mail list: http://lists.pardus.org.tr/mailman/listinfo/pardus-translators
.. _tracker bug: http://developer.pardus.org.tr/guides/bugtracking/tracker_bug_process.html
.. _announce: http://lists.pardus.org.tr/mailman/listinfo/pardus-announce
.. _developer: http://lists.pardus.org.tr/mailman/listinfo/pardus-devel
.. _gelistirici: http://lists.pardus.org.tr/mailman/listinfo/gelistirici
