.. highlightlang:: rest

General Pardus Howto
****************************

Installing Build Essentials
---------------------------------

If you need to compile a source package, you'll have to install development tools first. You can do this simply by typing this command in a console

.. code-block:: bash

    $ sudo pisi install -c system.devel

.. _setup-fixed-ip-address:

Setup a fixed IP address for your computer
---------------------------------------------

Introduction
^^^^^^^^^^^^^^^^

When you use your PardusPC in a LAN network for sharing printer(s) or remote file sharing with another LinuxPC(ssh) or WindowsPC(samba) it is highly advisable to give all computers a fixed IP address.

This is to prevent problems after a restart of the computer(s).

What we need
^^^^^^^^^^^^^^^

We need to know the "DHCP Client Range" and the "Default Gateway" of the router. The DHCP Client Range can only be found after making contact with the router. How to get access to the router is in the manual of the router.

Once you have access to your router check for: 

    * DHCP Client Range
    * Default Gateway (if not present it will be the IP address to get access to the router) 

Changing the IP address
^^^^^^^^^^^^^^^^^^^^^^^^^^

Open Tasma > Internet & Network > Network Manager.

    Remove the mark at the interface and select [Configure connection].
a    aSelect "Manual" and fill in:::

 Address:  new fixed IP address
 Net mask: 255.255.255.0 (pull-down menu)
 Gateway:  Default Gateway of the router
 (for 'new fixed IP address' take an address just above the DHCP Client Range)
 
 Select [Apply]. 
 Mark the interface and the new IP address should appear. 
 Check if your internet connection in Firefox is still working and in case of problems return to "Automatic Query (DHCP)" in Network Manager. 
 Close Network Manager and Tasma. 



How to print in Pardus to a remote Pardus printer
-----------------------------------------------------

Problem
^^^^^^^^^^
I have Pardus installed on a PC, and my Canon PIXMA printer is connected to it by means of USB. 
The PC is connected to an ADSL router. 
Also connected to the ADSL router but then wireless is my Pardus laptop. 
I have a simple question but tried lots of features in Tasma/KDE Print but I can not manage to solve it. 
How can I print from my Pardus laptop to the printer that is connected to my Pardus PC? 

Manual how to solve this problem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The computer with the printer connected is called the "server-PC" and all other computers in the network are called "client-PC". 

IP address of the computer with the printer connected "server-PC"
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It is highly recommended to give the computer with the printer connected a fixed IP address. See :ref:`setup-fixed-ip-address` for ip addressing.

Settings on server-PC
^^^^^^^^^^^^^^^^^^^^^^^

Change settings of firewall:

Open Tasma > Internet &Network > Firewall Config::

    Advanced > +
    Incoming
    Port Range = 631
    Accept
    OK > Apply > Back

Close Tasma 

Change of /etc/cups/cupsd.conf with [Alt+F2] kdesu kwrite /etc/cups/cupsd.conf + [Run]::


    # Administrator user group...
    SystemGroup pnpadmin
    Port 631    <== add this line
    .
    .
    # Restrict access to the server...
    <Location />
      Order allow,deny
      Allow @LOCAL    <== add this line
    </Location>

Save change and close Kwrite.

Settings on client-PC
^^^^^^^^^^^^^^^^^^^^^^^^^

Change of /etc/cups/client.conf with [Alt+F2] kdesu kwrite /etc/cups/client.conf + [Run]::

    ServerName localhost
    ServerName IP address of the server-PC    <== example ServerName 192.168.0.205

Save change and close Kwrite.

Configuration of printer.::

    [Tasma]>{Peripherals]>[Printers]>{Add}>{Add Printer/Class...}
    [Next >]
    [Remote CUPS server (IPP/HTTP)]
    [Next >]
    {Anonymous (no login/password))}
    [Next >]
    Host: = IP address of the server-PC
    Port: = 631
    [Next >]
    Select the printer. 
    [Next >]
    Select the {Manufacturer} and {Model}
    [Next >]
    Select the recommended driver (if not working select the simplified version)
    [Next >] 
    Test the printer
    [Next >] (3x)
    Supply a name for the printer 
    [Next >] (2x) [Back] and close Tasma

Important
^^^^^^^^^^^^^^

Restart all computers to apply all the changes.


How to make an image(backup) of a disk/partition to a remote PardusPC
-----------------------------------------------------------------------

Introduction
^^^^^^^^^^^^^^^^^

When you want to do a new installation(dual boot) of Pardus on a computer (WinPC) which already has another OS (Windows), it is highly recommended to make an image(backup) of the disk/partition.

The problem is where to put this image?

This is a manual about making and writing the image to a remote computer with an active Pardus 2008.1 (PardusPC).

Hardware and software requirements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To make the image use a Live CD with clonezilla-live-1.2.1-xx.iso which can be downloaded from http://www.clonezilla.org/download/sourceforge/

A second computer with an active Pardus 2008 OS is used to store the image.

The two computers are connected with a (Sitecom WL-535) router.

The PardusPC must have an active samba setup as described in http://en.pardus-wiki.org/HOWTO:SambaNetwork

"Making /home/samba (share) writable" is important.

The administrator password and IP address of the remote PardusPC must be available.

To show the IP address select the Network-applet in the system tray. 

