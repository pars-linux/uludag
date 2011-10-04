.. _package-update-process:

Package Update Process
~~~~~~~~~~~~~~~~~~~~~~

Pardus repositories has different policies for each and this document defines
what sort of updates needed for each of these repositories. In general, repositories
devel, testing and stable go from less conservative to more.

 .. image:: images/package-updates.png

Alpha Phase Updates
===================

Alpha phase updates are done on `devel source repository`_. The `devel source repository`_
is an area where the `open development`_ activity is done. Package updates are
build automatically every day and directly ship to `devel binary repository`_ users.

For devel repo updates,  Maintainers SHOULD:

    * Not to commit packages that breaks the builds
    * Notify maintainers that depend on their package to rebuild when there are abi/api changes that require rebuilds in other packages or offer to do these rebuilds for them.
    * Notify other maintainers when dealing with mass builds of many packages
    * Request for `package review`_ for new packages

Maintainers can merge the newest version of packages as long as they don't cause breakage. The next Pardus release also will be branched off this repository, therefore it is best to only push development releases to devel if you are fairly confident that there will be a stable enough release in time for the next Pardus release, otherwise you may have to back down to an older, stable version before branching.

Just before branching, we try to stabilize the major versions of software that will be exist in final release. Major updates can be done, but package breakage should be avoided if possible before branching.

Beta Phase Updates
==================

At the end of the `Alpha Phase`_ first branching is done and testing source_ and binary_ repositories are opened. After this branching Pardus enters a stabilization phase, therefore the package update changes should be more conservative and controllable and tended to stable release.

Package updates are build automatically every day and directly ship to `testing binary repository`_ users.

For `testing source repository`_ updates, Maintainers MUST:

    * Avoid major version updates and ABI breakage and API changes
    * Avoid new package merges

RC Phase Updates
================

Package updates are build automatically every day and directly ship to `testing binary repository`_ users.

At the end of RC phase `stable binary repository`_ is opened. Just before this release package conflicts or unresolved package dependencies, installation and high severity bugs must be fixed. Until final is released, only high and urgent `tracker bugs`_ should be fixed.



Shipping Phase Update Process
-----------------------------

This update process enloses alpha, beta and rc phases and there are different process for different type of updates.

#. `New package inclusion process`_
#. `New feature inclusion process`_
#. Bug fix inclusion process:

    #. Before `beta freeze time`_ all updates are done on devel and testing source repositories without any approval but a bug report should be exist:
        #. If its a security related bug, it has already been reported on `Security product`_ with the related release is specified.
        #. If bug is already reported, it should be triaged by developer or by other triager following the `bug triage`_ checklist
        #. If not, the developer should report a new bug following the `bug triage`_ checklist
        #. If a developer starts to deal with the bug and to implement, the bug status should be changed to **ASSIGNED**.

    #. Do not forget to reference the bug number and mark the upcoming package release as critical or security in package specification file. See `history comments`_ and `package updates type`_ for further details.

    #. All changes done to the package during the update should be reflected to the relevant bug report using the following special keywords in the SVN commit messages::

        BUG:COMMENT:#123456     # Inserts a comment into the bug report #123456
    #. If you fixed the bug change the bug status as **RESOLVED/FIXED**::

        BUG:FIXED:#123456       # Closes the bug report #123456 as RESOLVED/FIXED
    #. If your package needs an exception, please control Exceptions_ list and follow `exception request`_ process.
    #. If your package has a new package exception request and accepted please also request for `package review`_ for new packages.
    #. The bug fix inclusions needs approval after `beta freeze time`_ and stable phase update process is used.

Stable Phase Updates
====================

During planning_, development_ and stabilization_ phases, changes to the distribution primarily affect developers, early adopters and other advanced users, all of them use these pre releases at their own risk. On the other hand, after release is finalized, Pardus intends to wider usage and different range of users.

Many final_ (stable) release users are less experienced with Pardus and Linux, and look forward to a system that is reliable and does not require user intervention. Therefore, the  problems that they experience in their day to day usage, can be extremly destructive and so they expect a high degree of stability. Indeed, each stable phase update should have a valid reason and low risk regressions. Because updates are automatically recommended to a very large number of users. Also for Pardus releases, a major version means a stable set of features and functionality. As a whole result, we should avoid major updates of packages within a stable release. Updates should aim to fix bugs, and not introduce features, particularly when those features would affect the user or developer experience.

