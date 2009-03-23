.. highlightlang:: rest

Specific Pardus Howto
**************************

STARTUP
-------------

How to disable login screen?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Following the way of "Pardus > Tasma > System > Login manager > Convenience " go to Convenience section.You must be "root" here, so press the "Administrator Mode" button at the bottom of the window and write your root password.There is small box on the left of "Enable Auto login".Put a tick on that box and press on "OK" button at the bottom of the window.

How to enable "NumLock" on startup?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Press the "ALT+F2" buttons and write "kcmshell keyboard" on the command window and press on "run".Click on the "turn on" from the "NumLock on KDE Startup" section.And press on "OK".

How to autostart programs on startup? 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Install "autostart" program from pisi.If you dont know how to install program on pardus look :ref:`how-to-install-and-remove-programs` . Go to Pardus > Tasma > Desktop > Autostrat manager.You can add any program just pressing on "add" button.Dont forget to press on "apply" button at the bottom of the window after you add the program.

How to change splash screen?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First download a splash screen.You can download a splash screen which was made for Pardus from 
`here <http://www.kde-look.org/content/show.php/3lobyte+Pardus+and+New+KDE+3.5+Splash+?content=52201>`_. Go to Pardus > Tasma > Appearance and themes > Spash Screen.Press on the "add" button.Find the splash screen you lownloaded from the window just opened.Press on "OK".Then press on "apply".If you want you can test the splashscreen just pressing on "test" button. 

How to change login screen? 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First lownload a login screen.You can download the login screen which was made for Pardus from 
`here <http://kde-look.org/content/show.php/Login+for+Pardus%2BPardus+giri%C5%9F+temas%C4%B1?content=57871&PHPSESSID=828c9b01f495a86cbd4fa499b6076ca>`_. Go to Pardus > Tasma > Appearance and themes > Kdm Theme administrator.If there is not a program called "kdm theme" here.You should install it.If you dont know how to install program on pardus look here :ref:`how-to-install-and-remove-programs`. Press on the "Administrator Mode" button at the bottom of the window and write your root password.Press on the "Install new theme" button at the bottom of the window.Find the file you downloaded press on "OK" , then "OK" again.You can check your login screen pressing on "ctrl+alt+backspace".

There is another screen apart from splash screen and login screen. How to change it?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Goto "Pardus > Tasma > System> Login manager > Background".You must be "root" here, so press the "Administrator Mode" button at the bottom of the window and write your root password.Choose the picture you like from the "picture" section and press on "OK". 

I don't like startup music, How to change it? 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Go to "Pardus > Tasma > Sound and multimedia > System notifications".Find "KDE is starting up" and click on it.Below press on the folder icon from the "actions" section, choose another sound from there or choose any other sound you like.And press on "OK" then "apply". You can change other system sounds from here. 

PISI (Package Manager)
------------------------------

.. _how-to-install-and-remove-programs:

How to install and remove programs on Pardus?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can install programs on Pardus by PISI (Package manager).You can go to pisi by Pardus > Package manager or Pardus > Tasma > System > Package manager.

There are three buttons called "Show new packages","Show Installed packages","Show upgradable packages".You can upgrade Pardus by pressing on "Show upgradable packages" button,then put a tick on the small box on the left of the package you like to upgrade or just click on the "select all packages in this category" on the top of the window under search bar.Then press on the "upgrade packages"button on the right of the window. Pisi downloads the packages and installs all of them.

You can install the package you like by writing it on the search bar after you press on the "Show new packages" button. Then put a tick on the small box on the left of the package you like, then press on the "install packages" button on the right of the window. Pisi downloads the packages and dependencies and installs all of them after showing you the amount of the download.

You can remove the package you like by writing it on the search bar after you press on the "Show installed packages" button.Then put a tick on the small box on the left of the package you like to remove.Then press on the "Remove packages" button on the right of the window. Pisi removes the package and dependencies.

Note:If you couldnot find the package you like to install try PisiBul  :ref:`PisiBul`.

How to install .tar.gz packages on Pardus?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

These packages are very easy to install on Pardus.It is called installing by source code.First you open the package(right click > extract > exctract here).Then go to folder you've opened and press "f4".This opens the konsole.Then write this commands one by one::

     ./configure 
     make 
     su (and you write your root password) 
     make install

And it install the package.But you cannot install all "tar.gz" packages by this way.You should read "README, INSTALL" files to see how to install.

How to install other packages (.sh, .run, .bin) on Pardus?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can install these packages using konsole.First open the folder you like to install and press "f4".This opens the konsole then write the command according to the package - don't forget the "./" before::

    ./example.sh 

or::

    ./example.bin

or::

    ./example.run

But these packages must be "executable" and have permissions.You should right click on the file (example.sh) > properties > permissions.There is a small box on the left of "is executable" put a tick on it, then press "ok".This is for executable.You can also change the permissions on the same place.

