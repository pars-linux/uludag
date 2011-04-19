.. _security-team:

Security Process
================

:Author: Eren Türkay, Semen Cirit
:Last Modified Date: |today|
:Version: 0.2

Pardus Security team follow and close the security vulnerabilities of open source
projects which are included in Pardus repositories. While doing this, it works in
a cooperation with other distributions.  A standardized way is used in order to
enable this cooperation to track mail lists like vendor-sec, oss-security and to
catch the security bugs.

This documentation will briefly explain this standardized way and how the
Pardus Security team use it and how it works.

Constructive Notice from Security World
--------------------------------------

In order to understand how Pardus Security team work, there should be known that
the notions of security world, what e-mail lists are used and what are their aims.

Different notions from Security world:

**Vendor**: The person/association/corporation that provides services. Example
for vendors  **Pardus, Redhat, Debian, Ubuntu, HP, Oracle**.

**Upstream**: The person/association/corporation that is head of the development
process. It is similar in open source world, the developer or a group of people
that is head ofa development process.

**Advisory:** This is a manifesto which includes information about the security
vulnerability of a specific software version and also its solution.

`CVE ID`_: (CVEs, CVE names, CVE numbers) This is a specific number assigned for
a security vulnerability. This number is find an acceptance in order to prevent
security vulnerability to be seen in different forms and to cause a disorder and
to enable corporations or people that are interested in security vulnerabilities
to track it.
CVE numbers are assigned like CVE-{YEAR}-{NUMBER}, ex: CVE-2010-4354. CVE numbers
can be assigned by CNA (*CVE Numbering Authority*). The head of this authority is
the MITRE organization but Debian, Ubuntu, FreeBSD can also assign CVE numbers.
You can see all CNAs from `mitre CNA sayfası`_.

`Vendor-sec`_: This is a private e-mail list which consists of members like Linux
distributions and private corporations (IBM, Oracle, Apple). The discussions
about security vulnerabilities and when they will be opened to public, take place
in this e-mail list.

Oss-security_: This is a public discussion list for security vulnerabilities.
The CVS number is requested in this e-mail list for the security vulnerabilities
have already be public.

.. _CVE ID: http://cve.mitre.org/cve/identifiers/index.html
.. _mitre CNA sayfası: http://cve.mitre.org/cve/cna.html
.. _Vendor-sec: http://oss-security.openwall.org/wiki/mailing-lists/vendor-sec
.. _Oss-security: http://oss-security.openwall.org/wiki/about

How the process works?
----------------------

Vulnerabilities from Vendor-sec
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Explaining this process with an example will be more effective and simple:
Assuming that XX project has a security vulnerability.

    #. The information about the vulnerability are send to vendor-sec_ e-mail list. There exists a detailed information about the vulnerability.

    #. The vulnerability is reviewed by MITRE. If it has not already been reported, its CVE number is given by MITRE or an other authority which have a permission to give CVE ID.

    #. After this assignment, the developer of XX project is informed about the vulnerability. This vulnerability is discussed privately on the XX project bugzilla. The patch which closes the vulnerability is send to vendor-sec_ list by the person contacted with related developer.

    #. After the vulnerability closed, the time of the public announce is set. This time is given in order to enable distributions to close and test the bugs. This time is generally 1 week, but if a distribution require more time, it can be extended. The important point in that process, any information can not be spread before the declared public announce time and commit the patches to public svn repositories.

The above items are the process excluding Pardus Security team part. Pardus
Security team is a vendor-sec_ member and obey the vendor-sec_ privacy rules.

