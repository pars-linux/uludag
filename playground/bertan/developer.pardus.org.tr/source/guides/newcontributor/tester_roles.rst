.. _tester-roles:

What kind of works a tester interested in?
==========================================

:Author: Semen Cirit
:Last Modification Date: |today|
:Version: 0.1

This page explains all activities you can get involved in to help with Pardus
tests. You can easily get involved_ and choose one or more activities related
to Pardus tests below.

While you are testing for stable release package updates or development release,
push all the buttons, use all the command line options, verify all the
documentation, review it for usability, and suggest future features.
This is especially useful for software which has undergone major changes lately.

Reporting and Triaging bugs
---------------------------

You can involve directly in Pardus tests, just by reporting problems to `Pardus Bugzilla`_.
You only need to have a `bugzilla account`_.

You can also start to bug triage by following `bugzilla mail list`_ and tracking
bugs to find their correct component, severity and request additional information
in order to help developers.

`Reporting and triaging bugs`_ is a big contribution for Pardus.

Joining Package Update Tests
-----------------------------

Pardus Test team has two different maintenance test process. One of them is regular
`package update tests`_ and the other is `security vulnerability update tests`_ for
official final Pardus releases.

In these tests the listed packages on `test mail list`_ by test supervisor are
tested via their testcases_. See `Pardus Package testcases`_.

The maintenance tests can only be done by approved testers, you can be a
an approved tester by `applying for a new contributor`_.

Testing Shipping Release
------------------------

Before each Pardus release shipped, an acceptance test should be done by Pardus
Test Team. In this acceptance tests the testers should be sure the release blocker
bugs are closed and the openned issues are fixed for the related Pardus release.


Desktop and installation validation tests should also be done.

See: `Shipping release test process`_

.. desktop ve installation validation belgeleri yazılacak


Testing Pardus Nightly Releases
-------------------------------

Before an official Pardus release comes out, `nightly releases`_ are automatically
generated in order to tests the changes in repositories frequently. You can
contribute by installing these nigtly releases and testing them.

You can also keep a nightly release and install updates regularly,
and so can help test the release as it is developed.

Report any issues you find to `Pardus Bugzilla`_, following the instructions at
`bug requests`_.

See: `Development release test process`_

Creating Testcases
-------------------

In order to  simply keep a look out for problems, Pardus test team develops
structured testcases_ for packages. The experienced testers can also help 
creating testcases.

Developing Scripts and Tools
----------------------------

We also have some tools or scripts in order to make testing more efficient.
The tools and scripts that already developed are generally used for package
update acceptence. These are `create repository for test team`_, `dependency checker`_,
`linker checker`_, `broken link finder`_, `find packages from same source`_,
`find newly added packages`_. 


Tools currently under development are `package acceptence test tool`_,
`bug reporting tool`_.

.. scirptleri açıklayan sayfayı hazırla

.. _involved: http://developer.pardus.org.tr/guides/newcontributor/how-to-be-contributor.html
.. _applying for a new contributor: http://developer.pardus.org.tr/guides/newcontributor/how-to-be-contributor.html
.. _Pardus Bugzilla: http://bugs.pardus.oarg.tr/
.. _bugzilla account: http://bugs.pardus.org.tr/createaccount.cgi
.. _Reporting and triaging bugs: http://developer.pardus.org.tr/guides/bugtracking/index.html
.. _bugzilla mail list: http://liste.pardus.org.tr/mailman/listinfo/bugzilla
.. _testcases: http://en.wikipedia.org/wiki/Test_case
.. _test mail list: http://liste.pardus.org.tr/mailman/listinfo/testci
.. _Pardus package testcases: http://cekirdek.pardus.org.tr/~semen/testcases/turkish/
.. _nightly releases: http://ftp.pardus.org.tr/pub/pardus/nightly/
.. _bug requests: http://developer.pardus.org.tr/guides/bugtracking/bug_and_feature_requests.html
.. _create repository for test team: http://svn.pardus.org.tr/uludag/trunk/scripts/create-repo-for-test-team
.. _dependency checker: http://svn.pardus.org.tr/uludag/trunk/scripts/dep-checker
.. _linker  checker: http://svn.pardus.org.tr/uludag/trunk/scripts/checkelf
.. _broken link finder: http://svn.pardus.org.tr/uludag/trunk/scripts/find-broken-links
.. _find packages from same source: http://svn.pardus.org.tr/uludag/trunk/scripts/find-packages-from-same-source
.. _find updated packages: http://svn.pardus.org.tr/uludag/trunk/scripts/find-updated-packages
.. _find newly added packages: http://svn.pardus.org.tr/uludag/trunk/scripts/find-newly-added-packages
.. _group packages for their components: http://svn.pardus.org.tr/uludag/trunk/scripts/group-ack-list-as-components.py
.. _package acceptence test tool: http://svn.pardus.org.tr/uludag/trunk/playground/gsoc/testing-framework
.. _bug reporting tool: http://svn.pardus.org.tr/uludag/trunk/playground/gsoc/bug-reporting-tool/
.. _Shipping release test process: http://developer.pardus.org.tr/guides/releasing/testing_process/shipping_release_test_process.html
.. _Development release test process: http://developer.pardus.org.tr/guides/releasing/testing_process/development_release_test_process.html
.. _package update tests: http://developer.pardus.org.tr/guides/releasing/testing_process/package_update_tests/package_update_tests.html
.. _security vulnerability update tests: http://developer.pardus.org.tr/guides/releasing/testing_process/package_update_tests/security_tests.html
