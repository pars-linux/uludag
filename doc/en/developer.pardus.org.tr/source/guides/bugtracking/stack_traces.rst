.. _stack-traces:

Stack Traces
============


What is Stack Trace(Backtrace)?
-------------------------------

List of function calls lead to some point of the program and stack trace (backtrace) lists them. Stack traces can be taken with the assistance of  debugging tools like gdb tack traces from crashed applications so that developers can figure out what went wrong.

What looks like a Stack Trace?
------------------------------

A tipical stack trace is like below:

::

    [New Thread 8192 (LWP 15167)]

    0x420ae169 in wait4 () from /lib/i686/libc.so.6
    .
    .
    .

An other stack trace with debug symbols: We can see filenames and linenumbers of function calls.

::

    0x000000350a6c577f in *__GI___poll (fds=0xe27460, nfds=9, timeout=-1) at ../sysdeps/unix/sysv/linux/poll.c:83
    83          return INLINE_SYSCALL (poll, 3, CHECK_N (fds, nfds), nfds, timeout);
    .
    .
    .



What are debug symbols and what they do?
----------------------------------------

When a program compiled with its debug symbols, additional informations added. These informations can generate a stack trace of the buggy functions called and can list the files and number lines that function exists.

What are debug packages and how do I access them?
-------------------------------------------------

Pardus has debug packages of each normal package. These pacakges are compiled automatically with specific debug symbols. Therefore you can easily install the debug package of the buggy software. You should install debug package which is suitable with its normal package version. In order to install and use the debug packages, you should use related Pardus release test repository (exp: http://packages.pardus.org.tr/pardus-2009-test/). After adding the test repository and updating your system, you can add the related debug repository (ex: http://packages.pardus.org.tr/pardus-2009-debug/) and install the buggy application debug package.


 Example ::

        Find package and related debug package version of buggy application:

        [test@computer ~] $ pisi info amarok
        Installed package:
        Name: amarok, version 2.3.0, revision 38, build 20


Every package has a debug package and you can easily install it like below:

For amarok::

    sudo pisi it http://packages.pardus.org.tr/pardus-2009-debug/amarok-dbginfo-2.3.0.90-40-16.pisi


Using GDB to create stack trace:
--------------------------------

To run GDB:

::

    gdb <buggy application name>


Then write the below value to GDB command prompt:

::

    run

If you need some arguments you can use it like below:

::

    run --argument

After you run the program with GDB, you try to reproduce the crashe senario. After the program crash go back GDB terinal, the GDB prompt should be shown. If not, press CTRL+C keys and write the below command:

::

    thread apply all bt full

If any of them work, write "bt" command to GDB prompt.

These commands will create an output, these outputs are the stack trace. Copy this output to a file and quit GDB.

**Last Modified Date:** |today|

:Author: Semen Cirit

