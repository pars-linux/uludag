.. _feature-freeze:

Feature Freeze
==============

Features can be requested for

#. Pardus related technologies. See `feature request and tracking`_
#. Packages

Once the feature freeze time is reached, all new features for the release should
be complete and ready for testing.

New features are completed by feature freeze and tested during the test releases
Alpha_ and Beta_ of Pardus.

Expectations of Feature Freeze
------------------------------

Pardus has some expectations after feature freeze about what will be happening
with your feature. These expectations are valuable for testing the feature, test
how other pieces of the distribution interact with your feature, and test the
overall stability and design of the distribution.

After feature freeze some needed expectations:

#. Should implement something testable
#. Should have the the feature significantly complete
#. Should submit the fixed bugs with `version control system commit hooks`_
#. Can not continue to add new enhancements
#. Can not make the feature default if it is not already default before freeze
#. Can not make changes that require other softwares to change.

Code Complete
=============

A release is called code complete when the development team agrees that no entirely new source code will be added to this release. There may still be source code changes to fix major bugs. There may still be changes to documentation and data files, and to the code for test cases or utilities. New code may be added for a future release.

Exceptions
==========

Exceptions have to be approved by the release team for all packages.

They can be approved if the merge:

    * contributes to high severity `tracker bugs`_,
    * is warranted due to other exceptional circumstances, as judged by the release team.

Some cases about features:

    * Upstream microreleases are usually normal after feature freeze if they only fix bugs. The upstream change log and diff between the version in the Pardus development release and the new upstream version should be reviewed and verified that it only fix bugs. In any doubt please ask release managment team.
    * If a library breaks backward compatibility (changes existing API/ABI and introduces a new SONAME), then this always needs approval from the release management group after feature freeze, since all reverse dependencies need to be adjusted and rebuilt. (see `feature freeze exceptions for new upstream versions`_)
    * New packages need `package review`_ before they merge to `devel source repository`_. This process can take several days up to a few weeks. This time should be considered because, the merge date is important for the feature freeze, the new packages should be merged before feature freeze. If they are left after feature freeze they need an exception.

See `freeze exception process`_ for details.

.. _feature request and tracking: http://developer.pardus.org.tr/guides/newfeature/index.html
.. _version control system commit hooks: http://developer.pardus.org.tr/guides/releasing/repository_concepts/version_control_system_rules.html#enter-the-bug-number-when-solving-a-bug-from-the-bug-tracking-system
.. _freeze exception process: http://developer.pardus.org.tr/guides/releases/freezes/freeze_exception_process.html
.. _tracker bugs: http://developer.pardus.org.tr/guides/bugtracking/tracker_bug_process.html
.. _package review: http://developer.pardus.org.tr/guides/packaging/package-review-process.html
.. _devel source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#devel-folder
.. _feature freeze exceptions for new upstream versions: http://developer.pardus.org.tr/guides/releases/freezes/freeze_exception_process.html#feature-freeze-exceptions-for-new-upstream-versions
.. _Alpha: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html
.. _Beta: http://developer.pardus.org.tr/guides/releasing/official_releases/beta_phase.html
