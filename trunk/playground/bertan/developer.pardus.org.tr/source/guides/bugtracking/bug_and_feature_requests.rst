.. _bug-requests:

Bug Requests
============

Bugzilla is the bug tracking system that is used for Pardus Linux Distribution. Thanks to this tool feedbacks can be taken from users and developers on bugs and Pardus can be improved more powerfully.

Sometimes new reported bugs has some inadequate and improper informations. While the reporters waste their time file bugs, developers have to spend more time in order to comprehend, analyse and fix the bug. Moreover bugs can be closed or left uninterested because of missing and inaccurate information.

The following information is about how bugs can be reported more accurately and efficiently.

When do I need to file a bug?
-----------------------------

If there does not exist any bug already been reported, the bugs of the software that is mentioned in the release notes, on mailing lists or other formal documentation can be reported. Please do not hesitate to report bugs, under the assumption of everyone else is also seeing the same problem you are. The bug reports are so valuable in order to track them properly, because the problems that are figured out among the noise of mailing lists or irc-channels can be overlooked.

Bug Cycle
---------

You can find additional information from `bug cycle`_ document.

Before reporting a bug
----------------------

First thing you have to do is taking an account from http://bugs.pardus.org.tr. This is a very quick and simple process. See https://bugs.pardus.org.tr/docs/en/html/myaccount.html.

Understanding Bug Tracking System
---------------------------------

Understanding the way of developers to comprehend, analyse and fix the bugs and reporting the bugs in that way, make developers more receptive and more likely to fix the bugs. If you have never used Bugzilla before or are new to filing bug reports, it may be helpful to read the following pages.

    * https://bugzilla.mozilla.org/page.cgi?id=etiquette.html
    * `Effective bug reporting <http://www.chiark.greenend.org.uk/~sgtatham/bugs.html>`_

Base software are used by every user and it is possible that users will report bugs for them. But it does not mean that these software is more erroneous.

Find Duplicate Bugs
-------------------

Before reporting your bug, you should be sure that your bug has not already been reported. The simplest way to make a `keyword search <http://bugs.pardus.org.tr/query.cgi?format=specific>`_. Or you can use `advanced search <http://bugs.pardus.org.tr/query.cgi?format=advanced>`_. You can also look the `most reported bug statistics <http://bugs.pardus.org.tr/duplicates.cgi>`_.

It is not a useful way is to say "I am also experiencing this bug.". But you can give additional and useful details (log files, error reports etc.) about when you have experienced the bug. 

See :ref:`finding-duplicates`.

Gather Useful Information
-------------------------

For additional information  `Gather Information for Specific Bugs`_.

Generally useful to check /var/log/messages and ~/.xsession-errors (for desktop users) files. There are also software specific log files under /var/log directory, you can look log files according to your bug and attach them to the report.

Start to file a bug
-------------------

You can file a bug report from `there <http://bugs.pardus.org.tr/enter_bug.cgi>`_.

You should read `bug writing guidelines <http://bugs.pardus.org.tr/page.cgi?id=bug-writing.html>`_ carefully.

Please pay attention to give all informations about the bug and to use a clear expression. Comment like "This to be fixed!", "This is catastrophic!" are not good, this type of comments generally are seemed as hostile and attacking by developers, and this doesn't help them to fix the problem.

Find right component
--------------------

This is very important to choose right product and compenent while filing a bug report. You can find directly the right developer by choosing the right component and this helps resolve the bugs faster. If you assign your bug to a wrong component, your bugs fixing should wait until a developer or a bug triager have assigned it to right component.

See details from :ref:`correct-component`.

After reporting bug
-------------------

    * Developers generally do not send an acknowlegement comment that they are dealing with the bug. You should be patient during your bug left commentless, and you should keep on following.
    * After reporting the bug, other users can comment it or developers can change the status or resolution of the bug report. In order to see different resolutions and status used in Pardus bug tracking system please visit `bug cycle`_.
    * Please do not allow someone to depart from your bug's subject. The irrelevant conversations in your bug comment cause only confusion and difficulty to track it.
    * If you think your bug has fixed but an other bug will exist about the same component, please file a new bug report.
    * If your bug is relevant to a release that reaches its end of life, the bug triagers will control whether this bug is experienced for maintained releases. If the bug is not reproducible for the maintained releases, they will close it.

