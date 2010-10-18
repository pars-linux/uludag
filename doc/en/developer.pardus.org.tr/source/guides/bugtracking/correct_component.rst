.. _correct-component:

Finding Correct Product and Component
=====================================

Which Program?
--------------

In order to see which programs run on your desktop, please press CTRL+ESC keys or press ALT+F2 keys and write "System Activity" and then press ENTER.

If you want to find out exactly what command a specific menu item will run, in KDE you can do the following:

    * Right click to the program on Kmenu, and choose "Add to Panel" option,
    * Right click to the icon stated on panel and select "icon settings" option,
    * Look the command part from Applications tab and close the window.
    * Right click again on th icon and choose "Remove icon" option, therefore we can take back all we have done.

Which file?
-----------

If you know the command, but you don't know the file path, the following command can help you:

::

    which <command-name>

The first line of the output that you seek.

    For example::

                $ which ssh
                /usr/bin/ssh

Which pisi package?
-------------------

After learning command and file path, you can find easly which pisi package has this file:

::

  pisi sf <file path>

For example::

        $ pisi sf /usr/bin/ssh
            /usr/bin/ssh is searched
            openssh package contains usr/bin/ssh file.

Therefore you can find programs package and file your bug related to this information.

For the packages that you have not installed, you can make a file path research on http://packages.pardus.org.tr.

Sometime the problem is library or plugin dependent, for this time just make your best guess. A triager or developer will reassign the bug if necessary.

**Last Modified Date:** |today|

:Author: Semen Cirit

