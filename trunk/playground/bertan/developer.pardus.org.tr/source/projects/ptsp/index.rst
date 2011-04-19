.. _ptsp-index:

PTSP
====

:Author: Metin Akdere

**PTSP** is an abbreviation for Pardus Terminal Server Project which aims to boot
thin clients over the network without needing any extra hardware or software on
the client-side. It helps you to reduce your maintainence and administration costs
in such environments where you need same type of workspace.

Although some other variations of terminal server projects exist out there in the
community, the main reason of creating **PTSP** is to ease the management of the
packages which are used to create rootfs. For instance LTSP_ is another
distribution that is used on the thin-client machines. It has its own packaging
system with a Perl_ based management tool. The created rootfs by ltsp admin tool
is not Pardus. Updating the packages, and keeping up with the distribution is not
an easy task. The management and configuration scripts are hacky. With Pisi_,
Mudur_, Coolplug_, Zorg_ and COMAR_ tools Pardus has all the infrastructure to create
an automatically bootable rootfs with its own packages.

Client-side Packages
--------------------

Following packages will be working on the thin-clients and must be installed to the rootfs:

* **lbuscd**: lbus thin client daemon.

* **ltspfsd**: ltspfs daemon.

* **ptsp-client**: Contains remote X connection service and udev rules for the client rootfs.

Server-side Packages
--------------------

Following packages will be working on the terminal server and must be installed to the server:

* **lbussd**: lbus server daemon.

* **ltspfs**: Fuse file system.

* **ptsp-server**: Contains kernel and initramfs which will be served over tftp, ptsp-client-rootfs,
lbussd daemon.

Installation
------------

Creating a working PTSP workspace consists of three main steps:

* Creating the rootfs which is a scaled-down version of the distrubition

* Preparing the server in order to serve thin clients

* Starting-up the server

Creating Rootfs
---------------

Rootfs will contain system.base component which includes minimal system environment, x11.driver
component to have a working graphical workspace and kernel as usual. After
creating the rootfs, we are archiving it in *"tar.bz2"* format and this will be
the source archive of our ptsp-server package.

Rootfs is created with the help of a script called *"build-client.py"*, placed at the root of
`ptsp <http://websvn.pardus.org.tr/uludag/trunk/ptsp/>`_ Addition to this script,
required packages listed above also live under this URL. 

Following is an example for creating a rootfs in the current working directory, using Corporate2 packages repo ::

#python build-client.py -o ptsp-client-rootfs/ -r http://paketler.pardus.org.tr/corporate2/pisi-index.xml.bz2

List of options for creating rootfs::

    Usage: build-client.py [option ...]
    Following options are available:

    -h, --help            display this help and exit
    -o, --output          create the ptsp client rootfs into the given output path
    -r, --repository      ptsp client rootfs packages will be installed from this repository
    -a, --additional      install the given additional packages to ptsp client rootfs 

Preparing Server
----------------

First of all install *"dhcp"*, *"tftp"*, *"perl-X11-Protocol"*, *"xdg-user-dirs"*, *"ptsp-server"* packages on the server. As all these packages are dependent on *"ptsp-server"*, installing only this will cause all others to be installed. After installing required packages, apply following settings on the server:

#. **Configuring DHCP Server**

    With *"dhcp"* package, you will be running your own dhcp server. In order to distribute IP addresses for your clients, removing comments in the **/etc/dhcp/dhcpd.conf** file and then starting your dhcp service with "*service dhcpd start*" command will be enough for now on. If you have two network cards ("*ie. two ethernet cards; one for the internet , the other for the LAN*"), you must tell dhcp service on which interface it must be listening for dhcp requests by assigning the name of the interface to the **DHCPD_IFACE** in the **/etc/conf.d/dhcpd** configuration file.

#.  **Configuring Display Manager**

    Programs that seem to run on thin clients actually don't run on the clients; they run on the server completely and only their output is sent to the clients over Xdmcp protocol which uses UDP port 177. On the server we must enable Xdmcp request-listening by changing *"[Xdmcp]"* section to *"Enable=true"*. X session must be restarted for these changes to take place.

