Service Manager
~~~~~~~~~~~~~~~

:Author: Mehmet Özdemir

Service Manager is used for to manage systems services' status and their start options. A service's status may be running or stopped and its start option can be set as 'Run on startup' or not. If a service is running, it can serve something related to its job otherwise it is stopped and serves nothing. You can manage your services via Service Manager easily.

Features
--------

* Listing And Searching Services
    - Listing servers
    - Listing system services
    - Listing boot servies
    - Listing running servies
    - Listing all services
* Starting a Service
* Stopping a Service
* Restarting a Service
* Starting services automatically at startup


Source Code
-----------

You can `browse <http://svn.pardus.org.tr/uludag/branches/kde/service-manager/>`_
source code from WebSVN_.

Or you can get the current version from Pardus SVN using following commands::

$ svn co https://svn.pardus.org.tr/uludag/branches/kde/service-manager/

Requirements
------------

* python-qt
* python-kde

Bugs
----

* `Normal Priority Bug Reports <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=normal&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=Servis%20Y%C3%B6neticisi%20%2F%20Service%20Manager>`_
* `Wish Reports <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=low&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=Servis%20Y%C3%B6neticisi%20%2F%20Service%20Manager>`_
* `Feature Requests <http://bugs.pardus.org.tr/buglist.cgi?bug_severity=newfeature&classification=Pardus%20Teknolojileri%20%2F%20Pardus%20Technologies&query_format=advanced&bug_status=NEW&bug_status=ASSIGNED&bug_status=REOPENED&product=Servis%20Y%C3%B6neticisi%20%2F%20Service%20Manager>`_

Tasks
-----

* `Open Tasks <http://proje.pardus.org.tr:50030/projects/service-manager/issues?set_filter=1&tracker_id=4>`_

Developed by
------------

* Bahadır Kandemir <bahadir [at] pardus.org.tr>

License
-------

Service Manager is distributed under the terms of the `GNU General Public License (GPL), Version 2 <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>`_.

.. _Pisi: http://developer.pardus.org.tr/pisi
.. _Python: http://www.python.org
.. _WebSVN: http://websvn.pardus.org.tr
