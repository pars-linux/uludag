.. _firewall-manager-index:

Firewall Manager
~~~~~~~~~~~~~~~~

:Author: Mehmet Özdemir

Firewall Manager is used for defining port blocking rules over a system's communication with other systems. These rules block or allow a connection attempt. These attempts may be either made by your system or a remote system. You can configure these rules via Firewall Manager.

Features
--------

* Activating Firewall
* Deactivating Firewall
* Editing Incoming Connection Rules
	- Adding an incoming rule
	- Deleting an incoming rule
* Editing Outgoing Connection Rules
	- Adding an outgoing rule
	- Deleting an outgoing rule
* Using Your Computer As A Gateway

Source Code
-----------

You can `browse <http://svn.pardus.org.tr/uludag/branches/kde/firewall-manager/>`_
source code from WebSVN_.

Or you can get the current version from Pardus SVN using following commands::

$ svn co https://svn.pardus.org.tr/uludag/branches/kde/firewall-manager/

Requirements
------------

* PyQt3
* kdelibs
* PyKDE3
* iptables


Bugs
----

* `Normal Priority Bug Reports <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=normal&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=G%C3%BCvenlik%20Duvar%C4%B1%20Y%C3%B6neticisi%20%2F%20Firewall%20Manager>`_
* `Wish Reports <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=low&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=G%C3%BCvenlik%20Duvar%C4%B1%20Y%C3%B6neticisi%20%2F%20Firewall%20Manager>`_
* `Feature Requests <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=newfeature&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=G%C3%BCvenlik%20Duvar%C4%B1%20Y%C3%B6neticisi%20%2F%20Firewall%20Manager>`_

Tasks
-----

* `Open Tasks <http://proje.pardus.org.tr:50030/projects/firewall-manager/issues?set_filter=1&tracker_id=4>`_

Developed by
------------

* Bahadır Kandemir <bahadir [at] pardus.org.tr> 

License
-------

Firewall Manager is distributed under the terms of the `GNU General Public License (GPL), Version 2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>`_.

.. _Pisi: http://developer.pardus.org.tr/pisi
.. _Python: http://www.python.org
.. _WebSVN: http://websvn.pardus.org.tr