#. **Configuring NFS Server**

    Clients mount their rootfs which we have created earlier over NFS. In order to achieve this, we define the directory which will be exported in the **/etc/exports** file. Add the following line to your own configuration (Notice that after ip block definiton we don't leave any whitespaces which may cause your settings to be unrecognized.)::

    /opt/ptsp       10.0.0.0/255.255.255.0(ro, no_root_squash)

#. **Editing /etc/hosts File**

    For every IP address obtained by thin clients from the DHCP server, a hostname must be defined in the **/etc/hosts** file on the server, in order to make USB devices work on thin clients. Moreover, hostnames that will be assigned to the clients together with the range of IP addresses defined in **/etc/dhcp/dhcpd.conf** must be added here ("*ie. /etc/dhcp/dhcpd.conf: range 10.0.0.2 -  10.0.0.10"*). On the client-side no extra operation is necessary; they add automatically their own IP address and hostname couple. An example for **/etc/hosts** file on the server::

        10.0.0.2        thin2
        10.0.0.3        thin3
        10.0.0.4        thin4
        10.0.0.5        thin5

#. **Loading Fuse Kernel Module**

    On the server **fuse** kernel module must be loaded. In order to load, type "*modprobe fuse*" on the command line. If you wish this to be done everytime your server boots, add **fuse** to the end of **/etc/modules.autoload.d/kernel-2.6** file.

    - Note : Since Pardus-2009 release **fuse** module comes automatically loaded, you don't need to this if you use 2009 or newer version of Pardus.

#. **Setting Up Sound Server**

    With the help of **pulseaudio** package, we are able to have a working sound system on the clients. Actually, multimedia program runs on the server and with **pulseaudio**, sound output of the program is sent to thin client over the network, so it is possible to hear sound output as we are running the program locally on thin client.

    Open **/opt/ptsp/etc/pulse/system.pa** configuration file and remove comments in the following lines::

        [...]
        load-module module-esound-protocol-tcp
        load-module module-native-protocol-tcp auth-ip-acl=127.0.0.1;10.0.0.0/16
        load-module module-zeroconf-publish
        [...]

#. **Don't Let Firefox Cache PixMaps**

   Especially on thin clients which lack high memory, when user browse the web pages that contain too many or relatively big-sized images with Firefox, we could come up with situations like alll of X sessions are terminated. The reason of that is Firefox which runs on the server tries to cache images on the X and this causes thin client memory be stuck with this. As a result, this circumstance leads to call of *"OOM killer"* and on the client X process is killed by thin client kernel. Related sources with the bug:

   * http://www.francisrobichaud.com/index.php/2008/07/08/optimizing-mozilla-and-pixmap-management-in-x

   * https://bugzilla.mozilla.org/show_bug.cgi?id=296818

   In order to prevent this to happen, type following comman command on the server::

   $echo "MOZ_DISABLE_IMAGE_OPTIMIZE=1" > /etc/env.d/11MozillaFirefoxPixmap


Running Server
--------------

- Before we run the server, make sure **ptsp-server** and **dhcp server** has the 10.0.0.1 IP address.

- Our thin clients connect to the X server using *"SERVER*" parameter in *"/opt/ptsp/etc/pts-client.conf"* (which is client-rootfs), so if you plan to change your server's IP address, consider changing here as well. Also, apply the same changes in the **pulseaudio** config file to make it broadcast to the relevant network.


- Till now, we have been working on configuring our thin client workspace environment. Now, everything is ready and lets start running our server and make clients boot:

    * Start **dhcp**, **tftp**, **portmap** and **nfs_utils** services by typing *"service <service_name> start"*



Features
--------

* Easy to set up a thin client workspace environment.

* Lowered management load.

Requirements
------------

* On the server, you need to install *"dhcp"*, *"tftp"*, *"ltspfs"*, *"perl-X11-Protocol"*, *"xdg-user-dirs"* and *"ptsp-server"* packages. As *"ptsp-server"* package depends rest of all, installing just that package will be enough.

* On thin clients you don't need to install any extra software. In your BIOS settings, just setup your thin clients to boot from LAN (default they might be so).

Bugs
----

* `Normal Priority Bug Reports <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=normal&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=PTSP>`_

* `Wish Reports <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=low&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=PTSP>`_

* `Feature Requests <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=newfeature&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=PTSP>`_

Tasks
-----

* `Open Tasks <http://proje.pardus.org.tr:50030/projects/ptsp/issues?set_filter=1&tracker_id=4>`_

Source Code
-----------

You can `browse <http://websvn.pardus.org.tr/uludag/trunk/ptsp/>`_
source code from WebSVN_.

Or you can get the current version from Pardus SVN using following commands::

$ svn co https://svn.pardus.org.tr/uludag/trunk/ptsp

Developed by
------------

**Curent Developers**

* Metin Akdere <metin_at_pardus.org.tr>

**Previous Developers & Contributors**

* Faik Uygur <faik_at_pardus.org.tr>

License
-------

PTSP is distributed under the terms of the
`GNU General Public License (GPL), Version 2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>`_.

.. _COMAR: http://developer.pardus.org.tr/projects/comar/
.. _Coolplug: https://svn.pardus.org.tr/uludag/trunk/coolplug/
.. _LTSP: http://www.ltsp.org/
.. _Mudur: https://svn.pardus.org.tr/uludag/trunk/mudur/
.. _Pisi: http://developer.pardus.org.tr/projects/pisi/
.. _Python: http://www.python.org/
.. _Perl: http://www.perl.org/
.. _WebSVN: http://websvn.pardus.org.tr/uludag/trunk/ptsp/
.. _Zorg: https://svn.pardus.org.tr/uludag/trunk/zorg/
