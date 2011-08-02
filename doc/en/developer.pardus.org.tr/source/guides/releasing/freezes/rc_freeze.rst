.. _rc-freeze:

Release Candidate Freeze
========================

The `test source repository`_ is freezed until RC is released, in order to stabilize RC for tests and to fix package inconsistencies and critical bugs in an isolated way. After this point release in `translation freeze` and in `kernel freeze`_  status. All exceptions need approval from release management group (see `Freeze Exception Process`_ for details) which is generally only fix image based problems and does not cause a regression.

Image based problems:
    * Package conflicts or unresolved package dependencies
    * Boot and installation bugs
    * Image based high severity `tracker bugs`_


.. _test source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#testing-folder
.. _translation freeze: http://developer.pardus.org.tr/guides/releasing/feezes/translation_freeze.html
.. _kernel freeze: http://developer.pardus.org.tr/guides/releasing/feezes/kernel_freeze.html
.. _Freeze Exception Process: http://developer.pardus.org.tr/guides/releasing/feezes/freeze_exception_process.html
.. _tracker bugs: http://developer.pardus.org.tr/guides/bugtracking/tracker_bug_process.html
