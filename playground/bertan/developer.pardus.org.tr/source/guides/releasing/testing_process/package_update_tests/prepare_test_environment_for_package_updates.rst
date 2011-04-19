.. _prepare-test-environment-for-package-updates:

Prepare Test Environment for Package Updates
============================================

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

.. geliştirici paket onayını yaz

Create Updated Package List for Stable Release
----------------------------------------------

After the developer package approval, the test supervisor create a list of approved
packages and run the `find packages from same source script`_ and add the missing
packages to the list.


::

    ./find-packages-from-same-source <repo name> <files to search for ....>

Example::

    ./find-packages-from-same-source testing-2011 xulrunner qt

The listed pacakges can be continue to update during testing phase and these
updated packages are found with `find updated pacakges script`_.

::

    ./find-updated-packages <repo name> <files to search for ....>

Example::

    ./find-updated-packages testing-2011 AssaultCube-1.1.0.3-7-p11-i686.pisi  QtCurve-Gtk2-1.6.1-26-p11-i686.pisi

Create Tester Repository and Upload Repository to Server
--------------------------------------------------------

The test supervisor create a special repository for testers. This repository
includes the stable binary repository + approved binary packages by developers.

In order to create this repository and upload it to http://packages.pardus.org.tr
`create repository for test team script`_ is run.

::

    ./create-depo-for-test-team <test team depository directory> <stable rsync address> <test depository directory> <test rsync address> <stable repo dir>

Example::

    ./create-depo-for-test-team testteam-2009 rsync://x/2011-stable pardus-2011-test rsync://x/2011-test /home/x/pardus/2011/stable

Find Missing Dependencies of Approved Packages for Stable Repository
--------------------------------------------------------------------

The tester repository is added to newly installed and updated virtual system.
After updated the system with newly added repository, `find broken links script`_
is run.

This script create a connection between virtual and physical machine and read
package names from the approved package list that exists on physical machine and
install them to virtual machine. It also runs the revdep-rebuild command for each
package and write the broken links to "broken" file.

Example "broken" file::

    google-gadgets needs:
    -------------------------------------------------------
    webkit-gtk

    gst-plugins-bad needs:
    -------------------------------------------------------
    libkate

Run the script:
^^^^^^^^^^^^^^^

The script and the approved package list are copied to the same directory and run
the below command.

::

    find-broken-links

This command require the followings:

#. The below information lists the machines on virtualbox, the relevant machine number will be chosen.
    ::

        1-"2008"
        2-"2009"
        3-"corporate"
        Please choose the machine you want to work with:

#. If the virtual box network mode is not bridge the script gives the below warning and finish it is work. Change it to bridge mode and rerun the script.

    ::

        It seems you still did not configure your Network property into "bridged"  program will exit now

#. The script require the below information successively::

    Please enter the virtual machine user name:
    Please enter the virtual machine name:
    Please enter the virtual machine user Password:
    Please enter the virtual machine root Password:
    Please enter the virtual machine language (tr or en):
    Please enter the real machine user name:

#. The script require the IP address of virtual machine
#. The script also require the new repository address (tester repository)

After all steps the script start to install each package and find broken links successively.

Update Approved Package List
----------------------------

After finding erroneous packages (with dependency problem), test supervisor
remove them from package list and file bug report for each of them with
"ACK test:" summary.

Warn Testers
------------

After updating the package list, the test supervisor `group this list`_ as
`package components`_. Then this list is sent to testers and the package update
tests start.



.. _final release: http://developer.pardus.org.tr/guides/releasing/official_releases/final_release.html
.. _devel source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#devel-folder
.. _testing source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#testing-folder
.. _waiting packages for approval script: http://svn.pardus.org.tr/uludag/trunk/scripts/find-waiting-packages-for-ack
.. _binary repositories: http://developer.pardus.org.tr/guides/releasing/repository_concepts/software_repository.html
.. _buildfarms: http://developer.pardus.org.tr/guides/releasing/preparing_buildfarm.html
.. _find packages from same source script: http://svn.pardus.org.tr/uludag/trunk/scripts/find-packages-from-same-source
.. _find updated pacakges script: http://svn.pardus.org.tr/uludag/trunk/scripts/find-updated-packages
.. _create repository for test team script: http://svn.pardus.org.tr/uludag/trunk/scripts/create-repo-for-test-team
.. _find broken links script: http://svn.pardus.org.tr/uludag/trunk/scripts/find-broken-links
.. _group this list: http://svn.pardus.org.tr/uludag/trunk/scripts/group-ack-list-as-components.py
.. _package components: http://developer.pardus.org.tr/guides/packaging/package_components.html
