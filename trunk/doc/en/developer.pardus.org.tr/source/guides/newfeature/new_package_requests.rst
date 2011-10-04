.. _new-package-request:

New Package Requests
====================

The already existed packages are updated to required versions and new packages are added to `devel source repository`_ before `feature freeze`_ time.

For the new packages, please file a bug to Pardus bugzilla `New Package Request`_ component. Please also give information about licence and main page of the package (The requested new packages must meet the `Licensing Criteria`_). Make sure that this package is not requested before, because we want many free software to reach as many people as possible and do not want to have too much duplication of packaging effort.

 .. image:: images/newpackage_bugzilla.png

Creating a new package and merging it to Pardus repositories
------------------------------------------------------------


If you are not yet a contributor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Choose your package from Pardus Bugzilla `New Package Request`_ component (If it is not filed yet, please create a new bug) and write a comment that you want to create the package.
#. Follow `package creation guidelines`_ and create the package and attach it to the bug.
#. Follow `mentoring process`_ steps in order to be merged your package to Pardus repositories.

If you want to a Pardus developer you can follow `new contributor`_ part and start to merge packages to Paruds repositories with yourself :)

If you are a developer
^^^^^^^^^^^^^^^^^^^^^^

#. Choose your package from Pardus Bugzilla `New Package Request`_ component (If it is not filed yet, please create a new bug) and changed the status of the bug to **ASSIGNED**
#. Follow `package creation guidelines`_ and create the package and commit it to `playground/review source repository`_.
#. Start `package review process`_ of your package
#. After the package pass the `package review criteria`_ and merge to `devel source repository`_, please change the New Package Request bug to **RESOLVED/FIXED**.


Deadline for new package merges to new Pardus release
-----------------------------------------------------

Feature freeze at milestone Alpha 3 is the last time for package meges to `devel source repository`_. It is recommended that to get things done a few weeks earlier, because `package review`_ may take some time.
After this time the `exception process`_ is in progress.


New Package Inclusion
---------------------

New packages are accepted to official Pardus repositories under `some circumstances`_. These circumstances are controlled at `package review`_ by related component supervisor and team leader.

.. _Licensing Criteria: http://developer.pardus.org.tr/guides/licensing/index.html
.. _devel source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#devel-folder
.. _feature freeze: http://developer.pardus.org.tr/guides/releasing/freezes/feature_freeze.html
.. _New Package Request: http://bugs.pardus.org.tr/enter_bug.cgi?product=Yeni%20Paket%20%C4%B0ste%C4%9Fi%2F%20New%20Package%20Request
.. _package creation guidelines: http://developer.pardus.org.tr/guides/packaging/howto_create_pisi_packages.html
.. _technique list: http://liste.pardus.org.tr/mailman/listinfo/teknik
.. _package review process: http://developer.pardus.org.tr/guides/packaging/package-review-process.html
.. _new contributor: http://developer.pardus.org.tr/guides/newcontributor/index.html
.. _playground/review source repository: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#review-folder
.. _Alpha 3: http://developer.pardus.org.tr/guides/releasing/official_releases/alpha_phase.html#alpha-3
.. _mentoring pprocess: http://developer.pardus.org.tr/guides/newcontributor/mentoring-process.html
.. _exception process: http://developer.pardus.org.tr/guides/releasing/freezes/freeze_exception_process.html#feature-freeze-exceptions-for-new-packages
.. _package review: http://developer.pardus.org.tr/guides/packaging/package-review-process.html
.. _package review criteria: http://developer.pardus.org.tr/guides/packaging/reviewing_guidelines.html
.. _some circumstances: http://developer.pardus.org.tr/guides/packaging/package-review-process.html#aim-of-review
.. _mentoring process: http://developer.pardus.org.tr/guides/newcontributor/mentoring_process.html