Gather Information for Specific Bugs
------------------------------------

Installation Bugs
^^^^^^^^^^^^^^^^^
    * Please add /var/log/yali.log file of the buggy installation.
    * Please add "fdisk -l" output to the bug report, if this is a bug about partitioning.

In order to take YALI related files:

* Press CTRL+ALT+F1 buttons at the same time.(This button directs you to system console.)
* Plug a usb stick to the machine.
* Mount the usb stick to the system:

::

    mkdir /mnt/log
    mount /dev/<your_usb_stick_partition> /mnt/log

* Copy the files that are needed for the bug.

::

    cp /var/log/yali.log /mnt/log
    fdisk -l > fdisk.txt
    cp fdisk.txt /mnt/log
    cp /etc/fstab /mnt/log

* Unmount the usb stick:

::

    umount /dev/<your_usb_stick_partition>


Crashes
^^^^^^^
If you have encountered with a program crash, you should add the stack trace of the program. Program crashes are hard to reproduce and fix. Therefore it is so valuable to give more information.

If you use Pardus test repository, you can add the debug repository of the related release http://packages.pardus.org.tr/pardus-x-debug/pisi-index.xml.bz2 and install the debug package of the buggy package and you can catch debug symbols from stack trace that very useful to fix the bug.

Freeze and Panics
^^^^^^^^^^^^^^^^^

If all machine is freezed or the screen is all black:
    * Check whether or not CapsLock, NumLock key are ligthing when you activate them. If they are ligthing, there is something else going on.
    * In order to check the booting problems, please run the system without splash. In order to achieve this, you should change "splah=silent" to "splah=verbose"
    * For the possibility of a bug about graphic cards, please boot the system without video card option. In order to do this, please select F4 function key and choose "Graphic Cards Disabled" at boot screen.
    * In order to state the problem specifically, you can disable various features. You can do this by pressing F5 function key and selecting ACPI disabled, Local APIC disabled successively on boot screen.
    * If the system could not boot, please take a digital camera photo of the last thing on the screen.


Hardware Specific Bugs
^^^^^^^^^^^^^^^^^^^^^^

If you think the error that you experienced is hardware related, you can add the link of your system smolt profile. In order to make this, run "smoltGui" on console and click sendProfile button on the opened window. Smolt will send you, the smolt profile link.

Hardware specific bugs are generally related with video cards, graphics card, camera, printer etc, not related with openoffice, calculator, texlive etc.

Programming related bugs
^^^^^^^^^^^^^^^^^^^^^^^^

    * Run the program on console and send all output with bug report. See :ref:`correct-component`.

X server related bugs
^^^^^^^^^^^^^^^^^^^^^

* The following command outputs should be added.

::

    lspci -nn > lspci.txt
    dmesg > dmesg.txt
    lsmod > lsmod.txt

* If the system and keyboard are working, please also add X server logs:

::

    cat /var/log/Xorg.0.log > xserver.txt

* If they are not working: Boot your system on VESA mode and take the following log:

::

    cat /var/log/Xorg.0.log.old

If the X was crashed, you can collect all above commands buy the below procedure:

* Press CTRL+ALT+F1 buttons at the same time.(This buttons direct you to system console.)
* Plug a usb stick to the machine.
* Mount the usb stick to th system:

::

    mkdir /mnt/log
    mount /dev/<your_usb_stick_partition> /mnt/log

* Copy the files that needed for the bug.

::

    cp <output> /mnt/log

* Unmount the usb stick:

::

    umount /dev/<your_usb_stick_partition>


For most of things COMAR log file is also needed:

::

    cat /var/log/comar3/trace.log > comar.txt

For network-manager
^^^^^^^^^^^^^^^^^^^

