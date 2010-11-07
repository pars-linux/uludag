.. _package-manager-index:

Package Manager
~~~~~~~~~~~~~~~

:Author: Gökmen Göksel

**Package Manager** is a graphical user interface for Pardus' Package
Management System Pisi_ and used to search, install or upgrade packages from
Pardus package repository. It's a handy and usable tool to manage your packages
in an easy way.

Features
--------

* Install, remove or upgrade packages:

  - It is possible to operate packages one by one or multiple
  - Basket support to operate selected multiple packages
* Package search with in each main category which are *"Installed Packges"*, 
  *"New Packages"* or *"Upgradable Packages"*
* System Tray support for checking updates with predefined interval
* Automatic update support
* Notification support for each action
* It is possible to install a package with one click by using ``pm-install``
* Manage system-wide Pisi_ options:

  - Manage source repositories
  - Manage cache options of Pisi_
  - Manage bandwith limit options of Pisi_
  - Manage proxy options of Pisi_

Source Code
-----------

You can `browse <http://websvn.pardus.org.tr/uludag/trunk/kde/package-manager/manager/>`_
source code from WebSVN_.

Or you can get the current version from Pardus SVN using following commands::

$ svn co https://svn.pardus.org.tr/uludag/trunk/kde/package-manager/manager

Requirements
------------

* Pisi_ 2.1 or higher
* Python_ 2.6 or higher
* PyQt 4.5 or higher
* PyKDE 4.3 or higher

Tasks
-----

* `Open tasks <http://proje.pardus.org.tr:50030/projects/pm/issues?set_filter=1&tracker_id=4>`_

Bugs
----

* `Normal Priority Bug Reports <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=normal&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=Paket%20Y%C3%B6neticisi%20%2F%20Package%20Manager>`_
* `Wish Reports <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=low&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=Paket%20Y%C3%B6neticisi%20%2F%20Package%20Manager>`_
* `Feature Requests <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=newfeature&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=Paket%20Y%C3%B6neticisi%20%2F%20Package%20Manager>`_

Developed by
------------

* Gökmen Göksel <gokmen_at_pardus.org.tr>
  Lead Developer

* Faik Uygur <faik_at_pardus.org.tr>
  First Developer

License
-------

Package Manager is distributed under the terms of the `GNU General Public License (GPL), Version 2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>`_.

.. _Pisi: http://developer.pardus.org.tr/projects/pisi/index.html
.. _Python: http://www.python.org
.. _WebSVN: http://websvn.pardus.org.tr/uludag/trunk/kde/package-manager/