How to add repo "contrib" to pisi (Package Manager)?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There is only one repo on pisi by default(pardus-2007.2).But you cannot find all packages from this repo beacause anly approved packages are included in this repo.But you can add "contrip" repo if you want.

Open pisi (Pardus > Package manager or Pardus > Tasma > System > Package manager). Go to Settings > Configure package manager.Click on "Add new repository".Write "contrip" for "repository" name and write this adress for the repository address:

http://packages.pardus.org.tr/contrib-2007/pisi-index.xml.bz2

Then click on "OK" and "OK" again.

Or you can use konsole and add the repo. Open konsole (press "alt+f2" and write konsole) and write this command::

    sudo pisi ar contrip http://paketler.pardus.org.tr/contrib-2007/pisi-index.xml.bz2 


.. _PisiBul:

What is PisiBul, How to use it?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PisiBul is a helping program defined by one of our friends as formula of simplfied life on Pardus. It helps us find and build pisi packages you could not find by Package manager. You can install Pisibul by following the instructions found `here <https://developer.pardus.org.tr/pisi/pisi-pisibul.html>`_.

Go to Pardus > Utilities > Pisibul and open the program. When you write the package name on the search bar the package appears on the right of the window. Click on the package then press on "the create the package" button. Then you must write root password. After that it creates the pisi package on the desktop after a couple of minutes depending on the amount of the package.You can install the package just clicking on the pisi package.


Under the search bar there are three names "devel", "contrip", "playground". These are the names of the repos. There must be ticks on the small boxes on the left of the names. If there is no it means Pisibul is not searching these repos.

Note:I dont recommend using playground repo.

GRUB
-------

After update,there are two kernels in Grub ,How to delete it?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You should edit "grub.conf" file by going to "/boot/grub/grub.conf" .You can edit "grub.conf" in three ways:

    1) right click on grub.conf "actions > edit as root " and write root password 
    2) "Pardus > System > More applications > File manager" and write root password . Konqueror opens as root.Then go to "/boot/grub/grub.conf" and open "grub.conf" 
    3) Press "Alt + F2" and run command "kdesu kwrite /boot/grub/grub.conf" and write root password. 

You shoul delete the part below the second one.::

    title Pardus 2007
    root (hd0,1)
    kernel (hd0,1)/boot/kernel-2.6.18.5-71 root=/dev/hda2 video=vesafb:nomtrr,pmipal,ywrap,1024x768-32@60 
    splash=silent,fadein,theme:pardus console=tty2 mudur=language:tr quiet
    initrd (hd0,1)/boot/initramfs-2.6.18.5-67

    title Pardus 2007
    root (hd0,1)
    kernel (hd0,1)/boot/kernel-2.6.18.5-67 root=/dev/hda2 video=vesafb:nomtrr,pmipal,ywrap,1024x768-32@60 
    splash=silent,fadein,theme:pardus console=tty2 mudur=language:tr quiet
    initrd (hd0,1)/boot/initramfs-2.6.18.5-67

How to change opening order in Grub?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is my grub.conf::

    default 0
    timeout 10
    background 10333C
    splashimage (hd0,4)/boot/grub/splash.xpm.gz

    title Pardus 2007.2 [2.6.18.8-86]
    root (hd0,4)
    kernel (hd0,4)/boot/kernel-2.6.18.8-86 root=/dev/sda5 video=vesafb:nomtrr,pmipal,ywrap,1024x768-32@60 
    splash=silent,fadein,theme:pardus console=tty2 mudur=language:tr quiet
    initrd (hd0,4)/boot/initramfs-2.6.18.8-86


    title openSUSE 10.3 - 2.6.22.9-0.4
    root (hd0,12)
    kernel /boot/vmlinuz-2.6.22.9-0.4-default root=/dev/disk/by-id/scsi-SATA_ST3250620AS_5QE0H3ED-part13 vga=0x317
    resume=/dev/sda11 splash=silent showopts
    initrd /boot/initrd-2.6.22.9-0.4-default


    title Windows Xp
    rootnoverify (hd0,0)
    makeactive 
    chainloader +1

::
    default 0  This shows the opening order, you can  edit it: 


default 0 = first one = title Pardus 2007.2 [2.6.18.8-86] 
default 1 = second one = title openSUSE 10.3 - 2.6.22.9-0.4 
default 2 = third one = title Windows Xp 

::
    timeout 10  This shows the opening time, you can also edit it

How to reinstall Grub?
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Put Pardus installation cd on cdrom and reboot computer.When you see pardus installation screen::

    press "c". You will see this   "grub>"
    then write "root (0,"    (There is space between "root"and "(0,") and press "tab".This will show you partitions.
    then write "root (0,4)"   and press enter.(this (0,4) is  my pardus partition, you write your partition)
    then write "setup (hd0)"   (There is space between "setup" and "(hd0)".
    Reboot computer by pressing   "ctrl+alt+del"


.. XXX more?

