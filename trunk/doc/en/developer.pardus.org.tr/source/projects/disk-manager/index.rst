Disk Manager
~~~~~~~~~~~~

:Author: Mehmet Özdemir 

Disk Manager is a Pardus GUI application used for managing /etc/fstab file. 
It provides an easy interface to set storage devices' mount settings. These 
settings are used at the system startup. 

Features
--------

* Add an entry. (entry = a line which is used for to describe partition initialization information)
   - Adding an entry includes a mount operation if that entry is not already mounted.
* Remove an entry
* Mount a partition
* Unmount a partition

Source Code
-----------

You can `browse <http://svn.pardus.org.tr/uludag/branches/kde/disk-manager/>`_
source code from WebSVN_.

Or you can get the current version from Pardus SVN using following commands::

$ svn co https://svn.pardus.org.tr/uludag/branches/kde/disk-manager/

Requirements
------------

* PyQt3 
* PyKDE3 
* kdelibs 
* dbus-python 

Bugs
----

* `Normal Priority Bug Reports <http://hata.pardus.org.tr/enter_bug.cgi?bug_severity=normal&product=Disk%20Y%C3%B6neticisi%20%2F%20Disk%20Manager>`_
* `Wish Reports <http://hata.pardus.org.tr/enter_bug.cgi?bug_severity=low&product=Disk%20Y%C3%B6neticisi%20%2F%20Disk%20Manager>`_
* `Feature Requests <http://hata.pardus.org.tr/enter_bug.cgi?bug_severity=newfeature&product=Disk%20Y%C3%B6neticisi%20%2F%20Disk%20Manager>`_

Developed by
------------

* Gökmen GÖKSEL <gokmen [at] pardus.org.tr>
* İşbaran AKÇAYIR <isbaran [at] gmail.com>

Fstab Module Authors:

*A.Murat EREN <meren [at] pardus.org.tr>
*Onur KÜÇÜK <onur [at] pardus.org.tr>

License
-------

Disk Manager is distributed under the terms of the `GNU General Public License (GPL), Version 2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>`_.

.. _Pisi: http://developer.pardus.org.tr/pisi
.. _Python: http://www.python.org
.. _WebSVN: http://websvn.pardus.org.tr