While release is moving towards to end of life, the updates should decrease over time, approaching zero near end of life. This necessarily means that stable releases will not closely track the very latest upstream code for all packages.


For stable phase updates, major version update can probably cause ABI changes and it forces larger package updates on user systems and enforces contributors. Therefore it is discouraged in general. In addition, updates that are difficult to get back (change resources and configuration in one way) should be done carefully. So, working with upstream is crucial in order to keep pace with stable branch releases or patches for older releases.

Special Packages Updates
------------------------

Special packages should enclose and provide the most fundamental actions on a system. Those actions include:

    * desktop base environment
    * filesystems
    * graphics
    * login
    * networking / servers
    * package update base
    * minimal buildroot
    * post-install booting
    * compose live and install image

The security updates are also included this special package case.

In order to merge special packages and updates from  `devel source repository`_ to `testing source repository`_, package maintainers need an `exception request`_ and approval by merge responsible group.


All Other Updates
-----------------

These updates also need an approval by merge resposible group.

Package maintainers MUST:

#. Fix security vulnerability bugs
#. Fix severe regressions from the previous release. This includes packages which are totally unusable, like being uninstallable or crashing on startup.
#. Fix bugs that directly cause a loss of user data
#. Avoid new upstream versions of packages which provide new features, but don't fix critical bugs, a backport should be requested instead.
#. Avoid ABI breakage or API changes if at all possible.
#. Avoid changing the user experience if at all possible.
#. Avoid updates that are trivial or don't affect any Pardus users. 
#. Avoid adding new packages

Package maintainers SHOULD:

- Push only critical bug fixes and security fixes to previous release (n-1).

Exceptions
----------

Software packages will not be updated to their new upstream releases, new packages and features could not be added during maintenance phase, unless the below exceptions are requested to merge responsibles via merge bug report. Merge bug report should include the reason why it is needed and other bugs that it fixes. See `exception process`_ for details.

    The following things would be considered in an exception request:

        If the version update or new package adding:
            #. fixes a security issue that would affect a large number of users.
            #. fixes critical bugs and doesn't change ABI/API and nothing needs to be rebuilt against the new version.
            #. fixes critical bugs that many users are encountering.

    The following things should not be considered in an exception request:

        If the update or new package adding:
            #. converts databases or resources one way to a new format.
            #. requires user intervention for the service to keep working
            #. causes authorization and authentication changes
            #. changes the GUI that end user encounters
            #. fixes bugs that no Pardus user or customers has reported.


Stable Phase Update Process
---------------------------

Update a package on `devel source repository`_:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. For each update a bug report should be exist:
    #. If its a security related bug, it has already been reported on `Security product`_ with the related release is specified.
    #. If bug is already reported, it should be triaged by developer or by other triager following the `bug triage`_ checklist
    #. If not, the developer should report a new bug following the `bug triage`_ checklist
    #. If a developer starts to deal with the bug and to implement, the bug status should be changed to **ASSIGNED**.

#. Security and critical updates should be done in a minimally invasive approach:
    - If a patch is available for the current version, apply it
    - If a patch is not available for the current version, attempt to backport it
    - If it is impossible to backport or the backport is not safe/suitable for the current version, update to the upstream release which fixes the security/critical bug. See `Exceptions`_

#. Do not forget to reference the bug number and mark the upcoming package release as critical or security in package specification file. See `history comments`_ and `package updates type`_ for further details.

#. All changes done to the package during the update should be reflected to the relevant bug report using the following special keywords in the SVN commit messages::

    BUG:COMMENT:#123456     # Inserts a comment into the bug report #123456
#. If you fixed the bug change the bug status as **RESOLVED/FIXED**::

    BUG:FIXED:#123456       # Closes the bug report #123456 as RESOLVED/FIXED
#. If your package needs an exception, please control Exceptions_ list and follow `exception request`_ process.
#. If your package has a new package exception request and accepted please also request for `package review`_ for new packages.

Merging to `testing source repository`_:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following workflow applies when the package maintainer decides to merge the relevant commits into the `testing source repository`_:

#. Give **MERGEREQUEST** keyword and CC merge responsible mail lists to the bug report
#. The merge responsibles review this merge request:
    #. If the merge request is not approved, bug takes the one of the `insoluable bug resolutions`_ or left for next release and status is changed to **RESOLVED/LATER**  by merge responsibles.
    #. If the merge request is approved, the bug marked with **APPROVED** keyword.
        #. The developer merge it to `testing source repository`_ and reflect it as a comment to merge bug report using the following special keyword in the SVN commit messages and give **MERGED** keyword to the bug::

            BUG:KEYWORD:<MERGED>
        #. The merge responsible, build the **MERGED** keyword binary packages on buildfarm.

