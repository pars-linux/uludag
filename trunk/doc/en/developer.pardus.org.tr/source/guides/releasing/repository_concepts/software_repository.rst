.. _software-repository:

Software Repository (binary or package repository)
==================================================

:Author: Semen Cirit
:Date: |today|
:Version: 0.1

A software repository generally means a storage location from which software
packages may be retrieved and installed on a computer. Therefore compiled
Pardus packages are located at software repositories in binary format.

Every Pardus distribution has specific `binary repositories`_.

Devel Binary Repository
-----------------------

The packages under `devel package source repository`_ are compiled and the created
binary pisi packages are located under this repository.

Users that want to use bleeding edge versions of packages, they can use this
repository.

Test Binary Repository
----------------------

The packages under `stable package source repository`_ are compiled and the created
binary pisi packages are located under this repository.

Stable Binary Repository
------------------------

The updated and newly added packages under test binary repository enters a test
process. The approved packages after this process are merged to this stable
repository by release manager.


During alfa, beta versions of Pardus distributions, all these repositories are
the same.

.. _binary repositories: http://packages.pardus.org.tr/pardus/
.. _devel package source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#devel-folder
.. _stable package source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#stable-folder
.. _test binary repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/software_repository.html#test-binary-repository
