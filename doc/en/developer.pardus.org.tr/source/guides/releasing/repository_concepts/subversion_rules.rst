.. _subversion-rules:

Rules for a correct Subversion usage
====================================

:Author: Ozan Çağlayan, Semen Cirit
:Date: |today|
:Version: 0.1

Subversion repository is a common place shared by all developers. In order to
work together developers should be using the repository efficiently, properly
and in an organized way.

Rules for using Subversion are the rules to be respected by the developers
having the privilege to write to Pardus repositories.

Always work with an up-to-date local copy
-----------------------------------------

The updates on the Subversion repository will be more frequent as the quantity
of the developers increase. In order to know about the rest of the process and
to avoid a conflict between what you do and the rest to be done, before you begin
to work, always update your repository by means of *svn update* command.

Think before you commit
-----------------------

Think twice before you commit the modifications you made, to the Subversion
repository. The data you commit to the repository will reach to all developers
and affect their work. In this sense, its of great importance to follow the
articles below:

#. Do not commit a non-running code to the Subversion repository,
#. Always update your repository before you commit by means of svn update in order to get the last changes. Be sure that the changes you made do not conflict with the others,
#. Pay attention to what you commit. To make sure of this, always control the changes you are about to commit by means of svn diff command before commitment,
#. Always test the changes you made. Even better, test them twice.

Write descriptive commit log messages
-------------------------------------

Explanation messages used in the commit logs should focus on the modification
and be as descriptive as possible. As much as you can, try to add explanation
messages related with only the files you made changes on. However, in the limits
of the context, you can include all the information which can not be derived
from the output of a *svn diff* command in your explanation message.

Refraining from adding a proper explanation message will make it difficult to
understand the changes you made.

Abide by the work plans
-----------------------

If a work/time plan exists for the distribution in general or if the main
developer of the component you are working on sets such a plan, abide by this
plan regarding your commitments.

For example, an application developer might want to stop adding new features
to the application at a particular time and might want to work on fixing the
known issues. Its expected that the change you make is coherent with this rule.

If you are not sure of the coherency of the change you made with the plan, you
have to refer the related e-mail lists or the main developer.

Changes affecting other components
----------------------------------

If you made a change affecting more than one component, inform all developers
about the change. In order to ensure all developers know about the major update
you made, always send an informative message to the related e-mail list.

Take responsibility for the changes you made
--------------------------------------------

If the update you made is creating a problem, take the responsibility of it
and make sure to solve it yourself or by getting help.

Respect the generally accepted principles
-----------------------------------------

Obey the general rules accepted during developers' discussions and be sure
that your changes are not violating those rules.

Enter the bug number when solving a bug from the bug tracking system
--------------------------------------------------------------------

If the update you make is solving a reported bug, in order to synchronize the
bug tracking system with the updates in the repository, notify the bug you
solved.

If the svn commit message includes the below information your changes on the
source code and your message will be added as a comment to the bug report::

    BUG:COMMENT:<Bug ID>

If the svn commit message includes the below information your changes on the
source code, your message will be added as a comment to the bug report and
the bug status changed as RESOLVED/FIXED::

        BUG:FIXED:<Bug ID>


Update the files for which you are responsible
----------------------------------------------

Update only the files which are in your responsibility. If you find a bug in files
which is in another developer's responsibility, first, discuss the situation
either by directly contacting the responsible developer or by asking the other
developers in e-mail lists and only after doing so make an attemp to update the
repository. If the responsible developer does not accept the changes you made,
behave respectfully.

Do not add the automatically created files to the repository
------------------------------------------------------------

Do not add the files such as Makefile, Makefile.in, configure scripts, etc.
which are created afterwards by compilation tools. These files will be recreated
in different forms in all developers' machines and will be perceived as an update
by the other develepors. In general, adding these files to the repository is
perceived as a bug.

Perform atomic updates
----------------------

Commit all the modifications related to a particular improvement/update at once.
Subversion lets you commit more than one file at a time. Other developers might be
confused because of seperate commits and they can miss the improvements you made.

Resources
---------

* `Commit Messages <http://who-t.blogspot.com/2009/12/on-commit-messages.html>`_

