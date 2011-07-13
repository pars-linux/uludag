Git Workflow
============

Basic principles
----------------

*Master is always ready to release*

The master branch is the central branch of completed features and improvements.
It is the origin for development branches as well as release branches. Code in
master is supposed to be done, tested, and ready for being branched for a
release. In theory a distribution should be able to take a snapshot of master,
go through their QA procedures, and then give stable packages to end users.

All non-trivial commits should be first done in feature branches, being tested
and reviewed, and only then merged to master, when they are done and stable.

Master is never frozen for new features or string changes. These freezes happen
in release branches.

*Development happens in feature branches*

Development of features and bug fixes, which require a significant amount of
code changes, happens in feature branches. These branches are branched off
master. Developers are free to handle these branches according to their own
needs, but when they are merged into master they need to be done, tested and
reviewed.

*Feature branches are tested and reviewed before being merged to master*

When feature branches are merged into master, they need to be done, tested, and
reviewed. The level of review depends on the policies of the module, and the
significance of the change. Libraries will have stricter policies than leaf
modules, central applications with a larger developer base will have stricter
policies than smaller applications maintained by single persons.

Ideally broad testing of feature branches happens before being merged to
master, including testing by developers who haven't worked on the changes. To
facilitate this testing the use of integration branches is recommended, which
collect changes from feature branches and make them available to a wider
audience.

*Integration branches are used for wider testing of feature branches*

To make the development happening in individual feature branches available to a
wider audience, the use of integration branches is recommended. Integration
branches are maintained by individuals or groups of maintainers. They collect
changes from feature branches, which are ready for review by fellow developers
and which are done to a state where they are considered to be ready by the
developer.

Integration branches are supposed to be usable for people who want to use or
look at the latest state of development and are willing to report or fix bugs.
ntegration branches should not contain changes known to be broken. These
branches are made visible and accessible to a developer audience beyond the
people working on the actual features.

Integration branches are not merged into master. Rather, the branches that were
merged into these integration branches are merged directly into master after
going through any integration and testing.

*Release branches*

Release branches are branched off master for doing releases. The branch is made
when the release goes into feature and string freeze. No feature development
and no string changes are done in release branches. They are there for final
stabilization and QA of a release and generating release tarballs. The release
branch is tagged with the version number, when creating a release tarball.

Fixes going into the release branches are done in the release branch and then
merged to master, so master keeps getting all fixes made in release branches,
which apply to master.

*Local branches are always rebased, remote branches never*

When developing in a local branch, changes should always be rebased before
pushing them to the remote origin. This keeps a simple linear history. Rebasing
can be thought of as applying changes as patches to the latest version of the
code. In case of conflicts they need to be adapted. So developers always patch
against the latest version of the code.

Remote branches are shared by multiple people. Rebasing them causes different
people to have different versions of history, which causes conflicts,
inconsistent and hard to understand states. So remote branches should never be
rebased. Merging them properly also reflects that development actually happened
in a side line.

Social Workflow
---------------

After a developer completed the issue that assinged to him/herself, he/she
uploads the patch into the issue tracking system. Supervisor of project and
developers that have right to review, investigate the codes. If they accept the
solution, *the project leader* applies the patch.

The contributor that wants to develop a git project, may take on an issue. For
using efficient time and labor, he or she should send an e-mail to mail list
that planning to create for each project to inform project members. After the
contributor completed an issue, he/she should start the review process with
either issue tracking system or dedicated mail list. If the solutions is
approved, *the project leader* includes the patch into project.

The contributor wants to add new feature that is not stated on issue tracking
system. In fact, he or she claims hir or her desire should be a project
requirement. The demant is discussed on project mail list. If project leader
agreed to do this demand, new issue would be create on tracker.pardus.org.tr
and assigne to concerned person.