The Pardus Security team work is started from the below part:

    #. After the vulnerability is send to vendor-sec_ e-mail list, Pardus security team controls whether this vulnerability affects Pardus repositories. All Pardus distributions is controlled.

    #. If the vulnerability exists a private bug is reported to Pardus bugzilla.

    #. The bug is generally reported before the CVE-ID assignment, so after the assignment bug is updated. All informartion about the vulnerability (discussions on vendor-sec or other platforms) is reflected to bug report.

    #. The report is assigned to related package maintainer. The permission ro read the bug is gived only the developer and security team members. The necessary patch is added and date of the embargo is waited. During this period, any information is pumped out and can not be committed to public repositories.

    #. During the embargo period the bug resolved and the package maintainer and the security tester test whether the vulnerability is fixed or not. The aim of embargo period is for this. In other words, when the embargo period is finished, all of the distributions can take the bug fixed package to the public repositories rapidly and synchroneously.

    #. After the vulnerabilty is opened to public, the details about it published as PLSA.

    #. The private bug becomes public and the PLSA link is also gived. The state of the bug is marked as RESOLVED/FIXED.

    #. The written PLSA is also send to pardus-security e-mail list.

Vulnerabilities from oss-security
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the security bug has not come from vendor-sec_ and if they comes from public
security lists like oss-security_, the process will be a little different.
The members of this list is generally consist of the distribution security team
members or other people who are interested in security.

oss-security_ e-mail list is used for the public vulnerabilities which has not
already a CVE-ID and discussions about them.

All people can request a CVE-ID from oss-security_ list. Assigning a CVE-ID to a
security vulnerability simples the tracking process. A CVE-ID can be requested
for the fixed security vulnerabilities of an open source upstream project.
This case can generally be happened when a ChangeLog or a NEWS document has an
information about security for a specific software update. The mails like "Xxx
project has release a new version, and this closes yyy vulnerability, please
assign a CVE-ID?" are very common.

The other goodness of this list, it enables to keep track of kernel and kernel
family vulnerabilities. Eugene Teo from RedHat, has a strong interest for kernel
vulnerabilities and request CVE-ID. Therefore the way to track kernel
vulnerabilities becomes easier. While a kernel vulnerability exist, Eugene gives
the link of its bug report as a reference. It is suggested to follow this report
with a bug CC.


How the security update takes place?
------------------------------------

Pardus Security Team uses bugzilla in order to track the security vulnerabilities.
There exists a main security bug report and also exists blockers for each Pardus
distribution. Therefore distribution specific security vulnerabilities can be seen.

The vulnerability reported to bugzilla with BugSPY_ application. The script
file-sec-bug_.
can automatically file the security bug report to bugzilla. The script
check-todo-issues_
can also be used in order to download all CVE database and send the related
CVE-IDs automatically to bugzilla.

.. _BugSPY: http://svn.pardus.org.tr/uludag/trunk/bugspy/

There exists a template for vulnerability reports. This report consists of a
summary and a information about the vulnerability.

An example of a filed vulnerability report with file-sec-bug_::

        php: unsafe unserialize() remote code execution flaw (CVE-2010-2225)

        DESCRIPTION
        ===========
        A use-after-free vulnerability was discovered in the deserialization of
        SPLObjectStorage objects that can be abused for leaking arbitrary memory
        blocks or execute arbitrary code remotely.

        SOLUTION
        ========
        There is no known solution yet.

        REFERENCES
        ==========
        [1] http://this-is-reference.com/
        [2] http://www.php.net/foo-advisory.html

        NOTES
        =====
        The exploit shown in the advisory does not work with suhosin patch.
        However, it is possible for more sophisticated exploits to work with
        suhosin.

The report can simply be filed with the command "file-sec-bug_.py <file-name>"
the file name includes a text like above. This script will request; the
assignee, CC list and privacy information.

That has mentioned above the blocker bugs related to specific Pardus distribution
will also be opened. They will also be private.

For example the below blocker bug report will be filed for the above main bug report::

        Summary: php: unsafe unserialize() remote code execution flaw (CVE-2010-2225) - Pardus 2009
        Blocks: #21345
        Details: Pardus 2009 is affected from bug #12345

After reporting tahe bug, the bug also be documented under private repository.
The reported bug should added under the title "In bugzilla, not fixed yet".
This tracker document provides a coordination between security, test and release
manager. Thanks to this file all security vulnerebilities status can be seen and
controlled from one point.

