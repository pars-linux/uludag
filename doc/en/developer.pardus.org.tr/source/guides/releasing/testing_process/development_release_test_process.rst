.. _development-test-process:

Development Version Test Process
================================

:Author: Semen Cirit
:Last Modified Date: |today|
:Version: 0.1

Development releases are the current development line of Pardus and contains the
latest build of all Pardus packages updated on a daily basis.

Pardus development releases are live and installable  `nightly builds`_.

Who should use development releases?
------------------------------------

The development releases should not be used by end users as daily workstation.
Because these releases are the test releases of main development branch of Pardus
and many changes are not heavily tested before updates or releases realized, and
packages can break without warning. It is also possible that bugs in development
releases could cause data loss.

Still, testing development releases is a very valuable activity and affect
Pardus development directly and make a far reaching impact to Pardus stable
version.The test results can not only fix the bugs but also can give a new feature
or can increase the usability of an application.

Testing the latest release as soon as it is released is can also be enthusiastic.
Testing development releases is a great way to contribute to Pardus
development. You can install and try it if you have a spare system or use a
virtual machine.

You can also keep a nightly release and install updates regularly, and so can help
test the release as it is developed.

Nightly Releases
----------------

After the bootstrapping_ of the newly release, the nightly builds are started to
create automatically from the `devel branch`_ of the packages. These are built
automatically, therefore they will sometimes be beyond the size of a single CD,
and sometimes may not work at all.

If there is an error occured during the compilation of the packages by buildfarm_,
the images may not be built on a given night; in this case, the last three days
images will remain available.

Testing nightly builds is very valuable to ensure that the quality of the stable
releases is high.

Installing Nightly Releases
---------------------------

Downloading Nightly Releases
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can find nightly releases from here_, this tree includes Live, Installable
and Minimal nightly builds.


Test Nightly Releases Without Disturbing the System
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Test the Live versions from DVD or USB.
    - Burning ISOs
    - Create and use USB
#. Use virtual machine
#. Install to a separate partition.

.. See installation guide

Minimal Nightly Tests
^^^^^^^^^^^^^^^^^^^^^

Minimal nightly builds are very valuable for installation manager (YALI_) tests.
This minimal version is only includes packages those are only needed for YALI_.
Therefore installation time is very short and you can reproduce the bugs more
rapidly.

You can ofcourse also use normal full nightly release in order to test
installation manager (YALI_).

.. See installation guide for YALI_ tests.

Pisi Update from a Nigthly Release
----------------------------------

Keeping a nightly release and updating it regularly and testing it is also
possible. You can list the updated packages after updating the system with
**pisi hs** command. It lists the last package changes on system.

And you can test the updated packages applying the package `test cases`_ to,
relevant updated packages.

Test cases are documented as `component based`_. You can find the component of a
package with **pisi info package-name** command.

Some test cases can be missing, please send an email to `tester list`_ about
this problem.


Upgrade from a Previous Pardus Release
--------------------------------------

If you are a courageous tester, you can try to upgrade your system to a new
release but it is not fully recommended :)

You may run into dependency problems which could take time to resolve. Your
system may get totally into an unusable state.

You can try to upgrade your system by to ways:

#. Using graphical interface: Pardus has an upgrade manager, this application exists in previous release repositories as a pacakge and anyone can install and run this uplication in order to upgrade system to new Pardus release
#. Using command line: If the upgrade manager has not still available you can also try to upgrade your system as a tester.
    First you should disable your ancient repository and add new release repository:
        #. You can make it through package manager following Settings -> Configure Package Manager -> Repositories way
        #. You can make it via console with following commands::

            pisi lr <ancient repo>
            pisi ar <repo name> <new repo>

    Then you can start to update your system, but be carefull because your system
    can totally be unusable.

Testing Nightly Release
-----------------------

Reading `tester list`_ and `buildfarm list`_ and `reporting bugs`_ are the most
important things that all testers should do. All latest changes and compile
problems about package repositories are mailed to `buildfarm list`_, daily reading
of this list is key to staying on top of nightly builds. Discussion of changes
and problems are occured on `tester list`_ and `developer list`_, daily reading
of these lists are also very important.

You can also see the changes on nightly builds from changes files of `nightly
builds`_.

