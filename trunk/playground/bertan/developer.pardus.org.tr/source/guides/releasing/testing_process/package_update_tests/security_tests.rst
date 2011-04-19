.. _security tests:

Security Vulnerability Update Tests
------------------------------------

:Author: Semen Cirit
:Last Modified Date: |today|
:Version: 0.1


During maintenance phase the security vulnerabilities released packages should
immediately update, test and merge to stable repository.

After the all `mandatory work of security process`_ have done the test supervisor
send the needed information to testers and the security update tests starts. The
due date of the tests are very important, the packages should be tested until
this time.

The tester system must be `prepared as the package update tests`_. But only one
exeption can be existed: sometimes the test supervisor do not need to create
a tester repository and gives the official testing repository as an information
on security test warning mail instead. For this condition, testers will not add
the tester or testing repository to the test system (the stable repository will
remain).

The `package update test steps`_ must also be applied for this test type. But, if
there is not exist a tester repository, the packages should directly install with
their package links::

    sudo pisi it http://packages.pardus.org.tr/pardus/2011/testing/x86_64/Charis-compact-fonts-4.106-2-p11-x86_64.pisi http://packages.pardus.org.tr/pardus/2011/testing/x86_64/Charis-fonts-4.106-7-p11-x86_64.pisi http://packages.pardus.org.tr/pardus/2011/testing/x86_64/QtCurve-Gtk2-1.8.3-29-p11-x86_64.pisi http://packages.pardus.org.tr/pardus/2011/testing/x86_64/QtCurve-KDE4-1.8.2-28-p11-x86_64.pisi 

The listed packages on security test warning mail must installed alltogether like the example above.

.. _mandatory work of security process: http://developer.pardus.org.tr/guides/releasing/security_process.html#how-the-security-update-takes-place
.. _prepared as the package update tests: http://developer.pardus.org.tr/guides/releasing/testing_process/package_update_tests/package_update_tests.html#prepare-tester-machine
.. _package update test steps: http://developer.pardus.org.tr/guides/releasing/testing_process/package_update_tests/package_update_tests.html#start-package-update-tests


