.. _contributor availability:

Contributor Availability
========================

**Last Modified Date:** |today|

:Author: Semen Cirit

:Version: template


Life changes, also your availability may change. Therefore Pardus use
different status for contributor availability. These are active, away
or retired.

Active
------

If a contributor, fulfills the `responsibilities of a contributor`_, the status
will be active.

Your contributor bug has a keyword **ACTIVE**.

Away
----

We respectfully request that if you know you will be unavailable for an
extended period of time (vacation, big project at work, family needs, etc),
you should acquaint the other contributors on related group `mail lists`_.

You have to change also your status as away and contributor bug keyword as
**AWAY**.

If you are a developer and have packages, you should orphan_ your
packages that you could not maintain during this period. You may also get
assistant to to retire_ your packages from related `component supervisor`_

When ever your status is away your package can be updated and bugs can be
fixed by an other package maintainer.

When you return, you can take back your packages with assistance of related
component supervisors. You can use devel_ or gelistirici_ mail list for it.

Retired
-------

If a contributor wants no longer contribute to Pardus projects, he can get
retired. He applies the similar things with the away_ status process in order
to warn the other contributors and leave packages.

Absence and inactivity of a contributor can result also as retire. But before
starting this process, first try to communicate with the related team leader
and component supervisor where the contributor was active, if the contributor
looks inactive. He might be active in ways we can't determine easily.

When a contributor is retired, the contributor bug keyword will be **RETIRED**.

Steps to retire a contributor
-----------------------------

Team Leader or Component Supervisor Part
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Check communication activities on mail lists and irc-channels. Mail list
   activities can be controlled via mail list archive threads on last months.
