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

---

Running Server
--------------

---

Features
--------

---

Requirements
------------

---

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

.. _COMAR: https://svn.pardus.org.tr/uludag/trunk/comar/
.. _Coolplug: https://svn.pardus.org.tr/uludag/trunk/coolplug/
.. _LTSP: http://www.ltsp.org/
.. _Mudur: https://svn.pardus.org.tr/uludag/trunk/mudur/
.. _Pisi: http://developer.pardus.org.tr/pisi/
.. _Python: http://www.python.org/
.. _Perl: http://www.perl.org/
.. _WebSVN: http://websvn.pardus.org.tr/uludag/trunk/ptsp/
.. _Zorg: https://svn.pardus.org.tr/uludag/trunk/zorg/
