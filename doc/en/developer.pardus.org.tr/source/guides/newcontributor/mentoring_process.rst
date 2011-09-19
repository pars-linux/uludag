.. _mentoring-process:

Mentoring Process
=================

Mentoring is an assistance to allow `expected developers`_ to have packages reviewed and merged to Pardus repositories. Mentoring process is the time for learning Pardus and a start development for Pardus.

Request for Mentoring
---------------------

The general steps for contributing development and finalize your work:

* File a new bug or follow up on an existing one
* Work on the fix
* Request mentor

Detail steps:

#. File a new bug or follow up on an existing one.  (You can also look `Junior jobs`_ part.)
#. Do not deal with a bug which is already needs mentoring (This bugs has a **NEEDSMENTORING** keyword)
#. Control the current release schedule and find out which work can be integrated at the current point of the release cycle. (The work that you work on may not be merged immediately to repositories related to the release schedule state and may wait for the next release)
    #. The beginning of the release cycle is the best time for intrusive changes
    #. After feature freeze time, you will need a `freeze exceptions`_ for new features and new packages
    #. After the release is finalized, intrusive changes probably can not be merged to stable repositories and your fix may wait for the next new release. (See `Stable Phase Updates`_)
#. Work on the fix:
    #. If it is a new package, attach the package pisi source code as a compressed file.
    #. If it is a bug fix or a new feature request fix please attach as a patch and be sure your patch applies cleanly.
#. When the expected developer is ready for junior job review:
        #. Add **NEEDSMENTORING** keyword
        #. Change the bug status to RESOLVED/FIXED
        #. Send a message to `technical mail list`_
            Mail subject format will be::

               <Applicant Name> - <simple junior job information> pb#<BugID> JUNIORJOB Review

            Example::

                Semen Cirit - mangonel is a simple application launcher for KDE4 pb#17311 JUNIORJOB Review

         #. Add `technical mail list`_ archive link to the junior job bug URL.
#. According to expected developers work difficulty, the `playground svn`_ permissions can be given and review corrections can be tracked on the bug easily.

The commit messages can reflected as a comment to the relevant bug report using the following special keyword in the SVN commit messages:

::

    BUG:COMMENT:<Bug ID>

Mentoring Review
----------------
#. Mentors will triage bugs with **NEEDSMENTORING** keyword weekly, and picks bugs they are interested.
#. Select a bug to review according to your talent
    #. Set the keyword **MENTORED**
    #. Assign the bug to yourself,  change the bug status to **ASSIGNED**
#. The first aim is to welcome to expected developer, so be polite thanks them about the contribution.
#. Start to review bug on mentor `technical mail list`_.
    #. Follow `package review guidelines`_, `freeze exceptions`_ while reviewing
    #. Control that patches should apply and compressed files build and work correctly and built packages should install correctly
#. Let the expected developer know that if the work is not suitable for the current point of the release
    #. Guide expected developer about `freeze exceptions`_ process
    #. If it is not an exception, then set the bug status **RESOLVED/LATER**
#. If you think that the work is ready for Pardus repositories
    #. Change the keyword to **REVIEWED**
    #. If it is a new package, the maintainer of the package is yourself and merge it. (History comments author will be the expected developer.)
    #. If it a patch of a new feature or bug fix, apply the patch to relevant package and merge it.
    #. Hereafter the `Stable Phase Updates`_ process will be applied

.. _freeze exception: http://developer.pardus.org.tr/guides/releasing/official_releases/freezes/freeze_exception_process.html#exception-process
.. _Stable Phase Updates: http://developer.pardus.org.tr/guides/packaging/package_update_process.html#stable-phase-updates
.. _technical mail list: http://liste.pardus.org.tr/mailman/listinfo/teknik
.. _package review guidelines: http://developer.pardus.org.tr/guides/packaging/reviewing_guidelines.html
.. _freeze exceptions: http://developer.pardus.org.tr/guides/releasing/freezes/index.html
.. _playground svn: http://developer.pardus.org.tr/guides/releasing/repository_concepts/sourcecode_repository.html#playground-folder
.. _Junior Jobs: http://bugs.pardus.org.tr/buglist.cgi?keywords=JUNIORJOBS&query_format=advanced&keywords_type=allwords&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED
.. _expecten developers: http://developer.pardus.org.tr/guides/newcontributor/developer_roles.html#expected-developer

