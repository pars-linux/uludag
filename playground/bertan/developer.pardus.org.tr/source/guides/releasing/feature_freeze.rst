.. _feature-freeze:

Feature Freeze
==============

Features can be requested for

#. Pardus related technologies. See `feature request and tracking`_
#. Packages

Once the feature freeze time is reached, all new features for the release should
be complete and ready for testing.

New features are completed by feature freeze and tested during the test releases
Alpha and Beta of Pardus.


Expectations of Feature Freeze
------------------------------

Pardus has some expectations after feature freeze about what will be happening
with your feature. These expectations are valuable for testing the feature, test
how other pieces of the distribution interact with your feature, and test the
overall stability and design of the distribution.

After feature freeze some needed expectations:

#. Should implement something testable
#. Should have the the feature significantly complete
#. Should submit the fixed bugs with `svn commit hooks`_
#. Can not continue to add new enhancements
#. Can not make the feature default if it is not already default before freeze
#. Can not make changes that require other softwares to change.

.. _feature request and tracking: http://developer.pardus.org.tr/guides/newfeature/index.html
.. _svn commit hooks: http://developer.pardus.org.tr/guides/releasing/repository_concepts/subversion_rules.html#enter-the-bug-number-when-solving-a-bug-from-the-bug-tracking-system
