.. _package-update-tests:

Package Update Tests
====================

:Author: Semen Cirit
:Last Modified Date: |today|
:Version: 0.1


After the shippment of `final release`_ developers continue to add new packages
and update their packages on `devel source repository`_ during maintanence phase.

When these packages get their stable versions the developers merge them to
`testing source repository`_.

The `binary repositories`_ of these two repositories are generated automatically
by related buildfarms_.

The release manager compare these two binary repositories with `waiting packages for
approval script`_ regularly (twice a month generally) and send a warning mail to
start developer package approval.

After that the package update test process starts; test supervisor make some
`mandatory operations`_ at the beginning of test process, send the needed information
to testers and the package update tests starts.

These tests includes regular tests for newly added and updated packages to `testing
binary repository`_. 

Prepare Tester Machine
----------------------

* You can reserve a min 8Gb special partition for tests. And at the beginning of each
  regular package update test, you should re-install this system (Because the test
  environment must be proper.)

.. Yalı installation guide ekle

* After installation you must update the system. (The repository must be stable repository)
* Add the `tester repository`_ to the system.
    Change repository via  `Package Manager`_: Follow Settings -> Package Manager Settings
    -> Repositories and add the new repository, remove or disable the old repository (stable)
    Change repository via console::

        pisi lr
        pisi dr <old repository name>
            or
        pisi rr <old repository name>
        pisi ar <new repository name> <new repository>

* Re-update the system with tester repository

Start Package Update Tests
--------------------------

* Test supervisor sends a warning mail to start tests and gives relevant information
  (approved package list, tester repository name, tescase link etc.)
* For all packages:
    #. Install packages successively (If the package is already installed during update, the package manager will not list this package or the package install command will return package already installed warning)
        ::

            pisi it <package name>
    #. Apply testcase of the installed package. (The testcases are groupped by `package components`_. The warning mail includes the package list as components, therefore the testers can directly find the relevant testcase document. For example for the testcase of apache package, the server testcases document must be used)
    #. Report errors: After applying the testcases or using the package, if the tester experience with an error, this error must be repoted to bugzilla.
        But, before you file a new bug report you should be sure that the bug that you find:

        * Does not have a duplicate See: `Finding duplicates`_
        * Is suitable for `effective bug reporting document`_?
    #. Take system back: After installing a package and applying its testcase, the system should be taken back in order to install and test the next package on the approved package list. (If the package is directly installed with update, system will not taken back)
        * List the package changes::

            pisi hs

          Example output::

            Operation #51: install
            Date: 2011-01-26 10:39

                * mkinitramfs is upgraded from 1.0.3-88-p11-x86_64 to 1.0.5-91-p11-x86_64.
                * mudur is upgraded from 4.1.3-124-p11-x86_64 to 4.1.3-125-p11-x86_64.
                * baselayout is upgraded from 3.5.1-162-p11-x86_64 to 3.5.1-163-p11-x86_64.


            Operation #50: upgrade
            Date: 2011-01-18 08:25

                * baselayout is upgraded from 3.5.1-159-p11-x86_64 to 3.5.1-162-p11-x86_64.
                * sqlite is upgraded from 3.7.1-28-p11-x86_64 to 3.7.4-29-p11-x86_64.
                * grub is upgraded from 0.97-93-p11-x86_64 to 0.97-94-p11-x86_64.
                * cursor-theme-oxygen-black is upgraded from 4.5.5-144-p11-x86_64 to 4.5.5-150-p11-x86_64.

        * Take the relevant operation back: Control the last operation that you have done with the above command, then take the system back with below command (the given number to the command is the one previous operation number of your change operation number).
            ::

                sudo pisi hs -t <number of one previous operaiton>
    #. After all package tests are finished, send a report as a reply of the warning mail to `tester mail list`_.
        Example report::

            OK·
            ---------------------------
            AstroMenace-1.2_080519-8-p11-i686.pisi
            AstroMenace-data-1.2_070928-2-p11-i686.pisi
            BackupPC-3.2.0-1-p11-i686.pisi
            Bitstream-Vera-fonts-1.10-4-p11-i686.pisi

            Not OK
            ------------------------------
            ETL-0.04.13-4-p11-i686.pisi
            FreeImage-3.13.1-6-p11-i686.pisi
            FreeImage-devel-3.13.1-6-p11-i686.pisi
            FreeMat-4.0.1-3-p11-i686.pisi
            FusionSound-0.0_20080311-8-p11-i686.pisi
            FusionSound-devel-0.0_20080311-8-p11-i686.pisi


.. _final release: http://developer.pardus.org.tr/guides/releasing/official_releases/final_release.html
.. _devel source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#devel-folder
.. _testing source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#testing-folder
.. _waiting packages for approval script: http://svn.pardus.org.tr/uludag/trunk/scripts/find-waiting-packages-for-ack
.. _binary repositories: http://developer.pardus.org.tr/guides/releasing/repository_concepts/software_repository.html
.. _buildfarms: http://developer.pardus.org.tr/guides/releasing/preparing_buildfarm.html
.. _mandatory operations: http://developer.pardus.org.tr/guides/releasing/testing_process/package_update_tests/prepare_test_environment_for_package_updates.html
.. _testing binary repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/software_repository.html#testing-binary-repository
.. _tester repository: http://developer.pardus.org.tr/guides/releasing/testing_process/package_update_tests/prepare_test_environment_for_package_updates.html#create-tester-repository-and-upload-repository-to-server
.. _Package Manager: http://developer.pardus.org.tr/projects/package-manager/index.html
.. _package components: http://developer.pardus.org.tr/guides/packaging/package_components.html
.. _Finding duplicates: http://developer.pardus.org.tr/guides/bugtracking/finding_duplicates.html
.. _effective bug reporting document: http://developer.pardus.org.tr/guides/bugtracking/bug_and_feature_requests.html
.. _tester mail list: http://lists.pardus.org.tr/mailman/listinfo/testci