After binary package building, testing starts:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Packages have security update type are tested on daily basis.
    #. After the package build, the security related bugs take the  **COMPILED** keyword.
    #. The tester group search them daily and start the `security tests`_.
    #. If there is not any problem while testing the related bugs are marked as **VERIFIED/FIXED**
    #. If not, the tester group will reopen the bug, and marks as **REOPENED**
#. Packages have critical update type are listed by merge responsibles once a month:
    #. The tester group start the `package tests`_
    #. If there is not any problem while testing the related bugs are marked as **VERIFIED/FIXED**
    #. If not, the tester group will reopen the bug, and marks as **REOPENED**
#. Technological updates are listed by merge responsibles yearly,
    #. The tester group start the `package tests`_
    #. If there is not any problem while testing the related bugs are marked as **VERIFIED/FIXED**
    #. If not, the tester group will reopen the bug, and marks as **REOPENED**

Testing finish and merging to `stable binary repository`_:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By merge responsibles:

#. After testing finish the VERIFIED/FIXED packages are searched on bugzilla.
#. These packages are taken to stable binary repository.
#. All package bugs that have taken to `stable binary repository`_ are marked as CLOSED/FIXED.

.. _open development: http://developer.pardus.org.tr/guides/releasing/official_releases/release-process.html#open-development
.. _Package update tests: http://developer.pardus.org.tr/guides/releasing/testing_process/package_update_tests/index.html
.. _devel source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#devel-folder
.. _devel binary repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/software_repository.html#devel-binary-repository
.. _Alpha Phase: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html
.. _binary: http://developer.pardus.org.tr/guides/releasing/repository_concepts/software_repository.html#testing-binary-repository
.. _source: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#testing-folder
.. _testing binary repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/software_repository.html#testing-binary-repository
.. _stable binary repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/software_repository.html#stable-binary-repository
.. _tracker bugs:  http://developer.pardus.org.tr/guides/bugtracking/tracker_bug_process.html
.. _package review: http://developer.pardus.org.tr/guides/packaging/package-review-process.html
.. _planning: http://developer.pardus.org.tr/guides/releasing/official_releases/planning_phase.html
.. _development: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html
.. _stabilization: http://developer.pardus.org.tr/guides/releasing/official_releases/beta_phase.html
.. _final: http://developer.pardus.org.tr/guides/releasing/official_releases/final_phase.html
.. _bug triage: http://developer.pardus.org.tr/guides/bugtracking/howto_bug_triage.html#check-list-for-bugs-have-new-status
.. _history comments: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#history-comments
.. _package updates type: http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html#different-pspec-xml-file-tags
.. _testing source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#testing-folder
.. _insoluable bug resolutions: http://developer.pardus.org.tr/guides/bugtracking/bug_cycle.html
.. _security tests: http://developer.pardus.org.tr/guides/releasing/testing_process/package_update_tests/security_tests.html
.. _package tests: http://developer.pardus.org.tr/guides/releasing/testing_process/package_update_tests/package_update_tests.html
.. _exception request: http://developer.pardus.org.tr/guides/releasing/freezes/freeze_exception_process.html
.. _exception process: http://developer.pardus.org.tr/guides/releasing/freezes/freeze_exception_process.html
.. _Security product: http://bugs.pardus.org.tr/enter_bug.cgi?product=G%C3%BCvenlik%20%2F%20Security
.. _Shipping release test process: http://developer.pardus.org.tr/guides/releasing/testing_process/shipping_release_test_process.html
.. _New package inclusion process: http://developer.pardus.org.tr/guides/newfeature/new_package_requests.html#creating-a-new-package-and-merging-it-to-pardus-repositories
.. _New feature inclusion process: http://developer.pardus.org.tr/guides/newfeature/newfeature_requests.html#how-my-new-feature-request-is-accepted?
.. _Bug fix inclusion process: http://developer.pardus.org.tr/guides/packaging/package_update_process.html#update*a-package-on-`devel-source-repository`_:
.. _beta freeze time: http://developer.pardus.org.tr/guides/releasing/freezes/beta_freeze.html
