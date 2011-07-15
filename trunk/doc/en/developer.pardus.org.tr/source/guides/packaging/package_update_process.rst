.. _package-update-process:

Package Update Process
~~~~~~~~~~~~~~~~~~~~~~

Pardus repositories has different policies for each and this document defines
what sort of updates needed for each of these repositories. In general, repositories
devel, testing and stable should go from less conservative to more.


Alpha Phase Updates
===================

Alpha phase updates are done on `devel source repository`_. The `devel source repository`_
is an area where the `open development`_ activity is done. Package updates are build
automatically every day and directly ship to `devel binary repository`_ users.

`Package update tests`_ are not used for this repository.

For devel repo updates,  Maintainers SHOULD:

    * Not to commit packages that breaks the builds
    * Notify maintainers that depend on their package to rebuild when there are abi/api changes that require rebuilds in other packages or offer to do these rebuilds for them.
    * Notify other maintainers when dealing with mass builds of many packages
    * Request for `package review`_ for new packages

Maintainers can merge the newest version of packages as long as they don't cause breakage. The next Pardus release Also will be branched off this repository, therefore it is best to only push development releases to rawhide if you are fairly confident that there will be a stable enough release in time for the next Pardus release, otherwise you may have to back down to an older, stable version after the branching.

Just before branching, we try to stabilize the major versions of software that will be exist in stable release. Major updates can be done, but package breakage should be avoided if possible before branching.

Beta Phase Updates
==================

At the end of the `Alpha Phase`_ first branching is done and testing source_ and binary_ repositories are opened. After this branching Pardus enters a stabilization phase, therefore the package update changes should be more conservative and controllable and tended to stable release.

Package updates are build automatically every day and directly ship to `testing binary repository`_ users.

For testing source_ repo updates, Maintainers MUST:

    * Avoid major version updates and ABI breakage and API changes
    * Avoid new package merges
    * Wait package for a while in `devel source repository`_ before allowing for merge in testing source_ repository

RC Phase Updates
================

Package updates are build automatically every day and directly ship to `testing binary repository`_ users.

At the end of RC phase `stable binary repository`_ is opened. Just before this repository only package conflicts or unresolved package dependencies, installation and high severity bugs must be fixed. After this repository is opened, only high and urgent `tracker bugs`_ should be fixed.


Stable Phase Updates
====================

During planning_, development_ and stabilization_ phases, changes to the distribution primarily affect developers, early adopters and other advanced users, all of them use these pre releases at their own risk. On the other hand, after release is finalized, Pardus intends to wider usage and different range of users.

Many final_ (stable) release users are less experienced with Pardus and Linux, and look forward to a system that is reliable and does not require user intervention. Therefore, the  problems that they experience in their day to day usage, can be extremly destructive and so they expect a high degree of stability. Indeed, each stable phase update should have a valid reason and low risk regressions. Because updates are automatically recommended to a very large number of users. Also for Pardus releases, a major version means a stable set of features and functionality. As a whole result, we should avoid major updates of packages within a stable release. Updates should aim to fix bugs, and not introduce features, particularly when those features would affect the user or developer experience.

While release is moving towards to end of life, the updates should decrease over time, approaching zero near end of life. This necessarily means that stable releases will not closely track the very latest upstream code for all packages. 
After release is finalized, the next new release planning_ starts and new `devel source repository`_ is opened, latest upstream codes can be committed here.


Special Packages Updates
------------------------

Special packages are required to perform the most fundamental actions on a system. Those actions include:

    * desktop base environment
    * graphical network install
    * post-install booting
    * decrypt encrypted filesystems
    * graphics
    * login
    * networking
    * get updates
    * minimal buildroot
    * compose new trees
    * compose live

The security updates are also are included this special package case.

Rebases should be carefully considered with respect to their dependencies. A rebase that required (or provided) a new Python ABI, for example, would almost certainly not be allowed. ABI changes in general are very strongly discouraged, they force larger update sets on users and they make life difficult for third-party packagers. Additionally, updates that convert resources or configuration one way (ie, from older->newer) should be approached with extreme caution as there would be much less chance of backing out an update that did these things. 

Working with upstream is crucial in order to keep pace with stable branch releases or patches for older releases.


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
.. _stabilzation: http://developer.pardus.org.tr/guides/releasing/official_releases/beta_phase.html
.. _final: http://developer.pardus.org.tr/guides/releasing/official_releases/final_phase.html