After experiencing with an error, you should report them to bugzilla_. You can
use the assistance of `reporting bugs`_ document. Bugs reported on mail lists or
IRC is not enough, because finding them in history is very difficult, please do
not forget to file bugs to bugzilla_, bugs always be accessible to other testers
and to the developers.

Furthermore the below advices are very useful testing nightly releases:

#. While you are testing, you can learn more about your system, be familiar with bugs in subsystems or package. Testing is an opportunity to learn subsytem and package functioning and be accustomed with their documentations. The documentation can also have bugs, testing system according to documentation give you a chance to detect badly worded and out dated documentation. Reading documentation and learning how things work give you a valuable experience while participating in development process.
#. Be accustomed with log files under /var/log/ path
#. Take notes about the changes that you make on your system. This notes will be valuable when you experience with a problem, you can try to reproduce it in a more effective way.
#. Do not remove at least one old kernel that works
#. Update and reboot daily your system. It is difficult to track the startup bugs caused by and old update, daily update and reboot avoid this.
#. Be accustomed with `grub errors`_ and useful `grub usage`_ for troubleshooting boot up errors.
#. Do not use **--ignore-dependency**, **--ignore-file-conflict** or  **--ignore-package-conflicts** in order to work around dependency problems, file or package conflicts. Please do not report it immediately, because development tree can change very rapidly and these type of errors can be fixed by some developers in one or two days. If you see this error for several days, please report these problems to bugzilla_ or `tester list`_ unless you see a disscussion on `tester list`_, `developer list`_  or a message on `buildfarm list`_ about it.

Report Bugs
-----------

The build reports can be followed on `buildfarm list`_ and these reports include
compile start and end warnings, compile errors of each package for each release
and supported architecture. Before updating your system, please control this
list in order to see updated or newly added packages and their problems.

If you experince with a problem that not reported on `buildfarm list`_ about the
last updated packages, please first control the `developer list`_ and `tester
list`_. If there exist a thread about the problem that you experienced, you can
be sure the developers are aware of the problem.

However, if your problem exsits longer than a few days and there is not any
thread on e-mail lists, that means you experienced with a bug that not everyone
is seeing. This is the time to file a bug report as a tester and make an
influance.

But, before you file a new bug report you should be sure that the bug
that you find:

#. Does not have a duplicate See: `Finding duplicates`_
#. Does not be mentioned on e-mail lists
#. Is suitable for `effective bug reporting document`_

.. _here: http://ftp.pardus.org.tr/pub/ISO/Nightly/
.. _nightly builds: http://ftp.pardus.org.tr/pub/ISO/Nightly/
.. _live: http://ftp.pardus.org.tr/pub/ISO/Live/
.. _installable: http://ftp.pardus.org.tr/pub/ISO/Installation/
.. _bootstrapping: http://developer.pardus.org.tr/guides/releasing/bootstrapping.html
.. _devel branch: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#devel-folder
.. _buildfarm: http://developer.pardus.org.tr/guides/releasing/preparing_buildfarm.html
.. _YALI: http://developer.pardus.org.tr/projects/yali/index.html
.. _test cases: http://cekirdek.pardus.org.tr/~semen/testcases/turkish/
.. _tester list: http://liste.pardus.org.tr/mailman/listinfo/testci
.. _buildfarm list: http://liste.pardus.org.tr/mailman/listinfo/buildfarm
.. _component based: http://developer.pardus.org.tr/guides/packaging/package_components.html
.. _upgrade manager: http://developer.pardus.org.tr/projects/upgrade-manager/index.html
.. _developer list: http://liste.pardus.org.tr/mailman/listinfo/developer
.. _reporting bugs: http://developer.pardus.org.tr/guides/bugtracking/bug_and_feature_requests.html
.. _bugzilla: http://bugs.pardus.org.tr
.. _grub usage: http://www.troubleshooters.com/linux/grub/grub.htm
.. _grub errors: http://www.linuxselfhelp.com/gnu/grub/html_chapter/grub_13.html
.. _Finding duplicates: http://developer.pardus.org.tr/guides/bugtracking/finding_duplicates.html
.. _effective bug reporting document:  http://developer.pardus.org.tr/guides/bugtracking/bug_and_feature_requests.html

.. burning isos yaz
.. create usb yaz
.. installation guide yaz