After the vulnerability fixed and it should be committed with a description which
includes "BUG:FIXED:bugID" information. This means that the given bugID bug is
fixed. For example if a bug with ID #1337 is fixed for Pardus 2009 repositories,
the commit description should include "BUG:FIXED:1337" information.

After the package has taken to stable repository the package is taken from
"In bugzilla, not fixed yet" to "Fixed but needs compiling" part in mentioned
tracker document. After that the release manager will build the package and take
it to "Compiled and waiting in testing" part in tracker document.

After the tests finished the tested and problem free packages are taken to
"Tested and ready for stable, waiting merging" part in tracker document.

Then release amanger takes the packages to stable binary repositories. Release
manager will also send a notification mail about security updated packages with
"Security Fixes (<date>)" subject. He/She takes the announced packages from
"Tested and ready for stable, waiting merging" to "Merged to stable but needs
PLSA to write" part in tracker document.

At this point the security supervisor will publish PLSAs and give bug report
references in PLSAs. Also he/she gives the PLSA numbers and links to the related
bug as a comment.

The script "file-sec-bug_.py" is generally used for vulnerabilities which have not
CVE-ID yet. If a bug has the CVE-ID, an other application SecureSPY_ can be used in
order to download the CVE database and file the related ID's to bug report.

.. _SecureSPY: http://svn.pardus.org.tr/uludag/trunk/bugspy/security

The script `./bin/update -v <http://svn.pardus.org.tr/uludag/trunk/bugspy/security/bin/update>`_
will update the `data/CVE/list <http://svn.pardus.org.tr/uludag/trunk/bugspy/security/data/CVE/list>`_
database. Using the diff command the newl added CVE-ID assignments can be found.
After the CVE-ID update the
./bin/check-todo-issues_
script can be used for the applications on CVE database. For the usage of this
script: The **ENTER** key passes an other CVE-ID. The inputs are marked with TODO
label by default. If the vulnerability is not related with a package in our
repositories, its CVE-ID should be marked as "NOT-FOR-US" with **N** key. If
it affects one of our repositories, it should be used **B** key in order to open
a bug report for it. When the **B** key is pressed an interactive command prompt
will guide. Thanks to this script, the vulnerability report will be performed
according to template format mentioned above and the CVE-ID information is also
included in this report. After this point the title should be changed on bug
report.

If there exist a bug report and a CVE-ID assigned, the bug ID should be gived
for the related CVE-ID with <#bugID> format. The script will also add the CVE-ID
and its description to the bug if they are not exist. If a bug hase more then one
CVE-ID, the bug ID should also be added for all rlated CVE-IDs.

If a mistake was made during this session, and a bug affected our repository was
marked as **N** (NOT-FOR-US), the input "NOT-FOR-US" should be found in
`data/CVE/list <http://svn.pardus.org.tr/uludag/trunk/bugspy/security/data/CVE/list>`_
file for the related CVE-ID and the information "NOT-FOR-US: fooo" should be
replaced with "TODO: check" and the 
./bin/check-todo-issues_
script should be run. After this correction the CVE-ID will be again listed and
the normal process will occur. 

You can find the details with running "./bin/check-todo-issues --help" and
you can look the `data/CVE/list <http://svn.pardus.org.tr/uludag/trunk/bugspy/security/data/CVE/list>`_
format.

You can track PLSA's from security `website <http://security.pardus.org.tr/>`_ and
`rss <http://security.pardus.org.tr/en/rss/>`_. You can also get an account from
`security mail list <http://liste.pardus.org.tr/mailman/listinfo/pardus-security>`_.

.. _file-sec-bug: http://svn.pardus.org.tr/uludag/trunk/bugspy/bin/file-sec-bug.py
.. _check-todo-issues: http://svn.pardus.org.tr/uludag/trunk/bugspy/security/data/CVE/list

