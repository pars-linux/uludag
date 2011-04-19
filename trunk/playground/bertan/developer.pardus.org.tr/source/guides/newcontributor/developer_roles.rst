.. _developer-roles:

What kind of works a developer interested in?
=============================================

Pardus Linux Distribution developers have different roles in the project. A developer has one of these roles or more at the same time. A developer also can take a new role according to his experience.

Package Maintainers
-------------------
#. Maintain the package according to repository and package rules.
#. Control, analyse, resolve and fix the bugs that reported on `Bugzilla <http://bugs.pardus.org.tr>`_
#. Follow and read the technical lists and websites about the maintained package
#. Follow and read the other distributions plans about the maintained package.
#. Be in contact with the upstream of the maintained package.
#. Before merging the package to relavant repositories, make functional and installation tests.
#. Follow the security related bugs from `Bugzilla <http://bugs.pardus.org.tr>`_ and be in contact with Security Supervisor.

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
#. Control, analyse, resolve and fix the bugs that reported on `Bugzilla <http://bugs.pardus.org.tr>`_
#. Maintain the packages that are required for the software

Lead Developer:
---------------
#. Analyse, manage and plan all the life cycle of the project
#. Take into account the new feature requests and prepare a requirement list in consultation with the related developers.
#. Give timelines of the project in consultation with release manager and product manager.
#. Organize and coordinate the developers under the project.
#. Review bugs related to the project and give related severity and priority levels.

**Last Modified Date** |today|

:Author: Semen Cirit

.. _package review: http://developer.pardus.org.tr/guides/packaging/package-review-process.html