Menu item activation in Clonezilla.
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To activate a menu item in Clonezilla do:

Menu items with [ ]:go to the item with the arrow keys, hit the spacebar ([ ]>[*]) and activate with the [Enter] key.

Menu items without [ ]:go to the item with the arrow keys and activate with the [Enter] key. 

Boot the WinPC with the Clonezilla liveCD.

Here is a list of the menu items with my input/selection between ().

       1. Select your language.
       2. Configuring console-data ... (Don't touch keymap).
       3. Start_Clonezilla
       4. Choose the mode: ... (device-image)
       5. Mount image directory ... (samba_server)
       6. Mode to setup the network ... (dhcp)
       7. IP address ... (modify = IP address of the PardusPC)
       8. Domain in the samba server ... (leave empty)
       9. Account in server ... (accept default=administrator)
       10. The directory where.... (modify = /share)
       11. Now you have to enter the password for ... (modify = administrator password of the PardusPC)
       12. Choose the mode: ... (saveparts)
       13. Input a name to save the image ... (modify = whatever you want, this will be the name of the directory of the image)
       14. Choose the source partition ... (select the partition you want to image)
       15. Which clone program(s) ... (accept default)
       16. Set advanced parameters ... (accept default)
       17. Choose the compression ... (accept default=-z1)
       18. The size (MB) to split ... (accept default=2000)
       19. The action when client ... (accept default)
       20. Are you sure you want ... (y) 

Wait .......and at the end select your Start over/Poweroff option. 


Making a USB version of Clonezilla/Gparted in order to install Pardus on a Netbook
-------------------------------------------------------------------------------------

Introduction
^^^^^^^^^^^^^^^^^^^^

For this we need a USB stick with a mimimum of 2GB.

We will create two partitions, a 125MB FAT16 partition for Clonezilla/Gparted and the remaining space for a FAT32 partition to save the Pardus image file ~1.4GB.

Clonezilla-USB is used to restore the Pardus image file to the hard disk of the Netbook. Once Pardus on the netbook is active we can use the GParted-USB for resizing the user (/home) partition on the netbook.

General Setup
^^^^^^^^^^^^^^^^^^

pen GParted and remove all existing partitions from the USB stick.

Create a new 125MB FAT16 partition on the USB stick.

Set the Boot flag of the 125MB FAT16 partition (don't forget this one).

Make a note of the /dev/sd?1 USB drive letter value. In this case it is "b" (/dev/sdb1)

Create on the remaining free space of the USB stick a FAT32 partition.

Close GParted.

On the Desktop in System mount the 526M Removable Media and note the mounting point /media/sd?1. In this case "/media/sdb1"

Open a terminal and make a new directory::

    mkdir netbook-usb

Cd into netbook-usb::

    cd netbook-usb

To be able to boot from the LiveUSB, a boot loader for Linux operating from a FAT filesystem is required. The Open Source project SYSLINUX will do this job.

Download the latest syslinux-??.zip file to the above created netbook-usb directory from URL: http://www.kernel.org/pub/linux/utils/boot/syslinux/. At this moment syslinux-3.73.zip (4.4MB)

Unpack syslinux::

    unzip syslinux-3.73.zip

Write the MBR of the USB::

    cat /usr/lib/syslinux/mbr.bin > /dev/sd?  (replace ? with your USB drive letter)

Write the boot file to the 125MB FAT16 partition::

    sudo ./linux/syslinux -s /dev/sd?1  (replace ? with your USB drive letter)

Download the latest "Clonezilla live zip file for USB flash drive or USB hard drive > Stable branch from http://www.clonezilla.org/download/sourceforge/ to the above created netbook-usb directory. At this moment clonezilla-live-1.2.1-39.zip (94.9MB)

Download the latest gparted-live-???.zip file to the above created netbook-usb directory from URL: http://gparted.sourceforge.net/download.php. At this moment gparted-live-0.4.1-2.zip 

Clonezilla or GParted
^^^^^^^^^^^^^^^^^^^^^^^^^

If present remove all files and directories except ldlinux.sys from the 125MB FAT16 partition.

Unpack the wanted.zip to the 125MB FAT16 patition::

    unzip clonezilla-live-1.2.1-39.zip -d /media/sd?1  (replace ? with your USB drive letter)

or::

    unzip gparted-live-0.4.1-2.zip -d /media/sd?1  (replace ? with your USB drive letter)

Close the terminal.

On the Desktop in System unmount the 125M Removable Media.


Installing graphics card drivers for Pardus 2008
--------------------------------------------------

**Method 1** - The first method is automated:

Run: Display Manager [Tasma>System]

Click: Detect Drivers


**Method 2** - This method has a GUI and involves selecting the exact packages you need:

Run: Package Manager

Click: Show New Packages

Search: "nvidia"

Check: Appropriate checkboxes. (depending on the age of your graphics card)

Click: "Install Package(s)"

Press: [Control-Alt-Backspace] /OR/ Reboot


**Method 3** - The third method requires Konsole and is a text-only installation of the NVIDIA packages:

Run: Konsole [Programs>System]

Type: "sudo pisi ur"

Type: "sudo pisi it nvidia-kernel nvidia-glx nvidia-tools"

Type: "sudo nvidia-xconfig"

Press: [Control-Alt-Backspace] /OR/ Reboot 

.. XXX more?

