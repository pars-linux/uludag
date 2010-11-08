.. _subversion-usage:

Subversion Usage
================

:Author: Ozan Çağlayan, Semen Cirit
:Date: |today|
:Version: 0.1

This document is not a detail subversion howto but it gives some tricks about
subversion usage.

If you want to learn more please see `subversion book`.

What is a subversion repository?
--------------------------------

A repository is a disk area on which the last version, all the versions prior to
the last version and the changes between versions of the software package(s)
every developer works on, information including their user, date and cause are
stored which can be reached by several methods.

How do I check if I have subversion on my system?
-------------------------------------------------

As the quickest way to see if you have Subversion in your system or not, you can
refer to the output of *svn --version* command .

It's a good sign if you see something like this::

    user@machine ~ $ svn --version
    svn, version 1.6.12 (r955767)
    compiled Aug 24 2010, 10:27:44

    Copyright (C) 2000-2009 CollabNet.
    Subversion is open source software, see http://subversion.tigris.org/
    This product includes software developed by CollabNet (http://www.Collab.Net/).

    The following repository access (RA) modules are available:

    * ra_neon : Module for accessing a repository via WebDAV protocol using Neon.
      - handles 'http' scheme
      - handles 'https' scheme
    * ra_svn : Module for accessing a repository using the svn network protocol.
      - with Cyrus SASL authentication
      - handles 'svn' scheme
    * ra_local : Module for accessing a repository on local disk.
      - handles 'file' scheme

How do I get a copy of a directory in the repository?
-----------------------------------------------------

In order to create a copy(checkout) of the repository *svn co* command is used.
Once the copy is created, no more processing is performed on this command copy.

::

    user@machine ~ $ svn co http://svn.pardus.org.tr/uludag
    A    uludag/trunk
    A    uludag/trunk/PyNotify
    A    uludag/trunk/PyNotify/.project
    A    uludag/trunk/PyNotify/libPyNotify
    A    uludag/trunk/PyNotify/libPyNotify/genericDevice.py
    A    uludag/trunk/PyNotify/libPyNotify/genericActions.py
    A    uludag/trunk/PyNotify/libPyNotify/__init__.py
    A    uludag/trunk/PyNotify/libPyNotify/iconFinder.py
    A    uludag/trunk/PyNotify/icons
    ..
    ..

You can treat the repository as if its an URI. By doing so, you can get any
subdirectory in the repository without checking out the whole repository::

    user@machine ~ $ svn co http://svn.pardus.org.tr/uludag/trunk/comar
    A    comar/belgeler
    A    comar/belgeler/comar-polkit.txt
    A    comar/belgeler/comar-python-types.txt
    A    comar/belgeler/PardusInitSystem.lyx
    A    comar/belgeler/Boot.Loader.txt
    A    comar/belgeler/ComarMimarisi.lyx
    A    comar/belgeler/comar-dbus.txt
    A    comar/belgeler/teknik-sunum.odp
    A    comar/belgeler/PardusAcilisSistemi.lyx
    A    comar/belgeler/temel-sunum.odp
    A    comar/betikler
    A    comar/betikler/pppoe.py
    ..
    ..

How do I know if my local copy is up-to-date or not?
----------------------------------------------------

You have to update the copy of the repository you have periodically with
*svn update* command in order to know about the last changes and to track
the last version.

If you call the command alone, all the files and the subdirectories in the
current working directory will be updated recursively::

    user@machine trunk $ pwd
    /home/machine/pardus/uludag/trunk
    user@machine trunk $ svn update
    G    comar/mudur/bin/mudur.py
    U    comar/belgeler/comar-polkit.txt
    A    comar/belgeler/Boot.Loader.txt
    U    comar/comar/ChangeLog
    U    comar/comar/src/dbus.c
    U    comar/zorg/data/DriversDB
    U    comar/api/setup.py
    A    comar/api/examples/qt3
    A    comar/api/examples/qt3/mainform.ui
    A    comar/api/examples/qt3/app.py
    A    comar/api/examples/qt3/Makefile
    A    comar/api/examples/qt4
    A    comar/api/examples/qt4/mainform.ui
    A    comar/api/examples/qt4/app.py
    A    comar/api/examples/qt4/Makefile
    U    pisi/ChangeLog
    ..
    ..
    Updated to revision 20808.

You can also append the file or the directory you want to update at the end of
the command::

    user@machine $ svn update buildfarm
    U    buildfarm/templates.py
    U    buildfarm/setup.py
    Updated to revision 20808.


How can I see what directories exist in a repository?
-----------------------------------------------------

A single repository may contain more than one directory in it. The hierarchy of
a repository is just like the inside of a directory on a disk. So, you can browse
without having to copy all the repository to your disk and just get a view of the
part you want to work on or have a look at. The list of directories and files in a
repository is displayed using *svn ls repository_address* command::

    user@machine ~ $ svn ls http://svn.pardus.org.tr/uludag
    branches/
    tags/
    trunk/

    user@machine ~ $ svn ls http://svn.pardus.org.tr/uludag/trunk
    CD-image/
    PolicyKit-kde/
    PyNotify/
    artwork/
    baselayout/
    .
    .
    .

What does the capital letters beside the file names mean?
---------------------------------------------------------

While you are working with SVN and during processes such as updating and
searching, as in the previous example, the signs by the files are to inform
you about what kind of a change related with the next file is performed.

One of the letters U, D, A, C or G may be found by files::

     * A Added
     * D Deleted
     * U Updated
     * G Merged (the last update you got from the repository is merged with the file you are performing local changes)
     * C Conflicted (the last update you got from the repository is conflicted with the changes you performed localy)

I modified some files, what shall I do now?
-------------------------------------------

Youu can use *svn status* when you want to see the local modifications you did
on a working copy. This command can run with an URI you add to the end of it as
all the other commands.

Below its seen that a file is added to, a file is deleted from and two files are
changed regarding the last updated copy of the repository::

    user@machine $ svn status
    A COMARd/csl/degisiklik
    D COMARd/csl/loader.py
    M COMARd/COMARValue.py
    M comar-call/rpc.c

    user@machine $ svn status COMARd/csl/COMARValue.py
    M COMARd/COMARValue.py

Also, you can learn what you particularly changed in changed files with
*svn diff* command::

    user@machine $ svn diff comar-call/rpc.c
    Index: comar-call/rpc.c
    ===================================================================
    --- comar-call/rpc.c (revision 158)
    +++ comar-call/rpc.c (working copy)
    @@ -146,6 +146,7 @@
    if (len == 0) break;
      if (len == -1) {
          puts("connection broken too soon");
    +         //totally different change
              break;
        }
    printf("RECV[%s]\n\n", buf);

Added part is showed with a "+" sign at the start of the line. Removed or
changed part is signed with "-".

I added a new file but there's a question mark beside it!
---------------------------------------------------------

While you are working on the copy of the repository when you would like to create
a new file, you should inform your local copy about your intention to add that
file to the repository with the help of *svn add* (it has sister commands such as
*svn copy*, *svn del*  as well).

Let's explain why there's such a need as follows:
Let's assume that you would like to compile and test an application which is in
your local copy. In this case, some files that you don't prefer to send to the
main repository will be created in your work copy such as Makefiles and .m4 files
which only you have any need for. In such cases, it will be very advantageous and
convenient if the files added locally are not added to the repository as well,
because when you change the source code of the software, recompile it and decide
to send it to the repository at a proper time, you know that the other files are
not going to the repository. With *svn add*, you add to the repository the files
you want to add. *svn del* will not mentioned again.

::

    user@machine $ svn status
    user@machine $ touch newscript.csl
    user@machine $ svn status
    ? newscript.csl
    user@machine $ svn add newscript.csl
    A newscript.csl
    user@machine $ svn status 
    A newscript.csl
    user@machine $

How do I revert my local modifications?
---------------------------------------

You can revert the modifications you made using *svn revert* command anytime you
like::

    user@machine $ svn status
    A COMARd/csl/thechange
    D COMARd/csl/loader.py
    M COMARd/COMARValue.py
    M comar-call/rpc.c

    user@machine $ svn revert comar-call/rpc.c
    Reverted 'comar-call/rpc.c'

    user@machine $ svn status
    A COMARd/csl/thechange
    D COMARd/csl/loader.py
    M COMARd/COMARValue.py

Its also possible to revert all of the files to their original state recursively::

    user@machine $ svn revert . -R
    Reverted 'COMARd/csl/thechange'
    Reverted 'COMARd/csl/loader.py' 
    Reverted 'COMARd/COMARValue.py'

    user@machine $ svn status
    user@machine $

I want to send the files I modified
-----------------------------------

If you are sure of the last condition of the files you changed, you can use
*svn commit*  to transmit your changes to the repository. By using this command
as its true for all the rest you can send to the repository a single file,
a single directory and what is under it or all the changes you made. When you
run *svn commit*, svn using your preferred text editor opens a file for you with
the changes you made listed in it in order to make sure others see what you
changed and to enable your changes to be logged for backward tracking in the
repository. To alter the text editor opened as the preferred one, you can make
use of the environment variable EDITOR::

    user@machine $ EDITOR="vi" svn commit
    user@machine $ EDITOR="mcedit" svn commit
    user@machine $ EDITOR="kwrite" svn commit

As soon as you write the changes to the text editor, save what you wrote and
close the editor, svn will commit the modifications in your local copy to the
remote repository.

Other commands
--------------

You can run Subversion to learn Subversion commands as well. * svn help command_name*
feeds you back with detailed information about command_name while svn help serves you
with a list of commands you can use::

    user@machine $ svn help
    usage: svn <subcommand> [options] [args]
    Subversion command-line client, version 1.5.3.
    Type 'svn help <subcommand>' for help on a specific subcommand.
    Type 'svn --version' to see the program version and RA modules
    or 'svn --version --quiet' to see just the version number.

    Most subcommands take file and/or directory arguments, recursing
    on the directories.  If no arguments are supplied to such a
    command, it recurses on the current directory (inclusive) by default.

    Available subcommands:
    add
    blame (praise, annotate, ann)
    cat
    changelist (cl)
    checkout (co)
    cleanup
    commit (ci)
    copy (cp)
    delete (del, remove, rm)
    diff (di)
    export
    help (?, h)
    import
    info
    list (ls)
    lock
    log
    merge
    mergeinfo
    mkdir
    move (mv, rename, ren)
    propdel (pdel, pd)
    propedit (pedit, pe)
    propget (pget, pg)
    proplist (plist, pl)
    propset (pset, ps)
    resolve
    resolved
    revert
    status (stat, st)
    switch (sw)
    unlock
    update (up)

    Subversion is a tool for version control.
    For additional information, see http://subversion.tigris.org/

In order to have detailed information about a Subversion command, call *svn help*
with the command name::

    user@machine $ svn help add
    add: Put files and directories under version control, scheduling
    them for addition to repository.  They will be added in next commit.
    usage: add PATH...

    Valid options:
      --targets ARG            : pass contents of file ARG as additional args
      -N [--non-recursive]     : obsolete; try --depth=files or --depth=immediates
      --depth ARG              : limit operation by depth ARG ('empty', 'files',
                                'immediates', or 'infinity')
      -q [--quiet]             : print nothing, or only summary information
      --force                  : force operation to run
      --no-ignore              : disregard default and svn:ignore property ignores
      --auto-props             : enable automatic properties
      --no-auto-props          : disable automatic properties
      --parents                : add intermediate parents

    Global options:
      --username ARG           : specify a username ARG
      --password ARG           : specify a password ARG
      --no-auth-cache          : do not cache authentication tokens
      --non-interactive        : do no interactive prompting
      --config-dir ARG         : read user configuration files from directory ARG

.. _subversion book: http://svnbook.red-bean.com/nightly/en/index.html