#. If s/he contributes as a developer, check the svn and bugzilla activity:
    #. In  order to check the developer's SVN activity run the below command::

        svn log | sed -n '/<username>/,/-----$/ p'

    #. The bugzilla activity as a commenter can be controlled with `graph
       reports`_, with changing below fields:

        #. On graph choose vertical axis as "status"
        #. Choose NEW, ASSIGNED, REOPENED, RESOLVED for status part
        #. Give a time interval, while the developer seems inactive
        #. Give developer mail address on email addresses part and choose
           commenter as the user part
    #. The assigned bug number for each developer can be found from here_. The
       time interval can also be given for that graph, in order to do it:

        #. Enter `graph reports`_ link.
        #. On graph choose vertical axis as "status", more than one picture as
           "assignee"
        #. Give a time interval, while the developer seems inactive
    #. Bugzilla activity can be controlled also via `bugzilla activity page`_.
#. If the contributor seems inactive during a considerable amount of time, the
   related `component supervisor`_ or `team leader`_ put some effort to contact
   the contributor, before starting the actual retirement process. When sending
   an email to the contributor, make sure that he might get retired due to being
   inactive.

Contributor Availability Coordinator Part
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

#. Send him the first mail and wait a minimum of two weeks, to give the
   contributor adequate time to respond to the mail. If you get no response during
   that period, send the second mail.

    First mail::

        Subject: Possible retirement of contributor <contributor name>

        Dear <contributor name>,

        Possible retirement pending as you haven't shown any activity in the past two
        (or more) months.

         - Last (viewable) bugzilla activity link.
         - Last SVN activity report.

        If you are just away, then please follow process [1].

        Please reply and inform about your situation. Any contributor seems to be inactive
        for a period of approximately 60 days, is subject to be retired. Please be aware that
        if we could not take feedback about you within 2 weeks, we will begin the retirement process.
        If we do retire you, it's pretty easy to come back when you are ready. Just do
        the [2] new contributor process again and you're back on.

        [1] http://developer.pardus.org.tr/guides/newcontributor/contributor_availability#away
        [2] http://developer.pardus.org.tr/guides/newcontributor/how-to-be-contributor.html

    Second mail::

        Subject: Second notice: Possible retirement of <contributor name>

        Dear <contributor name>,

        Possible retirement pending as you haven't shown any activity in the past two
        (or more) months.

         - Last (viewable) bugzilla activity link.
         - Last SVN activity report.

        If you are just away, then please follow process [1]. Any contributor seems to be
        inactive for a period of approximately 60 days, is subject to be retired.

        We're supposed to help Pardus, not to retire as many contributors as possible,
        but in order to able to make the maintenance of our contributor pool, we need to
        include the retirement of inactive contributors and revoking their access privileges.

        We do understand that life brings us unexpected changes and you simply may not have
        the time, resources, etc to contribute on a more frequent basis, every month or two
        is the preferred minimum. If we do retire you, it's pretty easy to come back when
        you are ready.  Just do the [2] new contributor process again and you're back on.
        You also always have the option of contributing as your schedule allows via bugzilla.

        Please reply and inform about your situation. Please be aware that if we have not heard
        from you within 2 weeks time, we will begin the retirement process.

        [1] http://developer.pardus.org.tr/guides/newcontributor/contributor_availability#away
        [2] http://developer.pardus.org.tr/guides/newcontributor/how-to-be-contributor.html

#. Consider any responses carefully. We're supposed to help Pardus, not to
   retire as many contributors as possible.
#. If the contributor doesn't respond in the given time or is otherwise still
   considered inactive, contributor availability coordinators start the process:

   #. Remove access to mail list that the contributor has an account (access is
      either removed completely or changed to voice depending on whether they ask for
      it or they're still considered active and helpful in the channel).

   If s/he contributes as a developer:

   #. Run takeover_ script in order to get orphan the package(s) of retired
      developer.

      Write the below settings for orphaning the package::

        NAME="Pardus"
        MAIL="admins@pardus.org.tr"

   #. If the retired developer is also a component supervisor, the developer
      name and mail address should be changed with Pardus
      and admins@pardus.org.tr respectively on component.xml file.
   #. Change the contributor status as retired on contributor bug as adding
        keyword "RETIRED".
   #. Search for all NEW and REOPEN bugs assigned to the retired contributor on
      Pardus Bugzilla and reassign them to Pardus, admins@pardus.org.tr.

.. _responsibilities of a contributor: http://developer.pardus.org.tr/guides/newcontributor/new-contributor-guide.html#responsibilities-of-a-contributor
.. _mail lists: http://developer.pardus.org.tr/guides/communication/mailing_lists.html
.. _orphan: http://developer.pardus.org.tr/guides/packaging/orphan_packages.html#orphaning-process
.. _retire: http://developer.pardus.org.tr/guides/packaging/orphan_packages.html#retiring-process
.. _away: http://developer.pardus.org.tr/guides/newcontributor/contributor_availability#away
.. _graph reports: http://bugs.pardus.org.tr/query.cgi?format=report-graph
.. _here: http://bugs.pardus.org.tr/report.cgi?y_axis_field=bug_status&cumulate=0&z_axis_field=assigned_to&format=bar&x_axis_field=&query_format=report-graph&short_desc_type=allwordssubstr&short_desc=&longdesc_type=allwordssubstr&longdesc=&bug_file_loc_type=allwordssubstr&bug_file_loc=&keywords_type=allwords&keywords=&deadlinefrom=&deadlineto=&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&emailassigned_to1=1&emailtype1=substring&email1=&emaillongdesc2=1&emailtype2=substring&email2=&bugidtype=include&bug_id=&chfieldfrom=&chfieldto=Now&chfieldvalue=&action=wrap&field0-0-0=noop&type0-0-0=noop&value0-0-0=
.. _component supervisor: http://developer.pardus.org.tr/guides/newcontributor/developer_roles.html#component-supervisor
.. _gelistirici: http://lists.pardus.org.tr/mailman/listinfo/gelistirici
.. _devel: http://lists.pardus.org.tr/mailman/listinfo/devel
.. _takeover: http://svn.pardus.org.tr/uludag/trunk/scripts/takeover
.. _bugzilla activity page: http://developer.pardus.org.tr/events/recent_events/bug_analysis/index.html
.. _team leader: http://developer.pardus.org.tr/guides/newcontributor/developer_roles.html#team-leaders
