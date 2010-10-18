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

Bugs
----

* `Normal Priority Bug Reports <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=normal&chfieldto=Now&query_format=advanced&chfieldfrom=2006-07-14&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&component=Grafik%20Aray%C3%BCz%C3%BC%20/%20Graphical%20User%20Interface&product=PiSi>`_
* `Wish Reports <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=low&chfieldto=Now&query_format=advanced&chfieldfrom=2006-07-14&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&component=Grafik%20Aray%C3%BCz%C3%BC%20/%20Graphical%20User%20Interface&product=PiSi>`_
* `Feature Requests <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=newfeature&chfieldto=Now&query_format=advanced&chfieldfrom=2006-07-14&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&component=Grafik%20Aray%C3%BCz%C3%BC%20/%20Graphical%20User%20Interface&product=PiSi>`_

Developed by
------------

* Gökmen Göksel <gokmen_at_pardus.org.tr>
  Lead Developer

* Faik Uygur <faik_at_pardus.org.tr>
  First Developer

License
-------

Package Manager is distributed under the terms of the `GNU General Public License (GPL), Version 2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>`_.

.. _Pisi: http://developer.pardus.org.tr/pisi
.. _Python: http://www.python.org
.. _WebSVN: http://websvn.pardus.org.tr
