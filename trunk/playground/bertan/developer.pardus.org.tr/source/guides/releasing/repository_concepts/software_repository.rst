.. _software-repository:

Software Repository (binary or package repository)
==================================================

:Author: Semen Cirit
:Date: |today|
:Version: 0.2

A software repository generally means a storage location from which software
packages may be retrieved and installed on a computer. Therefore compiled
Pardus packages are located at software repositories in binary format.

Every Pardus distribution has specific `binary repositories`_.

All of these repositories group packages by `supported architectures`_ and these
repositories are also have debug packages folder.

During alfa, beta versions of Pardus distributions, all these repositories are
the same.

Following table shows binary/farm/source mappings:

+---------------+-----------------+---------------+
| Binary Repo   |  Farm           | Source Repo   |
+===============+=================+===============+
| devel/i686    |  devel/i686     | devel         |
+---------------+-----------------+---------------+
| devel/x86_64  |  devel/x86_86   | devel         |
+---------------+-----------------+---------------+
| testing/i686  |  testing/i686   | testing       |
+---------------+-----------------+---------------+
| testing/x86_64|  testing/x86_64 | testing       |
+---------------+-----------------+---------------+
| stable/i686   |  -              | testing       |
+---------------+-----------------+---------------+
| stable/x86_64 |  -              | testing       |
+---------------+-----------------+---------------+


Devel Binary Repository
-----------------------

The packages under `devel package source repository`_ are compiled and the created
binary pisi packages are located under this repository.

Users that want to use bleeding edge versions of packages, they can use this
repository.

Testing Binary Repository
-------------------------

The packages under `testing package source repository`_ are compiled and the created
binary pisi packages are located under this repository.

Stable Binary Repository
------------------------

The updated and newly added packages under test binary repository enters a test
process. The approved packages after this process are merged to this stable
repository by release manager.

.. _binary repositories: http://packages.pardus.org.tr/pardus/
.. _devel package source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#devel-folder
.. _testing package source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#testing-folder
.. _test binary repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/software_repository.html#test-binary-repository
.. _supported architectures: http://developer.pardus.org.tr/guides/packaging/packaging_guidelines.html#architecture-support
