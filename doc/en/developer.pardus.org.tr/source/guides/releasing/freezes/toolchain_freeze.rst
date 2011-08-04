.. _toolchain-freeze:

Toolchain Freeze
================
TEMPLATE: Needs to be evaluated.

The toolchain is freezed at milestone `Beta 2`_  and the building structure of the release is fixed and can not been changed without release management group approval.

Before toolchain freeze below conditions must be considered:

#. ABI changes that require rebuild of entire repository must be done at the early points (At the end of planning_ and at `Alpha 1`_ phase) of new release
#. Automated compiler regression tests should have run for all architechtures and the logs should be as good or better than previous run's logs.
#. No build failures occur after rebuilding of bootloader and kernel for all architectures
#. No boot failures for each of architecture

.. _Beta 2: http://developer.pardus.org.tr/guides/releasing/official_releases/beta_phase.html#beta-2
.. _Alpa 1: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html#alpha-1
.. _planning: http://developer.pardus.org.tr/guides/releasing/official_releases/planning_phase.html

