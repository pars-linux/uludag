.. _developer-roles:

**Last Modified Date** 11-08-2011

:Author: Semen Cirit

Pardus Developers
~~~~~~~~~~~~~~~~~

If you trying to find out how to take part in development of Pardus, then you may find below links useful at first step:

* `Contribute to Pardus`_
* `Creating Packages`_
* `Development process`_
* `Being Pardus developer`_

What kind of works a developer interested in?
=============================================

Pardus Linux Distribution developers have an important role in creation of Pardus. They have a direct impact on the software and it meets the needs of users. In order to meet the needs of users and ensure that Pardus absolutely work , they have different roles in the project. A developer has one of these roles or more at the same time. A developer also can take a new role according to his experience.

Everybody can work on any package they want to improve. Pardus value all these contributions. If you do not have permissions for Pardus repositories yet, mentors can review your work and merge it for you. (See `mentoring process`_ for details).


Expected Developer
------------------
#. Gain experience on bug fixing and creating new packages
#. Request mentor review for their works,
    Mentors_ will:

    * Review their works
    * Give constructive feedback
    * Merge the package to related repository if it is ready
(See details in `mentoring process`_)

If you are already a `expected developer`_ and want to be a Pardus developer, please apply to `new contributor process`_.

Package Maintainers
-------------------
#. Maintain the package according to repository and package rules.
#. Control, analyse, resolve and fix the bugs that reported on Bugzilla_
#. Follow and read the technical lists and websites about the maintained package
#. Follow and read the other distributions plans about the maintained package.
#. Be in contact with the upstream of the maintained package.
#. Before merging the package to relavant repositories, make functional and installation tests.
#. Follow the security related bugs from Bugzilla_ and be in contact with Security Supervisor.
#. Help other package maintainers in order to expand their understanding of packaging work.

Component Supervisor
--------------------

* Every component and subcomponent has a component supervisor.
* If a subcomponent has not a supervisor, one up component supervisor is also the supervisor of it.
* The last decision about the component is given by main component supervisor.

Roles
^^^^^
   #. Control the package maintainers under his supervised component:

        The control is concerned with above instructions:

        - Are the updates acceptable for package and repository rules?
        - Is package maintainer dealing with related package bugs?
        - Are the packages merged before given deadline?

        If the package maintainer is not responsive for a long time, supervisor should:

        #. Deal with the unmaintained package. (package update, maintenance, merge, bug fix)
        #. Describe the package maintainer status. (retirement, military duty and other private issues)

   #. Move packages in the component and decide whether the package is suitable with the selected component.

   #. For the orphan packages under his supervised component:

       #. Control orphan packages and list them
       #. Maintain orphan packages for a while
       #. Allow temporarily maintenance of the orphan package for an other maintainer
       #. Find maintainer for orphan package.

   #. Join the new `package review`_ process of the packages under his supervised component.

Software Developer
------------------
#. Take into account the new feature requests and prepare a requirement list in consultation with the lead developer
#. Design the software that will be implement and prepare design documentation.
#. Implement assigned part of the software and prepare their unit tests.
#. Prepare the user guide and technical documentation
#. Control, analyse, resolve and fix the bugs that reported on Bugzilla_
#. Maintain the packages that are required for the software

Lead Developer:
---------------
#. Analyse, manage and plan all the life cycle of the project
#. Take into account the new feature requests and prepare a requirement list in consultation with the related developers.
#. Give timelines of the project in consultation with release manager and product manager.
#. Organize and coordinate the developers under the project.
#. Review bugs related to the project and give related severity and priority levels.


.. _package review: http://developer.pardus.org.tr/guides/packaging/package-review-process.html
.. _Contribute to Pardus: http://developer.pardus.org.tr/guides/newcontributor/areas-to-contribute.html
.. _Creating Packages: http://developer.pardus.org.tr/guides/packaging/index.html
.. _Development process: http://developer.pardus.org.tr/guides/releasing/index.html
.. _Being Pardus developer: http://developer.pardus.org.tr/guides/newcontributor/how-to-be-contributor.html
.. _mentoring process: http://developer.pardus.org.tr/guides/newcontributor/mentoring_process.html
.. _new contributor process: http://developer.pardus.org.tr/guides/newcontributor/how-to-be-contributor.html
.. _Bugzilla: http://bugs.pardus.org.tr
.. _Mentors: http://developer.pardus.org.tr/guides/newcontributor/newcontributor_mentors.html