In order to learn network device information:

::

    lspci -nn > lspci.txt

Ethernet related problems:

::

    ifconfig -a > ifconfig.txt

Wireless related problems:

::

    iwconfig > iwconfig.txt

for disk-manager
^^^^^^^^^^^^^^^^
::

    fdisk -l > fdisk.txt
    cat /etc/fstab > fstab.txt

for service-manager
^^^^^^^^^^^^^^^^^^^

::

    service -N > service.txt

for boot-manager
^^^^^^^^^^^^^^^^

::

    cat /boot/grub/grub.conf > grub.txt

for firewall-manager
^^^^^^^^^^^^^^^^^^^^

::

    service -N > service.txt
    iptables > iptables.txt

camera and video device related bugs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The below command output should be taken after all camera related programs closed:

::

    dmesg > dmesg.txt
    cat /var/log/syslog > syslog.txt
    lsusb > lsusb.txt
    test-webcam > webcam.txt

Audio Device related bugs
^^^^^^^^^^^^^^^^^^^^^^^^^

Run the below command as root, and take the WWW link:

::

    alsa-info

User authentications and permissions related bugs
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If the audit server has been started, you can add the following command output to bug report:

::

    tail /var/log/audit/audit.log > audit.txt

If it was not start:

::

    tail /var/log/messages


Firefox related bugs
^^^^^^^^^^^^^^^^^^^^

* In order to find the problem is related with firefox or its add-on: (If the problem is about the plugin please add plugin name to bug report)

    * Follow Tools -> Add-ons path and disable the enabled add-ons one by one and try to reproduce the bug for each. (After each disable of an add-on firefox should be restarted.)
    * In order to test firefox without using any add-on or theme, please run "firefox -safe-mode" command on console.
    * It would be useful to add the add-on and theme names used to bug report.
* Sometimes the problems are related with some special changes that have done by user, for these type of situations please try to reproduce the problem with creating a new user on the system.

See Firefox crashes on :ref:`stack-traces`.


Openoffice related bugs
^^^^^^^^^^^^^^^^^^^^^^^

* If a crash is experienced when openoffice start, this can be about OpenGL.
    * Please run `tstgl.c <http://developer.pardus.org.tr/guides/bugtracking/scripts/testgl.c>`_ file:

        ::

            gcc testgl.c -o testgl -lX11 -lGL
            ./testgl

    * If this command is also crashed, the problem is not about openoffice.
* When the openoffice is crashed, if it shows a dialog, please add it to the bug report.
* You can also take the stack trace, with installing its debug packages: see :ref:`stack-traces`.

    For example if a crash is occured for open office writer, the below commands should be run:
    ::

        vim `which oowriter`
            /opt/OpenOffice.org/lib/ooo-3.2/program/soffice.bin

        gdb /opt/OpenOffice.org/lib/ooo-3.2/program/soffice.bin
        run -writer
        bt

The stack trace output should be added to the bug report (-writer parameter will change according to openoffice applicaiton type. -calc, -impress, -math etc)


Enhancements and new feature requests
-------------------------------------

* Pardus Linux Project is an open source project, therefore before reporting an enhancement or a new feature please visit :ref:`forbidden-items`.
* Please don't forget to select newfeature severity reporting it from the bugzilla.
* Please explain the feature clearly and give the aim of it for Pardus Linux Dist.
* Requesting a new package is not a new feature or enhancement please report these from Packages/New Packages product on bugzilla.

See details from :ref:`newfeature-requests`.

Graphical User Interface related bugs
-------------------------------------

If a graphical user interface bug exist, the best is to add the screenshot of it to the bug report. Screenshots enables developers to see the problematic part more easy.

* In order to take screenshots, you can press "Print Screen" key on keyboard or you can also use gimp and take screenshot by following File -> Create -> Screenshot way.
* In order to take video you can use recordmydesktop package.

**Last Modified Date:** |today|

:Author: Semen Cirit
.. _bug cycle: http://developer.pardus.org.tr/guides/bugtracking/bug_cycle.html
