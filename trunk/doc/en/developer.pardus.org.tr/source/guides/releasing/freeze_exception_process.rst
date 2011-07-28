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

Feature Freeze Exceptions for new upstream versions
---------------------------------------------------

If you want to update a package to a new upstream version with new features or ABI/API changes:

#. File or triage the bug as explained at `Exception Process`_
#. Attach diff of upstream **ChangeLog** and **NEWS** if you think is needed
#. Mention what testing is needed in order to show that it works
#. Depend all related bugs to exception bug

We expect that the requested exceptions have already been prepared.

When the release manager group approves the exception, the bug keyword is changed to **APPROVED**, otherwise the bug report remains in **EXCEPTION** keyword state and wait for the nxt new Pardus release.

Feature Freeze Exceptions for new packages
-------------------------------------------

Additions of new packages for the new Pardus release up until Feature Freeze time at milestone `Alpha 3`_ stage. You should follow `new package process`_ before asking for an exception.

#. Follow `new package process`_
#. File or triage the bug as explained at `Exception Process`_

We expect that the requested exceptions have already been prepared.

When the release manager group approves the exception, the bug keyword is changed to **APPROVED**, otherwise the bug report remains in **EXCEPTION** keyword state and wait for the nxt new Pardus release


.. release grup mail listesi açılmalı

.. _Alpha 3: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html#alpha-3
.. _new package process: http://developer.pardus.org.tr/guides/newfeature/new_package_requests.html
